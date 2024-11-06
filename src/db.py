import os
from decimal import Decimal

from bson.codec_options import CodecOptions, TypeCodec, TypeRegistry
from bson.decimal128 import Decimal128
import urllib.parse
import motor.motor_asyncio

DB_HOST = "db"
DB_PORT = "5432"
DB_USERNAME = urllib.parse.quote_plus(os.getenv("DB_USERNAME"))
DB_PASSWORD = urllib.parse.quote_plus(os.getenv("DB_PASSWORD"))
DB_NAME = os.getenv("DB_NAME")

# MONGO_DB_URL = f'mongodb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:27017/{DB_NAME}?retryWrites=true&w=majority'
MONGO_DB_URL = f'mongodb://{DB_HOST}:27017/{DB_NAME}?retryWrites=true&w=majority'


class DecimalCodec(TypeCodec):
    python_type = Decimal
    bson_type = Decimal128

    def transform_python(self, value: Decimal) -> Decimal128:
        return Decimal128(value)

    def transform_bson(self, value: Decimal128) -> Decimal:
        return value.to_decimal()

codec_options = CodecOptions(type_registry=TypeRegistry([DecimalCodec()]))

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DB_URL)

db = client.get_database(DB_NAME, codec_options=codec_options)

async def setup_db_conn():
    yield client.get_database(DB_NAME)
