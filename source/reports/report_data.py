report_1 = dict(
    title="Сколько книг брал каждый читатель за все время",
    query="""
        select 
            u.lastname || ' ' || u.firstname || ' ' || u.middlename as ФИО, 
            coalesce(gbfu.cnt, 0) as "Количество книг"
        from users u
        left join (
            select bfu.user_id as user_id, count(distinct bfu.book_id) as cnt
            from books_for_users bfu
            group by bfu.user_id
        ) gbfu
        on u.id = gbfu.user_id
        order by ФИО;
    """,
    headings_cells=["ФИО", "Количество книг"]
)

report_2 = dict(
    title="Дата последнего посещения читателем библиотеки",
    query="""
        select 
            u.lastname || ' ' || u.firstname || ' ' || u.middlename as ФИО, 
            coalesce(return_date, take_date, u.register_date) as "Последнее посещение" 
        from users u
        left join (
            select bfu.user_id as user_id, max(real_return_date) as return_date, max(take_date) as take_date
            from books_for_users bfu
            group by bfu.user_id
        ) gbfu
        on u.id = gbfu.user_id
        order by ФИО;
    """,
    headings_cells=["ФИО", "Последнее посещение"]
)

report_3 = dict(
    title="Самый предпочитаемые читателями жанры по убыванию",
    query="""
        select 
            g.name as "Название жанра", coalesce(g_cnt.cnt, 0) as "Количество фактов взятия"
        from genres g
        left join (
            select gfb.genre_id, count(*) as cnt
            from genres_for_books gfb
            inner join books_for_users bfu
            on bfu.book_id = gfb.book_id
            group by gfb.genre_id
        ) g_cnt
        on g.id = g_cnt.genre_id
        order by "Количество фактов взятия" desc;
    """,
    headings_cells=["ФИО", "Количество фактов взятия"]
)

report_4 = dict(
    title="Любимый жанр каждого читателя",
    query="""
        select distinct on(ФИО)
            u.lastname || ' ' || u.firstname || ' ' || u.middlename as ФИО, 
            coalesce(g.name, 'Отсутствует информация') as "Жанр"
        from users u
        left join (
            select bfu.user_id, gfb.genre_id, count(*) as cnt
            from genres_for_books gfb
            inner join books_for_users bfu
            on bfu.book_id = gfb.book_id
            group by bfu.user_id, gfb.genre_id
        ) ugc
        on ugc.user_id = u.id
        left join genres g
        on ugc.genre_id = g.id
        order by ФИО;
    """,
    headings_cells=["ФИО", "Жанр"]
)

report_5 = dict(
    title="Читатели и книги, которые не были возвращены вовремя",
    query="""
        select u.lastname || ' ' || u.firstname || ' ' || u.middlename as ФИО, 
            b.name as Книга
        from books_for_users bfu
        inner join users u
        on bfu.user_id = u.id
        inner join books b
        on bfu.book_id = b.id
        where bfu.real_return_date is NULL or bfu.expected_return_date < bfu.real_return_date
        order by ФИО;
    """,
    headings_cells=["ФИО", "Книга"]
)

report_6 = dict(
    title="Самый читаемый автор",
    query="""
        select a.full_name as Автор, 
            coalesce(ac.cnt, 0) as "Количество фактов взятия его книг"
        from authors a
        left join (
            select afb.author_id, count(*) as cnt
            from authors_for_books afb
            left join books_for_users bfu
            on bfu.book_id = afb.book_id
            group by afb.author_id
        ) ac
        on ac.author_id = a.id
        order by "Количество фактов взятия его книг" desc, Автор;
    """,
    headings_cells=["Автор", "Количество фактов взятия его книг"]
)

report_7 = dict(
    title="Сколько книг сейчас находится на руках у каждого читателя",
    query="""
        select u.lastname || ' ' || u.firstname || ' ' || u.middlename as ФИО, 
            coalesce(uc.cnt, 0) as "Количество книг на руках"
        from users u
        left join (
            select bfu.user_id, count(*) as cnt
            from books_for_users bfu
            where bfu.real_return_date is NULL
            group by bfu.user_id
        )uc
        on uc.user_id = u.id
        order by ФИО;
    """,
    headings_cells=["ФИО", "Количество книг на руках"]
)

report_8 = dict(
    title="Сколько книг есть в библиотеке, сколько читателей",
    query="""
        select
            (select count(*) from users) as "Количество читателей",
            (select count(*) from books) as "Количество книг";
    """,
    headings_cells=["Количество читателей", "Количество книг"]
)
