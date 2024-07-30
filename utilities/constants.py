import os
from urllib.parse import quote

# STRIPE_API_KEY = "sk_test_51OHqk3SHsktzQ2xvjbaY44fk9wwLjfxIenRa88CGcEonHotJoLzvSEeC1Mg6M4V7vgSPj9RCvKQOPXj4rgnIIS5C00h2qwflbA"
STRIPE_API_KEY = "sk_test_51PE8c5SHFr7V01sFT0mI5ARfZyAtk3Ku9bDHn6oj4dgBbPUSPIlU8JByIkQz4MWciZ25qH7iYTKlW40DwIkh3lcY00FhS882lJ"
GOOGLE_CLIENT_ID="342487029539-9amlsnhpp3e24grhpouju8vnl1taooei.apps.googleusercontent.com"
ALLOWED_DOMAINS = [
    "*",
    "maangtechnologies.com",
    "gmail.com"
]
JWT_ENCODING_ALGORITHM = 'HS256'
JWT_EXPIRY_WINDOW_IN_HOURS = 24
#JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_SECRET_KEY = "MhvR7A0r9MObSekgMqvDH84rr1wAQtD/w5tZNYF2t98="


POSTGRES_DB_PSWD = 'maang@123'
encoded_password = quote(POSTGRES_DB_PSWD, safe='')
POSTGRES_DB_URL = 'postgres_db_url'
POSTGRES_DB_USERNAME = 'postgres_db_username'
POSTGRES_DB_NAME = 'postgres_db_name'

POSTGRES_DATABASE_URL = f'postgresql://maang:{encoded_password}@178.16.139.18:5432/clients_sge_staging'

PREFIX_URL = ""
