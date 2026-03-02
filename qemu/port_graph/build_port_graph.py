#!/usr/bin/env python3
"""
Build a Mermaid diagram of QEMU/libvirt domain interconnect port relationships
from domain XML files (e.g. virsh dumpxml output saved under a data directory).

Reads all domain XMLs in the given directory (not in subdirs like networks/),
parses <interface type='udp'>, type='client', type='server' to find
address:port endpoints, resolves peer domains, and emits a Mermaid flowchart.

Usage:
  python build_port_graph.py [--data DIR] [--output FILE] [--font-size 20px] [--node-padding 16]
  python build_port_graph.py --html [--width 1200] [--height 900]  # scale-to-fit in a fixed-size page
  Default: --data data/qemu  --output port_graph.md
  Use --html to emit a self-contained HTML file that renders the diagram in a given width/height and
  scale-to-fits so the diagram fills the space (bigger boxes and text, easier to read).
"""

import argparse
import os
import re
import xml.etree.ElementTree as ET
from typing import Any, Dict, List, Optional, Set, Tuple


def _mermaid_id(name: str) -> str:
    """Mermaid node IDs must be alphanumeric + underscore; no leading digit."""
    s = re.sub(r"[^A-Za-z0-9_]", "_", name)
    if s and s[0].isdigit():
        s = "n_" + s
    return s or "unnamed"


def _is_expandable_domain(domain_name: str) -> bool:
    """True if this domain should be rendered as a subgraph of port nodes (mgmt, lb)."""
    return "-mgmt-" in domain_name or "-lb-" in domain_name


def _short_name(domain_name: str) -> str:
    """Short label for display (e.g. jss-0-mgmt-5a86842b -> mgmt, jss-0-lb-437d2932 -> lb-437d2932)."""
    if "-mgmt-" in domain_name:
        return "mgmt"
    if "-lb-" in domain_name:
        # jss-0-lb-437d2932 -> lb-437d2932 (serial distinguishes multiple LBs)
        return "lb-" + domain_name.split("-lb-", 1)[1]
    if "-csw1-" in domain_name:
        return "csw1"
    if "-csw2-" in domain_name:
        return "csw2"
    # Service/storage node: jss-0-427fc39f -> node-427fc39f
    parts = domain_name.split("-")
    if len(parts) >= 3 and parts[0] == "jss" and parts[1].isdigit():
        return "node-" + parts[-1]
    return domain_name


def parse_domain_xml(path: str) -> Optional[Tuple[str, List[Dict[str, Any]]]]:
    """
    Parse a single domain XML file. Returns (domain_name, list of interface dicts)
    or None if not a domain or parse error.
    """
    try:
        tree = ET.parse(path)
    except ET.ParseError:
        return None
    root = tree.getroot()
    if root.tag != "domain":
        return None
    name_el = root.find("name")
    domain_name = name_el.text.strip() if name_el is not None and name_el.text else ""
    if not domain_name:
        return None

    interfaces: List[Dict[str, Any]] = []
    devices = root.find("devices")
    if devices is None:
        return (domain_name, interfaces)

    for idx, iface in enumerate(devices.findall("interface")):
        iface_type = iface.get("type") or ""
        if iface_type not in ("udp", "client", "server"):
            continue

        source = iface.find("source")
        if source is None:
            continue

        remote_addr = source.get("address")
        remote_port = source.get("port")
        if remote_port is not None:
            try:
                remote_port = int(remote_port)
            except ValueError:
                remote_port = None

        local_addr: Optional[str] = None
        local_port: Optional[int] = None
        local_el = source.find("local")
        if local_el is not None:
            local_addr = local_el.get("address")
            p = local_el.get("port")
            if p is not None:
                try:
                    local_port = int(p)
                except ValueError:
                    pass

        interfaces.append({
            "idx": idx,
            "type": iface_type,
            "local_addr": local_addr,
            "local_port": local_port,
            "remote_addr": remote_addr,
            "remote_port": remote_port,
        })

    return (domain_name, interfaces)


