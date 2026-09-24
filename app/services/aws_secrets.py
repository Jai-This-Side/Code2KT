import json
import os

import boto3


def load_production_secrets() -> dict[str, str]:
    secret_name = os.getenv("CODE2KT_SECRET_NAME")

    # Local development: use .env instead.
    if not secret_name:
        return {}

    region = os.getenv("AWS_REGION", "us-west-2")

    client = boto3.client(
        "secretsmanager",
        region_name=region,
    )

    response = client.get_secret_value(
        SecretId=secret_name,
    )

    secret_string = response.get("SecretString")

    if not secret_string:
        raise RuntimeError("Secrets Manager returned no SecretString.")

    try:
        secrets = json.loads(secret_string)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            "Code2KT Secrets Manager value is not valid JSON."
        ) from exc

    if not isinstance(secrets, dict):
        raise RuntimeError(
            "Code2KT Secrets Manager value must be a JSON object."
        )

    return {
        str(key): str(value)
        for key, value in secrets.items()
    }