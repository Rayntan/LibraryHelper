import dataclasses
import datetime
from dataclasses import dataclass

from services.base_service import BaseModelService
from services.book_genre_service import BookGenreService, InBookGenre, OutBookGenre
from services.genre_service import GenreService, OutGenre
from services.author_service import AuthorService, OutAuthor
from services.book_author_service import BookAuthorService, InBookAuthor, OutBookAuthor
from services.user_book_service import UserBookService


@dataclass
class InBook:
    name: str


@dataclass
class OutBook(InBook):
    id: int
    register_date: datetime.date


class BookService(BaseModelService):
    TABLE_NAME = 'books'
    IN_MODEL = InBook
    OUT_MODEL = OutBook

    @staticmethod
    def get_default_fields() -> dict:
        return dict(register_date=datetime.date.today())

    @staticmethod
    def get_order_by() -> str:
        return "name"

    def get_genres(self, book_id: int):
        bgs = BookGenreService(self.conn)
        return bgs.join(GenreService, 'genre_id', book_id=book_id)

    def add_genre(self, book_id: int, genre_id: int) -> OutBookGenre:
        bgs = BookGenreService(self.conn)
        book_genre = bgs.create(InBookGenre(book_id=book_id, genre_id=genre_id))
        return book_genre

    def remove_genre(self, book_id: int, genre_id: int) -> None:
        bgs = BookGenreService(self.conn)
        bgs.delete(book_id=book_id, genre_id=genre_id)

    def get_authors(self, book_id: int):
        bas = BookAuthorService(self.conn)
        return bas.join(AuthorService, 'author_id', book_id=book_id)

    def add_author(self, book_id: int, author_id: int) -> OutBookAuthor:
        bas = BookAuthorService(self.conn)
        book_author = bas.create(InBookAuthor(book_id=book_id, author_id=author_id))
        return book_author

    def remove_author(self, book_id: int, author_id: int) -> None:
        bas = BookAuthorService(self.conn)
        bas.delete(book_id=book_id, author_id=author_id)

    def get_free_books(self):
        field_names = [field.name for field in dataclasses.fields(self.OUT_MODEL)]
        query = f"""
            select {','.join([f'{field_name}' for field_name in field_names])}\n
            from books
            where id not in (
                select bfu.book_id
                from books_for_users bfu
                where bfu.real_return_date is NULL
            )
            {"order by " + self.get_order_by() if self.get_order_by() else ""}
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
        return [self.OUT_MODEL(*row) for row in rows]

    def get_books_on_user_hands(self, user_id: int):
        field_names = [field.name for field in dataclasses.fields(self.OUT_MODEL)]
        query = f"""
            select {','.join([f'b.{field_name}' for field_name in field_names])}\n
            from books b
            inner join books_for_users bfu
            on b.id = bfu.book_id
            where bfu.real_return_date is NULL and bfu.user_id = {user_id}
            {"order by " + self.get_order_by() if self.get_order_by() else ""}
        """
        with self.conn.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()
        return [self.OUT_MODEL(*row) for row in rows]

    def get_book_place(self, book_id: int):
        query = f"""
            select u.lastname || ' ' || u.firstname || ' ' || u.middlename
            from users u
            inner join books_for_users bfu
            on bfu.user_id = u.id
            where bfu.book_id = {book_id} and bfu.real_return_date is NULL
        """

        with self.conn.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()
        return f"На руках у читателя {row[0]}" if row else "В библиотеке"
