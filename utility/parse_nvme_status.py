#!/usr/bin/python3
import argparse

"""
From: https://nvmexpress.org/wp-content/uploads/NVM-Express-1_4c-2021.06.28-Ratified.pdf

Figure 126: Completion Queue Entry: Status Field
Bits Description
31
Do Not Retry (DNR): If set to ‘1’, indicates that if the same command is re-submitted to any 
controller in the NVM subsystem, then that re-submitted command is expected to fail. If cleared to 
‘0’, indicates that the same command may succeed if retried. If a command is aborted due to time 
limited error recovery (refer to section 5.21.1.5), this bit should be cleared to ‘0’. If the SCT and 
SC fields are cleared to 0h, then this bit should be cleared to ‘0’.
30
More (M): If set to ‘1’, there is more status information for this command as part of the Error 
Information log that may be retrieved with the Get Log Page command. If cleared to ‘0’, there is 
no additional status information for this command. Refer to section 5.14.1.1.
29:28
Command Retry Delay (CRD): If the DNR bit is cleared to ‘0’ and the host has set the Advanced 
Command Retry Enable (ACRE) field to 1h in the Host Behavior Support feature (refer to section 
5.21.1.22), then:
a) a 00b CRD value indicates a command retry delay time of zero (i.e., the host may retry the 
command immediately); and
b) a non-zero CRD value selects a field in the Identify Controller data structure (refer to Figure 
251) that indicates the command retry delay time:
• a 01b CRD value selects the Command Retry Delay Time 1 (CRDT1) field;
• a 10b CRD value selects the Command Retry Delay Time 2 (CRDT2) field; and
• a 11b CRD value selects the Command Retry Delay Time 3 (CRDT3) field.
The host should not retry the command until at least the amount of time indicated by the selected 
field has elapsed. It is not an error for the host to retry the command prior to that time.
If the DNR bit is set to’1’ in the Status field or the ACRE field is cleared to 0h in the Host Behavior 
Support feature, then this field is reserved.
If the SCT and SC fields are cleared to 0h, then this field should be cleared to 00b.
27:25 Status Code Type (SCT): Indicates the status code type of the completion queue entry. This 
indicates the type of status the controller is returning.
NVM ExpressTM Revision 1.4c
79
Figure 126: Completion Queue Entry: Status Field
Bits Description
24:17 Status Code (SC): Indicates a status code identifying any error or sta

"""


