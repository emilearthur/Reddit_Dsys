"""Settting up configs."""

from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

PROJECT_NAME = "Reddit_Dsys"
VERSION = "0.0.1"
API_PREFIX = "/api"

# SECRET_KEY = config("SECRET_KEY", cast=Secret)

# ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=7 * 24 * 60)

# JWT_ALGORITHM = config("JWT_ALGORITHM", cast=str, default="HS256")
# JWT_AUDIENCE = config("JWT_AUDIENCE", cast=str, default="occupy_todo:auth")
# JWT_TOKEN_PREFIX = config("JWT_TOKEN_PREFIX", cast=str, default="Bearer")

POSTGRES_USER = config("POSTGRES_USER", cast=str)
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=Secret)
POSTGRES_SERVER = config("POSTGRES_SERVER", cast=str, default="db")
POSTGRES_PORT = config("POSTGRES_PORT", cast=str, default="5432")
POSTGRES_DB = config("POSTGRES_DB", cast=str)

DATABASE_URL = config(
    "DATABASE_URL",
    cast=DatabaseURL,
    default=f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}",
)

# REDIS_HOST = config("REDIS_HOST", cast=str, default="redis")
# REDIS_PASSWORD = config("REDIS_PASSWORD", cast=Secret)
# REDIS_PORT = config("REDIS_PORT", cast=str, default="6379")
# REDIS_URL = config("REDIS_URL", cast=str, default=f"redis://{REDIS_HOST}")

RABBITMQ_DEFAULT_USER = config("RABBITMQ_USER", cast=str, default="rabbitmq")
RABBITMQ_DEFAULT_PASS = config("RABBITMQ_PASSWORD", cast=Secret)
RABBITMQ_USER = config("RABBITMQ_USER", cast=str, default="rabbitmq")
RABBITMQ_PASSWORD = config("RABBITMQ_PASSWORD", cast=Secret)
RABBITMQ_NODENAME = config("RABBITMQ_NODENAME", cast=str, default="rabbitnode@localhost")
RABBITMQ_PORT1 = config("RABBITMQ_PORT1", cast=str, default="5672")
RABBITMQ_PORT2 = config("RABBITMQ_PORT2", cast=str, default="15672")
RABBITMQ_HOST = config("RABBITMQ_DEFAULT_VHOST", cast=str, default="vhost")
RABBITMQ_URL = config("RABBITMQ_URL", cast=str,
                      default=f"amqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT2}")
# EMAIL_ADDR = config("EMAIL", cast=str)
# EMAIL_PWD = config("EMAIL_PWD", cast=str)
# EMAIL_USERNAME = config("EMAIL_USERNAME", cast=str, default="EMILEX TRIG")



