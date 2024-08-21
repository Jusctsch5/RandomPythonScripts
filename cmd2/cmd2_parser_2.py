import cmd2
import argparse

class CRUDShell(cmd2.Cmd):
    def __init__(self, object_schemas):
        super().__init__()
        self.object_schemas = object_schemas
        self._generate_argparsers()

    def _generate_argparsers(self):
        for obj_name, operations in self.object_schemas.items():
            for operation, attributes in operations.items():
                arg_parser = argparse.ArgumentParser()
                for attr in attributes:
                    arg_parser.add_argument(f"--{attr}", required=True, help=f"{attr} attribute")
                setattr(self, f"{operation}_{obj_name}", cmd2.with_argparser(arg_parser)(self._perform_operation))

    def do_quit(self, arg):
        """Exit the shell."""
        return True

    def _perform_operation(self, args):
        operation, obj_name = args.command.split('_')
        try:
            schema = self.object_schemas[obj_name][operation]
            # Validate required attributes
            for attr in schema:
                if getattr(args, attr) is None:
                    print(f"Error: Attribute '{attr}' is required for {operation} operation.")
                    return
            print(f"Performing {operation} operation for '{obj_name}' with arguments: {args}")

        except KeyError:
            print(f"Error: Object '{obj_name}' not found in the schema.")

if __name__ == "__main__":
    # Example schema dictionary
    object_schemas = {
        "orange": {"create": ["color", "taste"], "read": ["color", "taste"], "update": ["color"], "delete": []},
        "apple": {"create": ["color", "taste", "size"], "read": ["color", "taste", "size"], "update": ["size"], "delete": ["color"]}
    }

    # Create and run the cmd2 shell
    shell = CRUDShell(object_schemas)
    shell.cmdloop()
