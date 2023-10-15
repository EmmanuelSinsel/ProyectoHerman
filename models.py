from pydantic import BaseModel


class Login(BaseModel):
    type: str | None = None
    token: str | None = None
    email: str | None = None
    password: str | None = None


class Where(BaseModel):
    where: str | None = None

class GetBook(BaseModel):
    isbn: str | None = None
    title: str | None = None

class Library(BaseModel):
    name: str | None = None
    address: str | None = None
    phone: str | None = None
    email: str | None = None
    state: str | None = None

    where: str | None = None


class Admin(BaseModel):
    user: str | None = None
    password: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    email: str | None = None
    state: str | None = None
    library_id: str | None = None
    where: str | None = None


class Alumn(BaseModel):
    account_number: str | None = None
    user: str | None = None
    password: str | None = None
    school_group: str | None = None
    carreer: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    email: str | None = None
    last_preference: str | None = None
    state: str | None = None

    where: str | None = None


class Advice(BaseModel):
    id_alumn: str | None = None
    message: str | None = None
    state: str | None = None

    where: str | None = None


class Book(BaseModel):
    tittle: str | None = None
    isbn: str | None = None
    id_category: str | None = None
    id_author: str | None = None
    status: str | None = None
    image: str | None = None
    id_library: str | None = None
    state: str | None = None

    where: str | None = None


class BookNotation(BaseModel):
    id_book: str | None = None
    message: str | None = None
    state: str | None = None

    where: str | None = None


class Favorite(BaseModel):
    id_alumn: str | None = None
    id_book: str | None = None
    state: str | None = None

    where: str | None = None


class Commentary(BaseModel):
    id_alumn: str | None = None
    id_book: str | None = None
    message: str | None = None
    state: str | None = None

    where: str | None = None


class Author(BaseModel):
    name: str | None = None
    state: str | None = None

    where: str | None = None


class Category(BaseModel):
    category: str | None = None
    state: str | None = None

    where: str | None = None


class Transaction(BaseModel):
    id_alumn: str | None = None
    id_book: str | None = None
    date_transaction: str | None = None
    date_deadline: str | None = None
    date_return: str | None = None
    notation: str | None = None
    id_library: str | None = None
    state: str | None = None

    where: str | None = None


class Reserve(BaseModel):
    id_alumn: str | None = None
    id_book: str | None = None
    date_pickup: str | None = None
    id_library: str | None = None
    state: str | None = None

    where: str | None = None