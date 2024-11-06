import decimal
from typing import Annotated, Optional
from bson.objectid import ObjectId
from pydantic import BaseModel, Field, BeforeValidator, AfterValidator, field_validator
from bson.decimal128 import Decimal128

def validate_objectId(value):
    if ObjectId.is_valid(value):
        return value
    raise ValueError("Invalid ObjectId")


PyObjectId = Annotated[str, BeforeValidator(str), AfterValidator(validate_objectId)]

class Book(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str
    subject: str
    author: str
    publisher: str
    price: decimal.Decimal


class UpdateBookModel(BaseModel):
    title: Optional[str] = None
    subject: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    price: Optional[decimal.Decimal] = None

