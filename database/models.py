from datetime import datetime
from decimal import Decimal
from pony.orm import *

db = Database()


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    tg_id = Required(Decimal, unique=True)
    username = Optional(str, unique=True)
    first_name = Optional(str, nullable=True)
    last_name = Optional(str, nullable=True)
    was_registered = Optional(datetime, default=lambda: datetime.now())
    last_usage = Optional(datetime, default=lambda: datetime.now())
    is_admin = Optional(bool, default=False)

class Product(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    height = Optional(str)
    width = Optional(str)
    depth = Optional(str)
    product_type = Optional(str)
    image = Optional(str)
    glass_type = Required('GlassType')
    color = Required('Color')
    collection = Required('Collection')
    model = Required('Model')
    covering = Required('Covering')

class Model(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    covering = Set('Covering')
    height = Optional(str)
    width = Optional(str)
    depth = Optional(str)
    product_type = Optional(str)
    links = Optional(str, nullable=True)
    collection = Set('Collection')
    product = Set(Product)

class Collection(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    documents = Optional(str, nullable=True)
    videos = Optional(str, nullable=True)
    model = Set(Model)
    product = Set(Product)

class Covering(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    links = Optional(str, nullable=True)
    product = Set(Product)
    model = Set(Model)

class Color(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    products = Set(Product)

class GlassType(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    products = Set(Product)

class Shop(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    phone = Required(str)
    city = Required(str)
    address = Required(str)
    geocode = Required(str)
    time = Optional(str, nullable=True)
    image = Optional(str, nullable=True)

class News(db.Entity):
    id = PrimaryKey(int, auto=True)
    text = Required(str)
    image = Optional(str)



    