def collect_domain_xmls(data_dir: str) -> List[str]:
    """Return list of domain XML paths (top-level .xml only, no networks subdir)."""
    data_dir = os.path.abspath(data_dir)
    if not os.path.isdir(data_dir):
        return []
    paths = []
    for name in os.listdir(data_dir):
        if name.endswith(".xml"):
            p = os.path.join(data_dir, name)
            if os.path.isfile(p):
                paths.append(p)
    return sorted(paths)


def build_endpoint_to_domain(
    domain_interfaces: Dict[str, List[Dict[str, Any]]],
) -> Dict[Tuple[str, int], str]:
    """Map (address, port) -> domain name for endpoints that 'own' that address:port (listen or udp local)."""
    endpoint_to_domain: Dict[Tuple[str, int], str] = {}
    for domain_name, ifaces in domain_interfaces.items():
        for iface in ifaces:
            if iface["type"] == "udp" and iface.get("local_addr") and iface.get("local_port") is not None:
                key = (iface["local_addr"], iface["local_port"])
                endpoint_to_domain[key] = domain_name
            if iface["type"] == "server" and iface.get("remote_addr") and iface.get("remote_port") is not None:
                # Server listens on remote_addr:remote_port in libvirt terms (source = listen address)
                key = (iface["remote_addr"], iface["remote_port"])
                endpoint_to_domain[key] = domain_name
    return endpoint_to_domain


def build_edges(
    domain_interfaces: Dict[str, List[Dict[str, Any]]],
    endpoint_to_domain: Dict[Tuple[str, int], str],
) -> List[Tuple[str, str, int, str]]:
    """List of (domain_a, domain_b, port, iface_type) for each link (no duplicate pairs)."""
    seen: Set[Tuple[str, str, int]] = set()
    edges: List[Tuple[str, str, int, str]] = []

    for domain_name, ifaces in domain_interfaces.items():
        for iface in ifaces:
            remote_addr = iface.get("remote_addr")
            remote_port = iface.get("remote_port")
            if remote_addr is None or remote_port is None:
                continue
            peer = endpoint_to_domain.get((remote_addr, remote_port))
            if not peer or peer == domain_name:
                continue
            key = tuple(sorted([domain_name, peer])) + (remote_port,)
            if key in seen:
                continue
            seen.add(key)
            edges.append((domain_name, peer, remote_port, iface["type"]))

    return edges


