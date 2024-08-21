#!/usr/bin/python3

import uuid
import hashlib

def generate_uuid_from_string(name):
    hash_object = hashlib.md5(name.encode())
    hash_hex = hash_object.hexdigest()
    return uuid.UUID(hash_hex)

name = "leaf-1"
uuid_from_name = generate_uuid_from_string(name)
print(uuid_from_name)

name = "leaf-2"
uuid_from_name = generate_uuid_from_string(name)
print(uuid_from_name)
