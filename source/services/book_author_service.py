from dataclasses import dataclass
from services.base_middle_service import BaseMiddleModelService


@dataclass
class InBookAuthor:
    book_id: int
    author_id: int


@dataclass
class OutBookAuthor(InBookAuthor):
    id: int


class BookAuthorService(BaseMiddleModelService):
    TABLE_NAME = 'authors_for_books'
    IN_MODEL = InBookAuthor
    OUT_MODEL = OutBookAuthor
