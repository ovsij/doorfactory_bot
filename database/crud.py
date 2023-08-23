from datetime import datetime
import pandas as pd

from database.db import *


# User
@db_session
def register_user(telegram_user):
    if not User.exists(tg_id = telegram_user.id):
        user = User(
            tg_id=telegram_user.id, 
            username=telegram_user.username, 
            first_name=telegram_user.first_name, 
            last_name=telegram_user.last_name)
        flush()
        return user
    else:
        print(f'User {telegram_user.id} exists')

@db_session
def get_user(tg_id : str = None, username : str = None):
    if tg_id:
        return User.get(tg_id=tg_id)
    if username:
        return User.get(username=username)
    else:
        return select(u for u in User)[:]

@db_session
def get_users():
    return select(int(u.tg_id) for u in User)[:]
        
@db_session()
def update_user(
    tg_id : int = None, 
    id : int = None,
    username : str = None,
    first_name : str = None,
    last_name : str = None,
    last_usage : bool = None,
    is_admin : bool = None
    ):
    if tg_id:
        user_to_update = User.get(tg_id = tg_id)
    if id:
        user_to_update = User[id]
    if username:
        user_to_update.username = username
    if first_name:
        user_to_update.first_name = first_name
    if last_name:
        user_to_update.last_name = last_name
    if is_admin:
        user_to_update.is_admin = is_admin
    if is_admin == False:
        user_to_update.is_admin = is_admin
    if last_usage:
        user_to_update.last_usage = datetime.now()

# Product
@db_session
def create_product(
    name : str,
    collection: Collection,
    model: Model,
    covering: Covering,
    height: str = None,
    width: str = None,
    depth: str = None,
    product_type: str = None,
    glass_type: GlassType = None,
    color : Color = None,
    image: str = None,
    ):
    Product(
        name=name,
        height=height,
        width=width,
        depth=depth,
        product_type=product_type,
        glass_type=glass_type,
        color=color,
        image=image,
        collection=collection,
        model=model,
        covering=covering,
    )

@db_session
def get_product(id : int = None, name : str = None, model : int = None, collection : int = None, covering : int = None, color : int = None, glass_type : int = None):
    if id:
        return Product[id]
    elif name:
        return Product.get(name=name)
    elif model and not color and not glass_type and not covering:
        return select(p for p in Product if p.model == Model[model])[:]
    elif model and color and not glass_type and not covering:
        return select(p for p in Product if p.model == Model[model] and p.color == Color[color])[:]
    elif model and color and glass_type and not covering:
        return select(p for p in Product if p.model == Model[model] and p.color == Color[color] and p.glass_type == GlassType[glass_type])[:]
    elif collection:
        return select(p for p in Product if p.collection == Collection[collection])[:]
    elif covering and not model:
        return select(p for p in Product if p.covering == Covering[covering])[:]
    elif model and covering and not color:
        return select(p for p in Product if p.covering == Covering[covering] and p.model == Model[model])[:]
    elif model and covering and color:
        return select(p for p in Product if p.covering == Covering[covering] and p.model == Model[model] and p.color == Color[color])[:]
@db_session
def update_product(id : int, name : str):
    if id:
        product_to_update = Product[id]
    else:
        product_to_update = Product.get(name=name)
    

@db_session
def delete_product(name : str):
    if id:
        product_to_delete = Product[id]
    else:
        product_to_delete = Product.get(name=name)
    return product_to_delete.delete()

@db_session
def product_exists(name : str):
    return Product.exists(name=name)

# Collection
@db_session
def create_collection(name : str):
    return Collection(name=name)

@db_session
def get_collection(id : int = None, name : str = None, covering : int = None):
    if id:
        return Collection[id]
    elif name:
        return Collection.get(name=name)
    elif covering:
        return select(c for c in Collection if covering in (prod.covering.id for prod in c.product))[:]
    else:
        return select(c for c in Collection)[:]

@db_session
def update_collection(id : int, name : str):
    if id:
        collection_to_update = Collection[id]
    else:
        collection_to_update = Collection.get(name=name)
    
@db_session
def delete_collection(name : str):
    if id:
        collection_to_delete = Collection[id]
    else:
        collection_to_delete = Collection.get(name=name)
    return collection_to_delete.delete()

@db_session
def collection_exists(name : str):
    return Collection.exists(name=name)

# Model
@db_session
def create_model(name : str):
    return Model(name=name)

@db_session
def get_model(id : int = None, name : str = None, collection : int = None, covering : int = None):
    if id:
        return Model[id]
    if name:
        return Model.get(name=name)
    if covering and collection:
        return select(m for m in Model if Collection[collection] in m.collection and covering in (prod.covering.id for prod in m.product))[:]
    #if covering:
    #    return select(m for m in Model if m.covering == Covering[covering])[:]
    else:
        return select(m for m in Model)[:]
    

@db_session
def update_model(id : int, name : str):
    if id:
        model_to_update = Model[id]
    else:
        model_to_update = Model.get(name=name)
    
@db_session
def delete_model(name : str):
    if id:
        model_to_delete = Model[id]
    else:
        model_to_delete = Model.get(name=name)
    return model_to_delete.delete()

@db_session
def model_exists(name : str):
    return Model.exists(name=name)

# Covering
@db_session
def create_covering(name : str):
    return Covering(name=name)

