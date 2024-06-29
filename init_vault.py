import hvac
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--token", default="none")
parser.add_argument("--port", default=5000)
parser.add_argument("--vault_addr", default="none")
parser.add_argument(
    "--hf_token",
)
parser.add_argument(
    "--prod_host"
)

namespace = parser.parse_args()


client = hvac.Client(
         url=namespace.vault_addr,
         token=namespace.token,
     )

print("AUTH: ", client.is_authenticated())


create_response = client.secrets.kv.v2.create_or_update_secret(
         path='server',
         secret=dict(PASS='test',
                     HOST='host.docker.internal',
                     PORT=namespace.port,
                     PROD_HOST=namespace.prod_host,
                     VAULT_ADDR=namespace.vault_addr),
)