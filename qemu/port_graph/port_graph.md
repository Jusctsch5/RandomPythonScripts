# QEMU interconnect port graph

```mermaid
%%{init: {'themeVariables': { 'fontSize': '20px' }, 'flowchart': {'nodeSpacing': 300, 'rankSpacing': 520, 'diagramPadding': 80}}}%%
flowchart TB


  subgraph jss_0_427fc39f["node-427fc39f"]
    jss_0_427fc39f_p0("21103 udp")
    jss_0_427fc39f_p1("21119 udp")
    jss_0_427fc39f_p2("21003 udp")
    jss_0_427fc39f_p3("21019 udp")
    jss_0_427fc39f_p4("20003 udp")
  end

  subgraph jss_0_44995b32["node-44995b32"]
    jss_0_44995b32_p0("21101 udp")
    jss_0_44995b32_p1("21117 udp")
    jss_0_44995b32_p2("21001 udp")
    jss_0_44995b32_p3("21017 udp")
    jss_0_44995b32_p4("20001 udp")
  end

  subgraph jss_0_4e6aa585["node-4e6aa585"]
    jss_0_4e6aa585_p0("21105 udp")
    jss_0_4e6aa585_p1("21121 udp")
    jss_0_4e6aa585_p2("21005 udp")
    jss_0_4e6aa585_p3("21021 udp")
    jss_0_4e6aa585_p4("20005 udp")
  end

  subgraph jss_0_6a03e784["node-6a03e784"]
    jss_0_6a03e784_p0("21107 udp")
    jss_0_6a03e784_p1("21123 udp")
    jss_0_6a03e784_p2("21007 udp")
    jss_0_6a03e784_p3("21023 udp")
    jss_0_6a03e784_p4("20007 udp")
  end

  subgraph jss_0_6de98027["node-6de98027"]
    jss_0_6de98027_p0("21106 udp")
    jss_0_6de98027_p1("21122 udp")
    jss_0_6de98027_p2("21006 udp")
    jss_0_6de98027_p3("21022 udp")
    jss_0_6de98027_p4("20006 udp")
  end

  subgraph jss_0_712ce0f4["node-712ce0f4"]
    jss_0_712ce0f4_p0("21102 udp")
    jss_0_712ce0f4_p1("21118 udp")
    jss_0_712ce0f4_p2("21002 udp")
    jss_0_712ce0f4_p3("21018 udp")
    jss_0_712ce0f4_p4("20002 udp")
  end

  subgraph jss_0_72908381["node-72908381"]
    jss_0_72908381_p0("21100 udp")
    jss_0_72908381_p1("21116 udp")
    jss_0_72908381_p2("21000 udp")
    jss_0_72908381_p3("21016 udp")
    jss_0_72908381_p4("20000 udp")
  end

  subgraph jss_0_7618d0ec["node-7618d0ec"]
    jss_0_7618d0ec_p0("21104 udp")
    jss_0_7618d0ec_p1("21120 udp")
    jss_0_7618d0ec_p2("21004 udp")
    jss_0_7618d0ec_p3("21020 udp")
    jss_0_7618d0ec_p4("20004 udp")
  end

  subgraph jss_0_csw1_4758f8f1["csw1"]
    jss_0_csw1_4758f8f1_p0("22003 udp")
    jss_0_csw1_4758f8f1_p1("22004 udp")
    jss_0_csw1_4758f8f1_p2("22001 udp")
    jss_0_csw1_4758f8f1_p3("22002 udp")
  end

  subgraph jss_0_csw2_5b36d8c8["csw2"]
    jss_0_csw2_5b36d8c8_p0("22103 udp")
    jss_0_csw2_5b36d8c8_p1("22104 udp")
    jss_0_csw2_5b36d8c8_p2("22101 udp")
    jss_0_csw2_5b36d8c8_p3("22102 udp")
  end

  subgraph jss_0_lb_437d2932["lb-437d2932"]
    jss_0_lb_437d2932_p0("20021 udp")
  end

  subgraph jss_0_lb_685403e6["lb-685403e6"]
    jss_0_lb_685403e6_p0("20020 udp")
  end

  subgraph jss_0_lb_437d2932["lb-437d2932"]
    jss_0_lb_437d2932_p21100("21100 udp")
    jss_0_lb_437d2932_p21101("21101 udp")
    jss_0_lb_437d2932_p21102("21102 udp")
    jss_0_lb_437d2932_p21103("21103 udp")
    jss_0_lb_437d2932_p21104("21104 udp")
    jss_0_lb_437d2932_p21105("21105 udp")
    jss_0_lb_437d2932_p21106("21106 udp")
    jss_0_lb_437d2932_p21107("21107 udp")
    jss_0_lb_437d2932_p21116("21116 udp")
    jss_0_lb_437d2932_p21117("21117 udp")
    jss_0_lb_437d2932_p21118("21118 udp")
    jss_0_lb_437d2932_p21119("21119 udp")
    jss_0_lb_437d2932_p21120("21120 udp")
    jss_0_lb_437d2932_p21121("21121 udp")
    jss_0_lb_437d2932_p21122("21122 udp")
    jss_0_lb_437d2932_p21123("21123 udp")
    jss_0_lb_437d2932_p22003("22003 udp")
    jss_0_lb_437d2932_p22004("22004 udp")
    jss_0_lb_437d2932_p22103("22103 udp")
    jss_0_lb_437d2932_p22104("22104 udp")
  end

  subgraph jss_0_lb_685403e6["lb-685403e6"]
    jss_0_lb_685403e6_p21000("21000 udp")
    jss_0_lb_685403e6_p21001("21001 udp")
    jss_0_lb_685403e6_p21002("21002 udp")
    jss_0_lb_685403e6_p21003("21003 udp")
    jss_0_lb_685403e6_p21004("21004 udp")
    jss_0_lb_685403e6_p21005("21005 udp")
    jss_0_lb_685403e6_p21006("21006 udp")
    jss_0_lb_685403e6_p21007("21007 udp")
    jss_0_lb_685403e6_p21016("21016 udp")
    jss_0_lb_685403e6_p21017("21017 udp")
    jss_0_lb_685403e6_p21018("21018 udp")
    jss_0_lb_685403e6_p21019("21019 udp")
    jss_0_lb_685403e6_p21020("21020 udp")
    jss_0_lb_685403e6_p21021("21021 udp")
    jss_0_lb_685403e6_p21022("21022 udp")
    jss_0_lb_685403e6_p21023("21023 udp")
    jss_0_lb_685403e6_p22001("22001 udp")
    jss_0_lb_685403e6_p22002("22002 udp")
    jss_0_lb_685403e6_p22101("22101 udp")
    jss_0_lb_685403e6_p22102("22102 udp")
  end

  subgraph jss_0_mgmt_5a86842b["mgmt"]
    jss_0_mgmt_5a86842b_p20000("20000 udp")
    jss_0_mgmt_5a86842b_p20001("20001 udp")
    jss_0_mgmt_5a86842b_p20002("20002 udp")
    jss_0_mgmt_5a86842b_p20003("20003 udp")
    jss_0_mgmt_5a86842b_p20004("20004 udp")
    jss_0_mgmt_5a86842b_p20005("20005 udp")
    jss_0_mgmt_5a86842b_p20006("20006 udp")
    jss_0_mgmt_5a86842b_p20007("20007 udp")
    jss_0_mgmt_5a86842b_p20020("20020 udp")
    jss_0_mgmt_5a86842b_p20021("20021 udp")
  end

  jss_0_427fc39f_p4 --> jss_0_mgmt_5a86842b_p20003
  jss_0_427fc39f_p2 --> jss_0_lb_685403e6_p21003
  jss_0_427fc39f_p3 --> jss_0_lb_685403e6_p21019
  jss_0_427fc39f_p0 --> jss_0_lb_437d2932_p21103
  jss_0_427fc39f_p1 --> jss_0_lb_437d2932_p21119
  jss_0_44995b32_p4 --> jss_0_mgmt_5a86842b_p20001
  jss_0_44995b32_p2 --> jss_0_lb_685403e6_p21001
  jss_0_44995b32_p3 --> jss_0_lb_685403e6_p21017
  jss_0_44995b32_p0 --> jss_0_lb_437d2932_p21101
  jss_0_44995b32_p1 --> jss_0_lb_437d2932_p21117
  jss_0_4e6aa585_p4 --> jss_0_mgmt_5a86842b_p20005
  jss_0_4e6aa585_p2 --> jss_0_lb_685403e6_p21005
  jss_0_4e6aa585_p3 --> jss_0_lb_685403e6_p21021
  jss_0_4e6aa585_p0 --> jss_0_lb_437d2932_p21105
  jss_0_4e6aa585_p1 --> jss_0_lb_437d2932_p21121
  jss_0_6a03e784_p4 --> jss_0_mgmt_5a86842b_p20007
  jss_0_6a03e784_p2 --> jss_0_lb_685403e6_p21007
  jss_0_6a03e784_p3 --> jss_0_lb_685403e6_p21023
  jss_0_6a03e784_p0 --> jss_0_lb_437d2932_p21107
  jss_0_6a03e784_p1 --> jss_0_lb_437d2932_p21123
  jss_0_6de98027_p4 --> jss_0_mgmt_5a86842b_p20006
  jss_0_6de98027_p2 --> jss_0_lb_685403e6_p21006
  jss_0_6de98027_p3 --> jss_0_lb_685403e6_p21022
  jss_0_6de98027_p0 --> jss_0_lb_437d2932_p21106
  jss_0_6de98027_p1 --> jss_0_lb_437d2932_p21122
  jss_0_712ce0f4_p4 --> jss_0_mgmt_5a86842b_p20002
  jss_0_712ce0f4_p2 --> jss_0_lb_685403e6_p21002
  jss_0_712ce0f4_p3 --> jss_0_lb_685403e6_p21018
  jss_0_712ce0f4_p0 --> jss_0_lb_437d2932_p21102
  jss_0_712ce0f4_p1 --> jss_0_lb_437d2932_p21118
  jss_0_72908381_p4 --> jss_0_mgmt_5a86842b_p20000
  jss_0_72908381_p2 --> jss_0_lb_685403e6_p21000
  jss_0_72908381_p3 --> jss_0_lb_685403e6_p21016
  jss_0_72908381_p0 --> jss_0_lb_437d2932_p21100
  jss_0_72908381_p1 --> jss_0_lb_437d2932_p21116
  jss_0_7618d0ec_p4 --> jss_0_mgmt_5a86842b_p20004
  jss_0_7618d0ec_p2 --> jss_0_lb_685403e6_p21004
  jss_0_7618d0ec_p3 --> jss_0_lb_685403e6_p21020
  jss_0_7618d0ec_p0 --> jss_0_lb_437d2932_p21104
  jss_0_7618d0ec_p1 --> jss_0_lb_437d2932_p21120
  jss_0_csw1_4758f8f1_p2 --> jss_0_lb_685403e6_p22001
  jss_0_csw1_4758f8f1_p3 --> jss_0_lb_685403e6_p22002
  jss_0_csw1_4758f8f1_p0 --> jss_0_lb_437d2932_p22003
  jss_0_csw1_4758f8f1_p1 --> jss_0_lb_437d2932_p22004
  jss_0_csw2_5b36d8c8_p2 --> jss_0_lb_685403e6_p22101
  jss_0_csw2_5b36d8c8_p3 --> jss_0_lb_685403e6_p22102
  jss_0_csw2_5b36d8c8_p0 --> jss_0_lb_437d2932_p22103
  jss_0_csw2_5b36d8c8_p1 --> jss_0_lb_437d2932_p22104
  jss_0_lb_437d2932_p0 --> jss_0_mgmt_5a86842b_p20021
  jss_0_lb_685403e6_p0 --> jss_0_mgmt_5a86842b_p20020

  classDef wide padding:16px
  class jss_0_mgmt_5a86842b_p20003,jss_0_lb_685403e6_p21003,jss_0_lb_685403e6_p21019,jss_0_lb_437d2932_p21103,jss_0_lb_437d2932_p21119,jss_0_mgmt_5a86842b_p20001,jss_0_lb_685403e6_p21001,jss_0_lb_685403e6_p21017,jss_0_lb_437d2932_p21101,jss_0_lb_437d2932_p21117,jss_0_mgmt_5a86842b_p20005,jss_0_lb_685403e6_p21005,jss_0_lb_685403e6_p21021,jss_0_lb_437d2932_p21105,jss_0_lb_437d2932_p21121,jss_0_mgmt_5a86842b_p20007,jss_0_lb_685403e6_p21007,jss_0_lb_685403e6_p21023,jss_0_lb_437d2932_p21107,jss_0_lb_437d2932_p21123,jss_0_mgmt_5a86842b_p20006,jss_0_lb_685403e6_p21006,jss_0_lb_685403e6_p21022,jss_0_lb_437d2932_p21106,jss_0_lb_437d2932_p21122,jss_0_mgmt_5a86842b_p20002,jss_0_lb_685403e6_p21002,jss_0_lb_685403e6_p21018,jss_0_lb_437d2932_p21102,jss_0_lb_437d2932_p21118,jss_0_mgmt_5a86842b_p20000,jss_0_lb_685403e6_p21000,jss_0_lb_685403e6_p21016,jss_0_lb_437d2932_p21100,jss_0_lb_437d2932_p21116,jss_0_mgmt_5a86842b_p20004,jss_0_lb_685403e6_p21004,jss_0_lb_685403e6_p21020,jss_0_lb_437d2932_p21104,jss_0_lb_437d2932_p21120,jss_0_lb_685403e6_p22001,jss_0_lb_685403e6_p22002,jss_0_lb_437d2932_p22003,jss_0_lb_437d2932_p22004,jss_0_lb_685403e6_p22101,jss_0_lb_685403e6_p22102,jss_0_lb_437d2932_p22103,jss_0_lb_437d2932_p22104,jss_0_mgmt_5a86842b_p20021,jss_0_mgmt_5a86842b_p20020,jss_0_6de98027_p0,jss_0_6de98027_p1,jss_0_6de98027_p2,jss_0_6de98027_p3,jss_0_6de98027_p4,jss_0_7618d0ec_p0,jss_0_7618d0ec_p1,jss_0_7618d0ec_p2,jss_0_7618d0ec_p3,jss_0_7618d0ec_p4,jss_0_427fc39f_p0,jss_0_427fc39f_p1,jss_0_427fc39f_p2,jss_0_427fc39f_p3,jss_0_427fc39f_p4,jss_0_44995b32_p0,jss_0_44995b32_p1,jss_0_44995b32_p2,jss_0_44995b32_p3,jss_0_44995b32_p4,jss_0_lb_685403e6_p0,jss_0_csw2_5b36d8c8_p0,jss_0_csw2_5b36d8c8_p1,jss_0_csw2_5b36d8c8_p2,jss_0_csw2_5b36d8c8_p3,jss_0_72908381_p0,jss_0_72908381_p1,jss_0_72908381_p2,jss_0_72908381_p3,jss_0_72908381_p4,jss_0_712ce0f4_p0,jss_0_712ce0f4_p1,jss_0_712ce0f4_p2,jss_0_712ce0f4_p3,jss_0_712ce0f4_p4,jss_0_csw1_4758f8f1_p0,jss_0_csw1_4758f8f1_p1,jss_0_csw1_4758f8f1_p2,jss_0_csw1_4758f8f1_p3,jss_0_lb_437d2932_p0,jss_0_4e6aa585_p0,jss_0_4e6aa585_p1,jss_0_4e6aa585_p2,jss_0_4e6aa585_p3,jss_0_4e6aa585_p4,jss_0_6a03e784_p0,jss_0_6a03e784_p1,jss_0_6a03e784_p2,jss_0_6a03e784_p3,jss_0_6a03e784_p4 wide
  classDef subgraphTitle font-size:14px
  class jss_0_6de98027,jss_0_7618d0ec,jss_0_427fc39f,jss_0_44995b32,jss_0_lb_685403e6,jss_0_csw2_5b36d8c8,jss_0_72908381,jss_0_712ce0f4,jss_0_csw1_4758f8f1,jss_0_lb_437d2932,jss_0_4e6aa585,jss_0_6a03e784,jss_0_lb_685403e6,jss_0_mgmt_5a86842b,jss_0_lb_437d2932 subgraphTitle
  classDef port_udp fill:#1976d2,stroke:#0d47a1,stroke-width:1px,color:#ffffff
  class jss_0_mgmt_5a86842b_p20003,jss_0_lb_685403e6_p21003,jss_0_lb_685403e6_p21019,jss_0_lb_437d2932_p21103,jss_0_lb_437d2932_p21119,jss_0_mgmt_5a86842b_p20001,jss_0_lb_685403e6_p21001,jss_0_lb_685403e6_p21017,jss_0_lb_437d2932_p21101,jss_0_lb_437d2932_p21117,jss_0_mgmt_5a86842b_p20005,jss_0_lb_685403e6_p21005,jss_0_lb_685403e6_p21021,jss_0_lb_437d2932_p21105,jss_0_lb_437d2932_p21121,jss_0_mgmt_5a86842b_p20007,jss_0_lb_685403e6_p21007,jss_0_lb_685403e6_p21023,jss_0_lb_437d2932_p21107,jss_0_lb_437d2932_p21123,jss_0_mgmt_5a86842b_p20006,jss_0_lb_685403e6_p21006,jss_0_lb_685403e6_p21022,jss_0_lb_437d2932_p21106,jss_0_lb_437d2932_p21122,jss_0_mgmt_5a86842b_p20002,jss_0_lb_685403e6_p21002,jss_0_lb_685403e6_p21018,jss_0_lb_437d2932_p21102,jss_0_lb_437d2932_p21118,jss_0_mgmt_5a86842b_p20000,jss_0_lb_685403e6_p21000,jss_0_lb_685403e6_p21016,jss_0_lb_437d2932_p21100,jss_0_lb_437d2932_p21116,jss_0_mgmt_5a86842b_p20004,jss_0_lb_685403e6_p21004,jss_0_lb_685403e6_p21020,jss_0_lb_437d2932_p21104,jss_0_lb_437d2932_p21120,jss_0_lb_685403e6_p22001,jss_0_lb_685403e6_p22002,jss_0_lb_437d2932_p22003,jss_0_lb_437d2932_p22004,jss_0_lb_685403e6_p22101,jss_0_lb_685403e6_p22102,jss_0_lb_437d2932_p22103,jss_0_lb_437d2932_p22104,jss_0_mgmt_5a86842b_p20021,jss_0_mgmt_5a86842b_p20020,jss_0_6de98027_p0,jss_0_6de98027_p1,jss_0_6de98027_p2,jss_0_6de98027_p3,jss_0_6de98027_p4,jss_0_7618d0ec_p0,jss_0_7618d0ec_p1,jss_0_7618d0ec_p2,jss_0_7618d0ec_p3,jss_0_7618d0ec_p4,jss_0_427fc39f_p0,jss_0_427fc39f_p1,jss_0_427fc39f_p2,jss_0_427fc39f_p3,jss_0_427fc39f_p4,jss_0_44995b32_p0,jss_0_44995b32_p1,jss_0_44995b32_p2,jss_0_44995b32_p3,jss_0_44995b32_p4,jss_0_lb_685403e6_p0,jss_0_csw2_5b36d8c8_p0,jss_0_csw2_5b36d8c8_p1,jss_0_csw2_5b36d8c8_p2,jss_0_csw2_5b36d8c8_p3,jss_0_72908381_p0,jss_0_72908381_p1,jss_0_72908381_p2,jss_0_72908381_p3,jss_0_72908381_p4,jss_0_712ce0f4_p0,jss_0_712ce0f4_p1,jss_0_712ce0f4_p2,jss_0_712ce0f4_p3,jss_0_712ce0f4_p4,jss_0_csw1_4758f8f1_p0,jss_0_csw1_4758f8f1_p1,jss_0_csw1_4758f8f1_p2,jss_0_csw1_4758f8f1_p3,jss_0_lb_437d2932_p0,jss_0_4e6aa585_p0,jss_0_4e6aa585_p1,jss_0_4e6aa585_p2,jss_0_4e6aa585_p3,jss_0_4e6aa585_p4,jss_0_6a03e784_p0,jss_0_6a03e784_p1,jss_0_6a03e784_p2,jss_0_6a03e784_p3,jss_0_6a03e784_p4 port_udp
```
