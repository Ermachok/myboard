import os
from starlette.config import Config

base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(base_dir, '.env')

config = Config(env_path)

JWT_SECRET = config("JWT_SECRET", default=None)
JWT_ALG = config("JWT_ALG", default="HS256")
JWT_EXP = config("JWT_EXP", cast=int, default=86400)

DATABASE_URL = config("DATABASE_URL")
