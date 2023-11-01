from dataclasses import dataclass

from services.base_service import BaseModelService


@dataclass
class InGenre:
    name: str


@dataclass
class OutGenre(InGenre):
    id: int


class GenreService(BaseModelService):
    TABLE_NAME = 'genres'
    IN_MODEL = InGenre
    OUT_MODEL = OutGenre

    @staticmethod
    def get_order_by() -> str:
        return "name"
