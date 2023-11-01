from dataclasses import dataclass

from services.base_service import BaseModelService


@dataclass
class InAuthor:
    full_name: str


@dataclass
class OutAuthor(InAuthor):
    id: int


class AuthorService(BaseModelService):
    TABLE_NAME = 'authors'
    IN_MODEL = InAuthor
    OUT_MODEL = OutAuthor

    @staticmethod
    def get_order_by() -> str:
        return "full_name"