def emit_mermaid_flowchart(
    domain_names: List[str],
    edges: List[Tuple[str, str, int, str]],
    node_spacing: int = 40,
    rank_spacing: int = 520,
    diagram_padding: int = 80,
    graph_font_size: str = "20px",
    subgraph_font_size: str = "14px",
    node_padding: int = 16,
) -> str:
    """Produce Mermaid flowchart source (content only, no fence).
    Mgmt and LB domains are rendered as subgraphs of physical port nodes; service
    nodes that connect to them are also rendered as subgraphs of port nodes so
    both ends of each edge are ports and labels do not collide.
    We don't want theme=base because it causes contrast bleeding between nodes and subgraphs.
    """
    init = (
        "%%{init: {"
        "'themeVariables': { 'fontSize': " + repr(graph_font_size) + " }, "
        "'flowchart': {"
        f"'nodeSpacing': {node_spacing}, "
        f"'rankSpacing': {rank_spacing}, "
        f"'diagramPadding': {diagram_padding}"
        "}}}%%"
    )
    lines = [init, "flowchart TB", ""]
    node_ids = {d: _mermaid_id(d) for d in domain_names}

    expandable_target = {d for d in domain_names if _is_expandable_domain(d)}
    expandable_source = {
        domain_a for (domain_a, domain_b, _p, _t) in edges
        if domain_b in expandable_target
    }

    # (domain, port) -> port node id for mgmt/LB (target) subgraphs
    port_nodes_target: Dict[Tuple[str, int], str] = {}
    # port node id -> iface type ("udp", "client", "server") for coloring
    port_node_types: Dict[str, str] = {}
    for _a, domain_b, port, iface_type in edges:
        if domain_b in expandable_target:
            key = (domain_b, port)
            if key not in port_nodes_target:
                pid = node_ids[domain_b] + "_p" + str(port)
                port_nodes_target[key] = pid
                port_node_types[pid] = iface_type

    # (domain_a, domain_b, port) -> port node id for service node (source) subgraphs
    port_nodes_source: Dict[Tuple[str, str, int], str] = {}
    for domain_a in expandable_source:
        out_edges = sorted(
            (domain_b, port, iface_type)
            for (a, domain_b, port, iface_type) in edges
            if a == domain_a and domain_b in expandable_target
        )
        for idx, (domain_b, port, iface_type) in enumerate(out_edges):
            pid = node_ids[domain_a] + "_p" + str(idx)
            port_nodes_source[(domain_a, domain_b, port)] = pid
            port_node_types[pid] = iface_type

    # Regular nodes only for domains that are neither target nor source subgraphs
    for d in domain_names:
        if d in expandable_target or d in expandable_source:
            continue
        nid = node_ids[d]
        short = _short_name(d)
        lines.append(f"  {nid}(\"{short}\")")
    lines.append("")

    # Storage node (leaf) subgraphs at top level - not wrapped in a parent
    for d in sorted(expandable_source):
        short = _short_name(d)
        out_edges = sorted(
            (domain_b, port, iface_type)
            for (a, domain_b, port, iface_type) in edges
            if a == d and domain_b in expandable_target
        )
        if not out_edges:
            continue
        lines.append(f"  subgraph {node_ids[d]}[\"{short}\"]")
        for idx, (_db, port, iface_type) in enumerate(out_edges):
            pid = node_ids[d] + "_p" + str(idx)
            label = f"{port} {iface_type}"
            lines.append(f"    {pid}(\"{label}\")")
        lines.append("  end")
        lines.append("")

    # Mgmt/LB subgraphs at top level - each its own subgraph (no parent wrapper)
    for d in sorted(expandable_target):
        short = _short_name(d)
        ports_here = sorted({port for (dom, port) in port_nodes_target if dom == d})
        if not ports_here:
            continue
        lines.append(f"  subgraph {node_ids[d]}[\"{short}\"]")
        for port in ports_here:
            pid = port_nodes_target[(d, port)]
            iface_type = port_node_types.get(pid, "udp")
            label = f"{port} {iface_type}"
            lines.append(f"    {pid}(\"{label}\")")
        lines.append("  end")
        lines.append("")

    # Edges: port-to-port when both ends are subgraphs, else node-to-port or node-to-node
    for domain_a, domain_b, port, iface_type in edges:
        if domain_b in expandable_target:
            b_id = port_nodes_target[(domain_b, port)]
            if domain_a in expandable_source:
                a_id = port_nodes_source[(domain_a, domain_b, port)]
                lines.append(f"  {a_id} --> {b_id}")
            else:
                a_id = node_ids[domain_a]
                lines.append(f"  {a_id} --> {b_id}")
        else:
            a_id = node_ids[domain_a]
            b_id = node_ids[domain_b]
            label = f"port {port}"
            if iface_type != "udp":
                label += f" {iface_type}"
            lines.append(f"  {a_id} -->|{label}| {b_id}")

    # Bigger boxes: apply class to all node ids; smaller font for subgraph titles
    all_ids: List[str] = [node_ids[d] for d in domain_names if d not in expandable_target and d not in expandable_source]
    all_ids.extend(port_nodes_target.values())
    all_ids.extend(port_nodes_source.values())
    subgraph_ids = list(expandable_source) + list(expandable_target)
    subgraph_mermaid_ids = [node_ids[d] for d in subgraph_ids]
    lines.append("")
    lines.append(f"  classDef wide padding:{node_padding}px")
    lines.append(f"  class {','.join(all_ids)} wide")
    if subgraph_mermaid_ids:
        lines.append(f"  classDef subgraphTitle font-size:{subgraph_font_size}")
        lines.append(f"  class {','.join(subgraph_mermaid_ids)} subgraphTitle")
    # Color port submodules by iface type using blue hues so we don't imply status.
    udp_ids = [pid for pid, t in port_node_types.items() if t == "udp"]
    client_ids = [pid for pid, t in port_node_types.items() if t == "client"]
    server_ids = [pid for pid, t in port_node_types.items() if t == "server"]
    if udp_ids:
        # Darker blues so white text has enough contrast.
        lines.append("  classDef port_udp fill:#1976d2,stroke:#0d47a1,stroke-width:1px,color:#ffffff")
        lines.append(f"  class {','.join(udp_ids)} port_udp")
    if client_ids:
        lines.append("  classDef port_client fill:#1565c0,stroke:#0d47a1,stroke-width:1px,color:#ffffff")
        lines.append(f"  class {','.join(client_ids)} port_client")
    if server_ids:
        lines.append("  classDef port_server fill:#0d47a1,stroke:#082567,stroke-width:1px,color:#ffffff")
        lines.append(f"  class {','.join(server_ids)} port_server")
    return "\n".join(lines)


