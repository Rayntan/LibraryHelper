insert into
	genres(name)
values
	('Повесть'),
	('Биография'),
	('Роман'),
	('Ужасы'),
	('Учебная литература');

insert into books(name, register_date)
values('Маленький принц', '2023-09-30');
insert into genres_for_books(genre_id, book_id)
values(1, 1);
insert into authors(full_name)
values('Антуан де Сент-Экзюпери');
insert into authors_for_books(author_id, book_id)
values(1, 1);

insert into books(name, register_date)
values('Двенадцать стульев', '2023-09-30');
insert into genres_for_books(genre_id, book_id)
values(1, 2);
insert into authors(full_name)
values('Илья Ильф');
insert into authors(full_name)
values('Евгений Петров');
insert into authors_for_books(author_id, book_id)
values(2, 2);
insert into authors_for_books(author_id, book_id)
values(3, 2);

insert into books(name, register_date)
values('Поймай меня, если сможешь', '2023-09-30');
insert into genres_for_books(genre_id, book_id)
values(2, 3);
insert into authors(full_name)
values('Фрэнк Абигнейл');
insert into authors(full_name)
values('Стен Реддинг');
insert into authors_for_books(author_id, book_id)
values(4, 3);
insert into authors_for_books(author_id, book_id)
values(5, 3);

insert into books(name, register_date)
values('Над пропастью во ржи', '2023-09-30');
insert into genres_for_books(genre_id, book_id)
values(3, 4);
insert into authors(full_name)
values('Дэвид Селинджер');
insert into authors_for_books(author_id, book_id)
values(6, 4);

insert into books(name, register_date)
values('Коллекционер', '2023-09-30');
insert into genres_for_books(genre_id, book_id)
values(4, 5);
insert into authors(full_name)
values('Джон Фаулз');
insert into authors_for_books(author_id, book_id)
values(7, 5);

insert into books(name, register_date)
values('Война и мир', '2023-09-30');
insert into genres_for_books(genre_id, book_id)
values(1, 6);
insert into authors(full_name)
values('Лев Толстой');
insert into authors_for_books(author_id, book_id)
values(8, 6);

insert into books(name, register_date)
values('Анна Каренина', '2023-09-30');
insert into genres_for_books(genre_id, book_id)
values(3, 7);
insert into authors_for_books(author_id, book_id)
values(8, 7);

insert into books(name, register_date)
values('McDonalds Как создавалась империя', '2023-09-30');
insert into genres_for_books(genre_id, book_id)
values(2, 8);
insert into authors(full_name)
values('Рэй Крок');
insert into authors_for_books(author_id, book_id)
values(9, 8);

insert into books(name, register_date)
values('Богатый папа, бедный папа', '2023-09-30');
insert into genres_for_books(genre_id, book_id)
values(2, 9);
insert into authors(full_name)
values('Роберт Кийосаки');
insert into authors(full_name)
values('Шэрон Лектер');
insert into authors_for_books(author_id, book_id)
values(10, 9);
insert into authors_for_books(author_id, book_id)
values(11, 9);

insert into books(name, register_date)
values('Python для гиков', '2023-09-30');
insert into genres_for_books(genre_id, book_id)
values(5, 10);
insert into authors(full_name)
values('Азиф Мухаммад');
insert into authors_for_books(author_id, book_id)
values(12, 10);

insert into books(name, register_date)
values('Основы тестирования на проникновение', '2023-09-30');
insert into genres_for_books(genre_id, book_id)
values(5, 11);
insert into authors(full_name)
values('Рик Майерс');
insert into authors_for_books(author_id, book_id)
values(13, 10);

insert into
	users(firstname, lastname, middlename, phone, register_date)
values
	('Владислав', 'Власов', 'Андреевич', '+7 (982) 455-72-32', '2023-11-01'),
	('Ирина', 'Кульбеда', 'Викторовна', '+7 (999) 465-45-45', '2023-09-16'),
	('Николай', 'Штин', 'Сергеевич', '+7 (937) 060-01-23', '2023-10-13'),
	('Антонина', 'Высоцкая', 'Васильевна', '+7 (912) 786-45-63', '2023-10-26');

insert into
	books_for_users(user_id, book_id, take_date, expected_return_date, real_return_date)
values
	(1, 1, '2023-09-30', '2023-10-07', NULL),
	(1, 2, '2023-09-30', '2023-10-07', NULL),
	(2, 3, '2023-10-12', '2023-10-19', NULL),
	(3, 4, '2023-10-02', '2023-10-09', '2023-10-26'),
	(3, 5, '2023-10-02', '2023-10-09', '2023-10-25'),
	(4, 6, '2023-10-01', '2023-10-10', '2023-10-14'),
	(4, 10, '2023-10-15', '2023-10-22', '2023-10-30');