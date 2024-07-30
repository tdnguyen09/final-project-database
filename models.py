# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from config import bcrypt, db
from datetime import datetime

# db = SQLAlchemy()


order_product = db.Table('order_product',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('quantity', db.Integer),
    db.Column('price', db.Integer)
)

wishlist = db.Table('wishlist',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)

# product_category = db.Table('product_category',
#     db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
#     db.Column('category_id', db.Integer, db.ForeignKey('categories.id'), primary_key=True)
# )

class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db. String)
    image = db.Column(db.String)
    price = db.Column(db.Float)
    description = db.Column(db.String)
    product_depth = db.Column(db.Float)
    product_weight = db.Column(db.Float)
    product_height = db.Column(db.Float)
    product_width = db.Column(db.Float)
    discount=db.Column(db.Float)
    is_it_new = db.Column(db.Boolean)
    is_it_clearance = db.Column(db.Boolean)
    is_it_onsale = db.Column(db.Boolean)

    # brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))

    orders = db.relationship('Order', secondary=order_product, back_populates='products')
    user = db.relationship('User', secondary=wishlist, back_populates='products')
    # categories = db.relationship('Category', secondary=product_category, back_populates='products')


    def __repr__(self):
        return f'<Product {self.name} | In Stock: {self.is_in_stock}>'

# class Brand(db.Model, SerializerMixin):
#     __tablename__ = 'brands'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)

#     products = db.relationship('Product', backref='brand')

#     def __repr__(self):
#         return f'<Brand {self.name}>'

# class Category(db.Model, SerializerMixin):
#     __tablename__ = "categories"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.Strinng)

#     products = db.relationship('Product', secondary=product_category, back_populates="categories")

#     def __repr__(self):
#         return f'<Catergory {self.name}>'

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    _password_hash = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    state = db.Column(db.String)
    postcode = db.Column(db.Integer)
    phone_number = db.Column(db.Integer)

    orders = db.relationship('Order', backref='user')
    products = db.relationship('Product', secondary=wishlist, back_populates="user")

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}, ID: {self.id}>'

    @hybrid_property
    def password_hash(self):
        return self._password_hash
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')
    
    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8')
        )

# hash_password => before store or in models

class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    total_items = db.Column(db.Integer)
    total = db.Column(db.Float)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    products = db.relationship('Product', secondary=order_product, back_populates='orders')

    def __repr__(self):
        return f'<Order {self.id}, total: {self.total}>'