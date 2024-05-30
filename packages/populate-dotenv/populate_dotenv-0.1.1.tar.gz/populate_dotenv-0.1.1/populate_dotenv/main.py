""" Populate the environment variables from the specified key vault. """

import click
from azure.identity import InteractiveBrowserCredential
from azure.keyvault.secrets import SecretClient
from dotenv import dotenv_values


def get_keyvault_client(vault_name: str) -> SecretClient:
    """Get a SecretClient for the specified key vault."""
    keyvault_uri = f"https://{vault_name}.vault.azure.net"
    credential = InteractiveBrowserCredential()
    client = SecretClient(vault_url=keyvault_uri, credential=credential)
    return client


def search_in_keyvault(value: str) -> str | None:
    """Search for a key vault secret in the format 'key_name@vault_name'"""
    try:
        key_name, vault_name = value.split("@")
        client = get_keyvault_client(vault_name)
        key_value = client.get_secret(key_name).value
        return key_value
    except ValueError:
        return value


def populate_dotenv(filename: str = ".env.example") -> None:
    """Populate the environment variables from the specified key vault."""
    current_values = dotenv_values(filename)
    populated_values = {
        key: search_in_keyvault(value) for key, value in current_values.items()
    }
    with open(".env", "w", encoding="utf8") as new_file:
        for key, value in populated_values.items():
            new_file.write(f"{key}={value}\n")


@click.command()
@click.argument("filename", type=click.Path(exists=True), required=False)
def populate(filename=".env.example"):
    """Populate the environment variables from the specified key vault."""
    populate_dotenv(filename)
