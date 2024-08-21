import cmd2
import argparse

class CRUDShell(cmd2.Cmd):
    def __init__(self, object_schemas):
        super().__init__()
        self.object_schemas = object_schemas

    def do_quit(self, arg):
        """Exit the shell."""
        return True

    @cmd2.with_argparser(argparse.ArgumentParser())
    def do_create(self, arg):
        """Create an object."""
        self._perform_operation("create", arg)

    def do_read(self, arg):
        """Read an object."""
        self._perform_operation("read", arg)

    def do_update(self, arg):
        """Update an object."""
        self._perform_operation("update", arg)

    def do_delete(self, arg):
        """Delete an object."""
        self._perform_operation("delete", arg)

    def _perform_operation(self, operation, arg):
        args = self._parse_args(operation, arg)
        if args is not None:
            # Perform the CRUD operation using the parsed arguments
            print(f"Performing {operation} operation with arguments: {args}")

    def _parse_args(self, operation, arg):
        try:
            schema = self.object_schemas[arg][operation]
            args = input(f"Enter {operation} arguments ({', '.join(schema)}): ").split()
            # Check if all required attributes are provided
            if set(schema) == set(args):
                return args
            else:
                print(f"Error: Required attributes for {operation} operation: {', '.join(schema)}")
                return None
        except KeyError:
            print(f"Error: Object '{arg}' not found in the schema.")
            return None


if __name__ == "__main__":
    # Example schema dictionary
    object_schemas = {
        "orange": {"create": ["color", "taste"], "read": ["color", "taste"], "update": ["color"], "delete": []},
        "apple": {"create": ["color", "taste", "size"], "read": ["color", "taste", "size"], "update": ["size"], "delete": ["color"]}
    }

    # Create and run the cmd2 shell
    shell = CRUDShell(object_schemas)
    shell.cmdloop()
