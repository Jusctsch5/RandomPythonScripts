import logging
import subprocess
import re

logging.basicConfig()


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def init_impi(self):
    """Validate that our methods of locating metrics work."""
    command = ['sudo', 'dmidecode', '-t', '39']
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error("Failed to run dmidecode command: " + " ".join(command))
        return

    command = ['sudo', '/usr/bin/ipmitool', 'sdr', 'type', 'Power Supply']
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        logger.error("Failed to run ipmitool command: " + " ".join(command))
        return

    logger.info("NodeMetrics init successful.")

def update_ipmi(self):
    """Gather dynamic metrics using ipmitool and labels via dmidecode."""

    # Obtain fresh labels
    command = ['sudo', 'dmidecode', '-t', '39']
    logger.info("Gathering PSU info via command: " + " ".join(command))
    result = subprocess.run(command, capture_output=True, text=True)
    result_text = result.stdout

    # System Power Supply
    #    Power Unit Group: 1
    #    Location: PSU1
    #    Name: PWS-706P-1R
    #    Manufacturer: SUPERMICRO
    #    Serial Number: P7061VM08KB4068
    #    Asset Tag: N/A
    #    Model Part Number: PWS-706P-1R
    #    Revision: 2.1
    #    Max Power Capacity: 700 W
    #    Status: Present, OK
    #    Type: Switching
    #    Input Voltage Range Switching: Auto-switch
    #    Plugged: Yes
    #    Hot Replaceable: Yes
    psu_data = []  # List to store dictionaries of PSU info
    psu_blocks = result_text.split("System Power Supply")[1:]
    for psu in psu_blocks:
        logger.debug("PSU block: %s", psu)

        psu_pattern = re.compile(
                r"(?:.*\n)*"  # Skip
                r"\s*Location: (\S+)\n"
                r"\s*Name: ([^\n]+)\n"
                r"\s*Manufacturer: ([^\n]+)\n"
                r"\s*Serial Number: ([^\n]+)\n"
                r"(?:.*\n)*"  # Skip
                r"\s*Model Part Number: ([^\n]+)\n",
                re.MULTILINE
            )

        # Find all PSU blocks in the input text
        matches = psu_pattern.findall(psu)

        # Create a dictionary for each PSU with the captured groups
        for match in matches:
            logger.debug("PSU match: %s", match)
            psu_dict = {
                "location": match[0],
                "name": match[1],
                "manufacturer": match[2],
                "serial_number": match[3],
                "model_part_number": match[4]
            }
            psu_data.append(psu_dict)

    # PS1 Status       | C8h | ok  | 10.88 | Presence detected
    # PS2 Status       | C9h | ok  | 10.87 | Presence detected
    command = ['sudo', '/usr/bin/ipmitool', 'sdr', 'type', 'Power Supply']
    logger.info("Gathering PSU metrics via command: " + " ".join(command))
    result = subprocess.run(command, capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        parts = line.split("|")

        # Rename "PS1 Status" to "PSU1"
        original_psu_name = parts[0].strip()
        match = re.match(r"PS(\d+)\s+Status", original_psu_name)
        if match:
            psu_name = f"PSU{match.group(1)}"
        else:
            psu_name = original_psu_name

        # Parse Voltage
        voltage = float(parts[3].split()[0])
        # Parse Status (OK/Fail)
        status = 1 if "ok" in parts[2].lower() else 0
        # Parse Presence
        present = 1 if "Presence detected" in parts[4] else 0

        # Update labels
        labels = {}
        for psu in psu_data:
            if psu["location"] == psu_name:
                labels = psu

        label_keys = [
            "name",
            "manufacturer",
            "location",
            "serial_number",
            "model_part_number"
        ]
        filtered_labels = {key: labels.get(key, "Unknown") for key in label_keys if key in labels}

        # Update Prometheus metrics
        logger.info("labels: %s", filtered_labels)

        self.voltage_gauge.labels(**filtered_labels).set(voltage)
        self.status_gauge.labels(**filtered_labels).set(status)
        self.presence_gauge.labels(**filtered_labels).set(present)
