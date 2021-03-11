from sqlalchemy import MetaData, Table, Integer, Column, String, DateTime, Boolean, ForeignKeyConstraint, \
    PrimaryKeyConstraint, UniqueConstraint


def mock_book_author_publisher() -> MetaData:
    meta = MetaData()
    Table(
        'book',
        meta,
        Column('publisher_name', String),
        Column('author_first_name', String),
        Column('author_last_name', String),
        Column('title', String),
        Column('edition', Integer, nullable=True),
        Column('date_released', DateTime, nullable=True),
        Column('number_of_pages', Integer, nullable=True),
        Column('ebook_available', Boolean),
        PrimaryKeyConstraint('publisher_name', 'title', 'edition', name='pk_book'),
        UniqueConstraint(
            'author_first_name', 'author_last_name', 'title', 'edition',
            name='ix_book_author_title_edition'
        ),
        ForeignKeyConstraint(
            ('publisher_name',),
            ('publisher.company_name',),
            name='fk_book_publisher'
        ),
        ForeignKeyConstraint(
            ('author_first_name', 'author_last_name'),
            ('author.first_name', 'author.last_name'),
            name='fk_book_author'
        )
    )
    Table(
        'author',
        meta,
        Column('first_name', String),
        Column('last_name', String),
        Column('date_of_birth', DateTime),
        Column('home_country', String),
        Column('home_city', String),
        PrimaryKeyConstraint('first_name', 'last_name', name='pk_author'),
        ForeignKeyConstraint(
            ('home_country', 'home_city'),
            ('place.country', 'place.city'),
            name='fk_author_place'
        )
    )
    Table(
        'publisher',
        meta,
        Column('company_name', String),
        Column('parent_company', String, nullable=True),
        Column('is_public_company', Boolean),
        PrimaryKeyConstraint('company_name', name='pk_publisher'),
        ForeignKeyConstraint(
            ('parent_company',),
            ('publisher.company_name',),
            name='fk_publisher_parent'
        )
    )
    Table(
        'book_purchase',
        meta,
        Column('id', Integer, primary_key=True),
        Column('publisher_name', String),
        Column('title', String),
        Column('edition', Integer, nullable=True),
        Column('place_country', String),
        Column('place_city', String),
        Column('quantity', Integer),
        ForeignKeyConstraint(
            ('publisher_name', 'title', 'edition'),
            ('book.publisher_name', 'book.title', 'book.edition'),
            name='fk_book_purchase_book'
        ),
        ForeignKeyConstraint(
            ('place_country', 'place_city'),
            ('place.country', 'place.city'),
            name='fk_book_purchase_place'
        )
    )
    Table(
        'place',
        meta,
        Column('country', String),
        Column('city', String),
        PrimaryKeyConstraint('country', 'city', name='pk_place')
    )
    return meta
