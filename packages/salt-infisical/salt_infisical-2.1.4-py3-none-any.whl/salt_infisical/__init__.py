# SPDX-FileCopyrightText: 2023-present Jonathan Treffler <mail@jonathan-treffler.de>
#
# SPDX-License-Identifier: MIT


def get_config():
    import logging
    import json

    path = "/etc/salt/infisical_config.json"
    f = open(path, "r")
    config = {}

    try:
        config = json.load(f)
    except:
        logging.exception('Invalid config')
    finally:
        f.close()
        return config

def get_client():
    from infisical_client import ClientSettings, InfisicalClient, AuthenticationOptions, UniversalAuthMethod

    config = get_config()

    return InfisicalClient(
        ClientSettings(
            auth = AuthenticationOptions(
                universal_auth = UniversalAuthMethod(client_id=config["client_id"], client_secret=config["client_secret"])
            )
        )
    )

def fetch_infisical_secrets(
        environment: str = "dev",
        path: str = "/",
        project_id: str = "",
        recursive: bool = False,
    ):
    from infisical_client import ListSecretsOptions

    client = get_client()
    subdirectories = path.strip("/").split("/")

    secrets = {}
    for item in subdirectories[::-1]:
        if not secrets:
            secrets[item] = {secret.secret_key:secret.secret_value for secret in client.listSecrets(options=ListSecretsOptions(
                environment=environment,
                path=path,
                project_id=project_id or get_config()["project_id"],
                recursive=recursive
            ))}
        else:
            tmp = {}
            tmp[item] = secrets.copy()
            secrets = dict(tmp)

    salt = { 'infisical': {} }
    salt["infisical"][environment] = secrets

    return salt

def fetch_infisical_secret(
        secret_name: str,
        environment: str = "dev",
        path: str = "/",
        project_id: str = "",
    ):
    from infisical_client import GetSecretOptions

    client = get_client()
    subdirectories = path.strip("/").split("/")

    secrets = {}
    for item in subdirectories[::-1]:
        if not secrets:
            secrets[item] = client.getSecret(options=GetSecretOptions(
                secret_name=secret_name,
                environment=environment,
                path=path,
                project_id=project_id or get_config()["project_id"]
            )).secret_value
        else:
            tmp = {}
            tmp[item] = secrets.copy()
            secrets = dict(tmp)

    salt = { 'infisical': {} }
    salt["infisical"][environment] = secrets

    return salt