@db_session
def get_covering(id : int = None, name : str = None):
    if id:
        return Covering[id]
    elif name:
        return Covering.get(name=name)
    else:
        return select(c for c in Covering)[:]

@db_session
def update_covering(id : int, name : str):
    if id:
        covering_to_update = Covering[id]
    else:
        covering_to_update = Covering.get(name=name)
    
@db_session
def delete_covering(name : str):
    if id:
        covering_to_delete = Covering[id]
    else:
        covering_to_delete = Covering.get(name=name)
    return covering_to_delete.delete()

@db_session
def covering_exists(name : str):
    return Covering.exists(name=name)

# Color
@db_session
def get_color(id : int = None, model_id : int = None, covering_id : int = None):
    if id:
        return Color[id]
    elif model_id and not covering_id:
        return list(set([p.color for p in get_product(model=model_id)]))
    elif model_id and covering_id:
        return list(set([p.color for p in get_product(model=model_id, covering=covering_id)]))


@db_session
def get_glasstype(id : int = None, model_id : int = None, color_id : int = None, covering_id : int = None, collection_id : int = None):
    if id:
        return GlassType[id]
    if model_id and not covering_id and not collection_id:
        return list(set([p.glass_type for p in get_product(model=model_id, color=color_id)]))
    if model_id and covering_id and not collection_id:
        return list(set([p.glass_type for p in get_product(model=model_id, covering=covering_id, color=color_id)]))
    if model_id and collection_id:
        return list(set([p.glass_type for p in get_product(model=model_id, collection=collection_id)]))

@db_session
def get_shop(city : str = None):
    if city:
        return select(s for s in Shop if s.city == city)[:]
    else:
        return select(s for s in Shop)[:]


# Covering
@db_session
def create_news(text : str):
    return News(text=text)

@db_session
def get_news(id : int = None):
    if id:
        return News[id]
    else:
        return News.select().order_by(desc(News.id))[:]

@db_session
def update_news(id : int, image : str):
    news_to_update = News[id]
    news_to_update.image = image
    
@db_session
def delete_news(id : int):
    if id:
        news_to_delete = News[id]
    
    return news_to_delete.delete()


@db_session
def fill_db():
    df = pd.read_csv('database/catalogdip.csv')#, sep=';', encoding='windows-1251')
    for i in range(len(df)):
        try:
            if collection_exists(name=str(df.iloc[i]['Коллекция'])):
                collection = Collection.get(name=df.iloc[i]['Коллекция'])
            else:
                collection = Collection(name=df.iloc[i]['Коллекция'])
            #print('1')
            if covering_exists(name=df.iloc[i]['Тип покрытия']):
                covering = Covering.get(name=df.iloc[i]['Тип покрытия'])
            else:
                covering = Covering(name=df.iloc[i]['Тип покрытия'])
            #print('2')
            if model_exists(name=df.iloc[i]['Модель']):
                model = Model.get(name=df.iloc[i]['Модель'])
                model.collection += collection
            else:
                model = Model(
                    name=df.iloc[i]['Модель'],
                    collection = collection,
                    covering=covering,
                    height = str(df.iloc[i]['Высота']),
                    width = str(df.iloc[i]['Ширина']),
                    depth = str(df.iloc[i]['Толщина']),
                    product_type = str(df.iloc[i]['Тип продукта'])
                )
            #print('3')
            if Color.exists(name=df.iloc[i]['Цвет']):
                color = Color.get(name=df.iloc[i]['Цвет'])
            else:
                if df.iloc[i]['Цвет'] == 'Белый кипарис old':
                    continue
                color = Color(name=df.iloc[i]['Цвет'])
            #print('4')
            if GlassType.exists(name=df.iloc[i]['Тип остекления']):
                glassType = GlassType.get(name=df.iloc[i]['Тип остекления'])
            else:
                glassType = GlassType(name=df.iloc[i]['Тип остекления'])
            #print('5')
            create_product(
                name = df.iloc[i]['Наименование'],
                collection = collection,
                model = model,
                covering = covering,
                height = str(df.iloc[i]['Высота']),
                width = str(df.iloc[i]['Ширина']),
                depth = str(df.iloc[i]['Толщина']),
                product_type = str(df.iloc[i]['Тип продукта']),
                glass_type = glassType,
                color = color,
                image = 'database/images/' + df.iloc[i]['ФайлФото'],
                )
            #print('OK')
        except:
            print('error')
            pass

@db_session
def add_shops():
    import numpy as np
    df = pd.read_csv('database/shops.csv')
    print(len(df))
    for i in range(len(df)):
        image = 'https://alberodoors.com' + str(df.iloc[i]['IE_DETAIL_PICTURE']) if df.iloc[i]['IE_DETAIL_PICTURE'] != np.NaN else None
        if not Shop.exists(geocode=str(df.iloc[i]['IP_PROP27'])):    
            shop = Shop(
                name=df.iloc[i]['IE_NAME'],
                phone=str(df.iloc[i]['IP_PROP26']).replace('.0', ''),
                city=str(df.iloc[i]['City']),
                address=df.iloc[i]['IP_PROP25'],
                geocode=str(df.iloc[i]['IP_PROP27']),
                time=str(df.iloc[i]['IP_PROP240']),
                image=image,
            )
            commit()
            if shop.image == 'https://alberodoors.comnan':
                shop.image = None
        else:
            print(i)