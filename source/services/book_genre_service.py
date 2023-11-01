from dataclasses import dataclass
from services.base_middle_service import BaseMiddleModelService


@dataclass
class InBookGenre:
    book_id: int
    genre_id: int


@dataclass
class OutBookGenre(InBookGenre):
    id: int


class BookGenreService(BaseMiddleModelService):
    TABLE_NAME = 'genres_for_books'
    IN_MODEL = InBookGenre
    OUT_MODEL = OutBookGenre
