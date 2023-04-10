import json
import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publishers"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.Text, unique=True)

class Shop(Base):
    __tablename__ = "shops"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.Text, unique=True)

    def __str__(self):
        return f'{self.id}: {self.name}'

class Book(Base):
    __tablename__ = "books"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.Text, nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publishers.id"), nullable=False)

    publisher = relationship(Publisher, backref="books")

class Stock(Base):
    __tablename__ = "stocks"

    id = sq.Column(sq.Integer, primary_key=True)
    count = sq.Column(sq.Integer, nullable=False, default=0)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("books.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shops.id"), nullable=False)

    book = relationship(Book, backref="stocks")
    shop = relationship(Shop, backref="stocks")

class Sale(Base):
    __tablename__ = "sales"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.DECIMAL, nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    count = sq.Column(sq.Integer, nullable=False, default=1)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stocks.id"), nullable=False)

    stock = relationship(Stock, backref="sales")
def create_tables(engine):
    # Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

DSN = 'postgresql://postgres:postgres@localhost:5432/book_store_db'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('fixtures/tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()

#запрос
subq = session.query(Publisher).join(Book.publisher).filter(Publisher.id ==
int(input("Введите идентификатор издателя: ")))
q = session.query(Stock).join(subq, Book.id == subq.c.book_id)
print(q)
# как сюда еще впендюрить Sale, чтобы и цена с датой выводились?