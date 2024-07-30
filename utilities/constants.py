from urllib.parse import quote
POSTGRES_DB_USERNAME = "postgres"
POSTGRES_DB_PSWD = "root"
encoded_password = quote(POSTGRES_DB_PSWD, safe="")
POSTGRES_DB_NAME = "stargleam"
POSTGRES_DATABASE_URL = f"postgresql://{POSTGRES_DB_USERNAME}:{encoded_password}@localhost/{POSTGRES_DB_NAME}"
# POSTGRES_DATABASE_URL = (
#     f"postgresql://maang:{encoded_password}@178.16.139.18:5432/clients_dev_sge"
# )
