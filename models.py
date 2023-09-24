from pydantic import BaseModel

class Library(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class Admin(BaseModel):
    user: str | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    email: str | None = None
    state: str | None = None

    where: str  | None = None

class Alumn(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class Advice(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class Book(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class Book_Notation(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class Favorite(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class Commentary(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class Author(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class Category(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class Transaction(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class Reserve(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None