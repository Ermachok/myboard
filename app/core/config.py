from starlette.config import Config

config = Config(".env")

JWT_SECRET = config("JWT_SECRET", default=None)
JWT_ALG = config("JWT_ALG", default="HS256")
JWT_EXP = config("JWT_EXP", cast=int, default=86400)