class NvmeStatus:
    def __init__(self, do_not_retry, more, command_retry_delay, status_code_type, status_code):
        self.do_not_retry = do_not_retry
        self.more = more
        self.command_retry_delay = command_retry_delay
        self.status_code_type = status_code_type
        self.status_code = status_code

    def print(self):
        print(vars(self))
        print("Status Code Type: ",  end = "")
        if self.status_code_type == 0:
            print("Generatic Command Status")
        elif self.status_code_type == 1:
            print("Command Specific Status")
        elif self.status_code_type == 2:
            print("Media and Data Integrity Errors")
        elif self.status_code_type == 3:
            print("Path Related")
        elif self.status_code_type >= 4 and self.status_code_type <= 6:
            print("Reserved")
        elif self.status_code_type == 7:
            print("Vendor Specific")

        print("Status Code: " + hex(self.status_code) + " - ", end = "")
        if self.status_code == 0x00: print("Successful Completion: The command completed without error.")
        elif self.status_code == 0x01: print("Invalid Command Opcode: A reserved coded value or an unsupported value in the command opcode field.")
        elif self.status_code == 0x02: print("Invalid Field in Command: A reserved coded value or an unsupported value in a defined field (other than the opcode field). This status code should be used unless another status code is explicitly specified for a particular condition. The field may be in the command parameters as part of the Submission Queue Entry or in data structures pointed to by the command parameters.")
        elif self.status_code == 0x03: print("Command ID Conflict: The command identifier is already in use. Note: It is implementation specific how many commands are searched for a conflict.")
        elif self.status_code == 0x04: print("Data Transfer Error: Transferring the data or metadata associated with a command had an error.")
        elif self.status_code == 0x05: print("Commands Aborted due to Power Loss Notification: Indicates that the command was aborted due to a power loss notification.")
        elif self.status_code == 0x06: print("Internal Error: The command was not completed successfully due to an internal error. Details on the internal device error should be reported as an asynchronous event. Refer to Figure 147 for Internal Error Asynchronous Event Information.")
        elif self.status_code == 0x07: print("Command Abort Requested: The command was aborted due to an Abort command being received that specified the Submission Queue Identifier and Command Identifier of this command(refer to section 5.1).")
        elif self.status_code == 0x08: print("Command Aborted due to SQ Deletion: The command was aborted due to a Delete I/O Submission Queue request received for the Submission Queue to which the command was submitted.")
        elif self.status_code == 0x09: print("Command Aborted due to Failed Fused Command: The command was aborted due to the other command in a fused operation failing.")
        elif self.status_code == 0x0A: print("Command Aborted due to Missing Fused Command: The fused command was aborted due to the adjacent submission queue entry not containing a fused command that is the other command in a supported fused operation (refer to section 6.2).")
        elif self.status_code == 0x0B: print("Invalid Namespace or Format: The namespace or the format of that namespace is invalid.")
        elif self.status_code == 0x0C: print("Command Sequence Error: The command was aborted due to a protocol violation in a multicommand sequence (e.g., a violation of the Security Send and Security Receive sequencing rules in the TCG Storage Synchronous Interface Communications protocol (refer to TCG Storage Architecture Core Specification)).")
        elif self.status_code == 0x0D: print("Invalid SGL Segment Descriptor: The command includes an invalid SGL Last Segment or SGL Segment descriptor. This may occur under various conditions, including:• the SGL segment pointed to by an SGL Last Segment descriptor contains an SGL Segment descriptor or an SGL Last Segment descriptor;• an SGL Last Segment descriptor contains an invalid length (i.e., a length of 0h or 1h that is not a multiple of 16); or• an SGL Segment descriptor or an SGL Last Segment descriptor contains an invalid address (e.g., an address that is not qword aligned).")
        elif self.status_code == 0x0E: print("Invalid Number of SGL Descriptors: There is an SGL Last Segment descriptor or an SGL Segment descriptor in a location other than the last descriptor of a segment based on the length indicated. This is also used for invalid SGLs in a command capsule (refer to NVMe over Fabrics specification).")
        elif self.status_code == 0x0F: print("Data SGL Length Invalid: This may occur if the length of a Data SGL is too short. This may occur if the length of a Data SGL is too long and the controller does not support SGL transfers longer than the amount of data to be transferred as indicated in the SGL Support field of the Identify Controller data structure.")
        elif self.status_code == 0x10: print("Metadata SGL Length Invalid: This may occur if the length of a Metadata SGL is too short. This may occur if the length of a Metadata SGL is too long and the controller does not support SGL transfers longer than the amount of data to be transferred as indicated in the SGL Support field of the Identify Controller data structure.")
        elif self.status_code == 0x11: print("SGL Descriptor Type Invalid: The type of an SGL Descriptor is a type that is not supported by the controller, or the combination of type and subtype is not supported by the controller.")
        elif self.status_code == 0x12: print("Invalid Use of Controller Memory Buffer: The attempted use of the Controller Memory Buffer is not supported by the controller. Refer to section 4.7.")
        elif self.status_code == 0x13: print("PRP Offset Invalid: The Offset field for a PRP entry is invalid. This may occur when there is a PRP entry with a non-zero offset after the first entry or when the Offset field in any PRP entry is not dword aligned (i.e., bits 1:0 are not cleared to 00b).")
        elif self.status_code == 0x14: print("Atomic Write Unit Exceeded: The length specified exceeds the atomic write unit size.")
        elif self.status_code == 0x15: print("Operation Denied: The command was denied due to lack of access rights. Refer to the appropriate security specification (e.g., TCG Storage Interface Interactions Specification). For media access commands, the Access Denied status code should be used instead.")
        elif self.status_code == 0x16: print("SGL Offset Invalid: The offset specified in a descriptor is invalid. This may occur when using capsules for data transfers in NVMe over Fabrics implementations and an invalid offset in the capsule is specified.")
        elif self.status_code == 0x17: print("Reserved")
        elif self.status_code == 0x18: print("Host Identifier Inconsistent Format: The NVM subsystem detected the simultaneous use of 64-bit and 128-bit Host Identifier values on different controllers.")
        elif self.status_code == 0x19: print("Keep Alive Timer Expired: The Keep Alive Timer expired.")
        elif self.status_code == 0x1A: print("Keep Alive Timeout Invalid: The Keep Alive Timeout value specified is invalid. This may be due to an attempt to specify a value of 0h on a transport that requires the Keep Alive feature to be enabled. This may be due to the value specified being too large for the associated NVMe Transport as defined in the NVMe Transport binding specification.")
        elif self.status_code == 0x1B: print("Command Aborted due to Preempt and Abort: The command was aborted due to a Reservation Acquire command with the Reservation Acquire Action (RACQA) set to 010b (Preempt and Abort).")
        elif self.status_code == 0x1C: print("Sanitize Failed: The most recent sanitize operation failed and no recovery action has been successfully completed. ")
        elif self.status_code == 0x1D: print("Sanitize In Progress: The requested function (e.g., command) is prohibited while a sanitize operation is in progress. Refer to section 8.15.1.")
        elif self.status_code == 0x1E: print("SGL Data Block Granularity Invalid: The Address alignment or Length granularity for an SGL Data Block descriptor is invalid. This may occur when a controller supports dword granularity only and the lower two bits of the Address or Length are not cleared to 00b. Note: An implementation compliant to revision 1.2.1 or earlier may use the status code value of 15h to indicate SGL Data Block Granularity Invalid.")
        elif self.status_code == 0x1F: print("Command Not Supported for Queue in CMB: The implementation does not support submission of the command to a Submission Queue in the Controller Memory Buffer or command completion to a Completion Queue in the Controller Memory Buffer. Note: Revision 1.3 and later of this specification use this status code only for Sanitize commands.")
        elif self.status_code == 0x20: print("Namespace is Write Protected: The command is prohibited while the namespace is write protected as a result of a change in the namespace write protection state as defined by the Namespace Write Protection State Machine (refer to Figure 493).")
        elif self.status_code == 0x21: print("Command Interrupted: Command processing was interrupted and the controller is unable to successfully complete the command. The host should retry the command. If this status code is returned, then the controller shall clear the Do Not Retry bit to ‘0’ in the Status field of the CQE (refer to Figure 126). The controller shall not return this status code unless the host has set the Advanced Command Retry Enable (ACRE) field to 1h in the Host Behavior Support feature (refer to section 5.21.1.22).")
        elif self.status_code == 0x22: print("Transient Transport Error: A transient transport error was detected. If the command is retried on the same controller, the command is likely to succeed. A command that fails with a transient  transport error four or more times should be treated as a persistent transport error that is not likelyto succeed if retried on the same controller.")
        elif self.status_code >= 0x23 and self.status_code <= 0x7F: print("RESERVED")
        elif self.status_code >= 0x80 and self.status_code <= 0xBF: print("I/O Command Set Specific")
        elif self.status_code >= 0xC0 and self.status_code <= 0xFF: print(" Vendor Specific")            
        else:
            print("Unhandled")

def parse_status(status):
    if status > 0xFFFFFFFF:
        print("status is larger than 32 bits")
        return

    status_object = NvmeStatus(status >> 31 & 0b1,
                               status >> 30 & 0b1,
                               status >> 27 & 0b11,
                               status >> 24 & 0b111,
                               status >> 16 & 0b11111111)
    status_object.print()

def parse_status_field(status):
    if status > 0xFFFF:
        print("status is larger than 16 bits")
        return

    status_object = NvmeStatus(status >> 15 & 0b1,
                               status >> 14 & 0b1,
                               status >> 11 & 0b11,
                               status >>  8 & 0b111,
                               status  & 0b11111111)
    status_object.print()


if __name__ == "__main__":
    descriptionString = "Parses nvme status back"
    parser = argparse.ArgumentParser(description=descriptionString)
    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("--status-word", type=str, help="Status in hex form, ex: 0x11000000")

    # See Figure 92: Completion Queue Entry: Status Field
    group.add_argument("--status-field", type=str, help="Two bytes of status ex: 0x0009")

    args = parser.parse_args()
    if args.status_word:
        status = int(args.status_word, 16)
        parse_status(status)

    if args.status_field:
        status = int(args.status_field, 16)
        parse_status_field(status)