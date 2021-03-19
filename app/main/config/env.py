import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

JWT_EXPIRATION_TIME = int(os.getenv("JWT_EXPIRATION_TIME"))

ENVIRONMENT = "prod"