def emit_markdown(
    domain_names: List[str],
    edges: List[Tuple[str, str, int, str]],
    title: str = "QEMU interconnect port graph",
    node_spacing: int = 120,
    rank_spacing: int = 520,
    diagram_padding: int = 80,
    graph_font_size: str = "20px",
    subgraph_font_size: str = "14px",
    node_padding: int = 16,
) -> str:
    """Produce Markdown with a mermaid fenced code block."""
    flowchart = emit_mermaid_flowchart(
        domain_names,
        edges,
        node_spacing=node_spacing,
        rank_spacing=rank_spacing,
        diagram_padding=diagram_padding,
        graph_font_size=graph_font_size,
        subgraph_font_size=subgraph_font_size,
        node_padding=node_padding,
    )
    return f"# {title}\n\n```mermaid\n{flowchart}\n```\n"


def emit_html(
    domain_names: List[str],
    edges: List[Tuple[str, str, int, str]],
    title: str = "QEMU interconnect port graph",
    width_px: int = 1200,
    height_px: int = 900,
    node_spacing: int = 120,
    rank_spacing: int = 520,
    diagram_padding: int = 80,
    graph_font_size: str = "22px",
    subgraph_font_size: str = "14px",
    node_padding: int = 20,
) -> str:
    """Produce a self-contained HTML file that renders the diagram in a fixed-size
    container and scale-to-fits so the diagram fills the space.
    """
    flowchart = emit_mermaid_flowchart(
        domain_names,
        edges,
        node_spacing=node_spacing,
        rank_spacing=rank_spacing,
        diagram_padding=diagram_padding,
        graph_font_size=graph_font_size,
        subgraph_font_size=subgraph_font_size,
        node_padding=node_padding,
    )
    # Prevent </script> in diagram from closing the script tag.
    diagram_safe = flowchart.replace("</script>", "<\\/script>")
    font_size_css = graph_font_size.replace("'", "\\'")
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({{ startOnLoad: false }});
    const el = document.getElementById('diagram');
    const container = document.getElementById('container');
    const w = {width_px};
    const h = {height_px};
    try {{
      const {{ svg }} = await mermaid.render('mermaid-svg', el.textContent);
      container.innerHTML = svg;
      const svgEl = container.querySelector('svg');
      if (svgEl) {{
        const vb = svgEl.getAttribute('viewBox');
        if (vb) {{
          const parts = vb.split(/\\\\s+/);
          const vw = Number(parts[2]);
          const vh = Number(parts[3]);
          const scale = Math.min(w / vw, h / vh, 3);
          svgEl.setAttribute('width', Math.round(vw * scale));
          svgEl.setAttribute('height', Math.round(vh * scale));
          svgEl.style.maxWidth = '100%';
          svgEl.style.height = 'auto';
        }}
      }}
    }} catch (e) {{
      container.innerHTML = '<pre style="color:red">' + e.message + '</pre>';
    }}
  </script>
  <style>
    body {{ margin: 0; font-family: sans-serif; }}
    #container {{
      width: {width_px}px;
      height: {height_px}px;
      max-width: 100vw;
      max-height: calc(100vh - 2em);
      margin: 1em auto;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: auto;
      border: 1px solid #ccc;
    }}
    /* Resize Mermaid diagrams to fit on the page by default */
    .mermaid svg {{
      max-width: 100%;
      height: auto;
    }}
    #container svg {{
      max-width: 100%;
      height: auto;
      flex-shrink: 0;
    }}
    #container svg text {{
      font-size: {font_size_css} !important;
    }}
  </style>
