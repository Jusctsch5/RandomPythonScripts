#!/usr/bin/env python3

import os
from kubernetes import client, config

# Load the Kubernetes configuration from the default location (e.g., ~/.kube/config)
config.load_kube_config()

# Define the namespace and secret name
namespace = "myriad"
secret_name = "api-key-secret"

# Create an instance of the Kubernetes API client
api_instance = client.CoreV1Api()

try:
    # Retrieve the secret
    secret = api_instance.read_namespaced_secret(secret_name, namespace)

    # Decode the secret data (assuming it's base64 encoded)
    secret_data = {key.decode(): value.decode() for key, value in secret.data.items()}

    # Print the secret data
    print("Secret Data:")
    for key, value in secret_data.items():
        print(f"{key}: {value}")

except Exception as e:
    print(f"Error retrieving secret: {e}")