</head>
<body>
  <h1 style="text-align:center; margin:0.5em 0">{title}</h1>
  <div id="container"></div>
  <script type="text/plain" id="diagram">
{diagram_safe}
  </script>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build Mermaid port graph from libvirt domain XML files",
    )
    parser.add_argument(
        "--data",
        default=os.path.join(os.path.dirname(__file__), "data", "qemu"),
        help="Directory containing domain XML files",
    )
    parser.add_argument(
        "--output",
        default="port_graph.md",
        help="Output Markdown file path (.md with mermaid code block)",
    )
    parser.add_argument(
        "--node-spacing",
        type=int,
        default=300,
        metavar="N",
        help="Mermaid flowchart nodeSpacing (default 120)",
    )
    parser.add_argument(
        "--rank-spacing",
        type=int,
        default=520,
        metavar="N",
        help="Mermaid flowchart rankSpacing (default 520; vertical gap in TB layout)",
    )
    parser.add_argument(
        "--diagram-padding",
        type=int,
        default=80,
        metavar="N",
        help="Mermaid flowchart diagramPadding (default 80)",
    )
    parser.add_argument(
        "--graph-font-size",
        default="20px",
        metavar="SIZE",
        help="Graph font size for nodes and labels (default 20px, use larger e.g. 24px for readability)",
    )
    parser.add_argument(
        "--subgraph-font-size",
        default="14px",
        metavar="SIZE",
        help="Subgraph title font size (default 14px)",
    )
    parser.add_argument(
        "--node-padding",
        type=int,
        default=16,
        metavar="N",
        help="Extra padding inside each node in px (default 16)",
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Emit a self-contained HTML file that renders the diagram in a fixed-size area and scale-to-fits",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1200,
        metavar="PX",
        help="Container width in px when using --html (default 1200)",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=900,
        metavar="PX",
        help="Container height in px when using --html (default 900)",
    )
    args = parser.parse_args()

    paths = collect_domain_xmls(args.data)
    if not paths:
        print(f"No domain XMLs found in {args.data}")
        return

    domain_interfaces: Dict[str, List[Dict[str, Any]]] = {}
    for path in paths:
        result = parse_domain_xml(path)
        if result is None:
            continue
        name, ifaces = result
        if not ifaces:
            continue
        domain_interfaces[name] = ifaces

    if not domain_interfaces:
        print("No interconnect interfaces (udp/client/server) found in any domain XML.")
        return

    endpoint_to_domain = build_endpoint_to_domain(domain_interfaces)
    edges = build_edges(domain_interfaces, endpoint_to_domain)

    domain_names = sorted(domain_interfaces.keys())

    if args.html:
        out_path = args.output if args.output != "port_graph.md" else "port_graph.html"
        content = emit_html(
            domain_names,
            edges,
            node_spacing=args.node_spacing,
            rank_spacing=args.rank_spacing,
            diagram_padding=args.diagram_padding,
            graph_font_size=args.graph_font_size,
            subgraph_font_size=args.subgraph_font_size,
            node_padding=args.node_padding,
            width_px=args.width,
            height_px=args.height,
        )
    else:
        out_path = args.output
        content = emit_markdown(
            domain_names,
            edges,
            node_spacing=args.node_spacing,
            rank_spacing=args.rank_spacing,
            diagram_padding=args.diagram_padding,
            graph_font_size=args.graph_font_size,
            subgraph_font_size=args.subgraph_font_size,
            node_padding=args.node_padding,
        )

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Wrote {len(edges)} edges among {len(domain_names)} domains to {out_path}")


if __name__ == "__main__":
    main()
