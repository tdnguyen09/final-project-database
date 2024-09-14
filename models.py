# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from config import bcrypt, db
from datetime import datetime



wishlist = db.Table('wishlist',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)


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
    is_it_preorder = db.Column(db.Boolean)

    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    order_products = db.relationship('OrderProduct', back_populates='product')
    carts = db.relationship('Cart', back_populates='product')
    user = db.relationship('User', secondary=wishlist, back_populates='products')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'image': self.image,
            'price': self.price,
            'description': self.description,
            'product_depth':self.product_depth,
            'product_weight': self.product_weight,
            'product_height': self.product_height,
            'product_width': self.product_width,
            'discount':self.discount,
            'is_it_new':self.is_it_new,
            'is_it_clearance':self.is_it_clearance,
            'is_it_onsale':self.is_it_onsale,
            'is_it_preorder':self.is_it_preorder,
            'brand': self.brand.brand_name if self.brand else 'No brand assigned',
            'category': self.category.category_name if self.category else 'No category assigned'
        }

    def __repr__(self):
        return f'<Product {self.name}>'

class Brand(db.Model, SerializerMixin):
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    brand_name = db.Column(db.String)

    products = db.relationship('Product', backref='brand')

    def __repr__(self):
        return f'<Brand {self.name}>'

class Category(db.Model, SerializerMixin):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String)

    products = db.relationship('Product', backref='category')

    def __repr__(self):
        return f'<Catergory {self.name}>'
    
    def to_dict(self):
        return {
            'category_name': self.category_name
        }

class User(db.Model,SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    _password_hash = db.Column(db.String, nullable=False)
    address = db.Column(db.String)
    state = db.Column(db.String)
    postcode = db.Column(db.Integer)
    suburb = db.Column(db.String)
    phonenumber = db.Column(db.String)

    orders = db.relationship('Order', backref='user')
    products = db.relationship('Product', secondary=wishlist, back_populates="user")
    carts = db.relationship('Cart', back_populates='user')

    def to_dict(self):
        orders = [
            {
                'id': order.id,
                'total': order.total,
                'order_date': order.order_date.isoformat() if order.order_date else None,
                'products':[
                    {
                        'id':order_product.product.id,
                        'name':order_product.product.name,
                        'quantity':order_product.quantity,
                        'price':order_product.price
                    }
                    for order_product in order.order_products
                ]
            }
            for order in self.orders
        ]
        
        products = [
            {
                'id':product.id,
                'name': product.name,
                'image': product.image,
                'price': product.price,
                'discount':product.discount,
                'is_it_clearance':product.is_it_clearance,
                'is_it_onsale': product.is_it_onsale
            }
            for product in self.products
        ]
        carts = [
            {
                'id':cart.product.id,
                'name': cart.product.name,
                'image': cart.product.image,
                'price': cart.product.price,
                'discount':cart.product.discount,
                'is_is_new':cart.product.is_it_new,
                'is_is_preorder': cart.product.is_it_preorder,
                'is_it_clearance':cart.product.is_it_clearance,
                'is_it_onsale': cart.product.is_it_onsale,
                'quantity': cart.quantity
            }
            for cart in self.carts
        ]
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'address': self.address,
            'state': self.state,
            'postcode': self.postcode,
            'suburb': self.suburb,
            'phonenumber': self.phonenumber,
            'orders': orders,
            'products': products,
            'carts':carts
        }

    def __repr__(self):
        return f'<User {self.firstname} {self.lastname}, ID: {self.id}>'

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


class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    order_products = db.relationship('OrderProduct', back_populates='order')

    def __repr__(self):
        return f'<Order {self.id}, total: {self.total}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total': self.total,
            'order_date': self.order_date.isoformat(),
            'products': [
                {
                    'id': order_product.product.id,
                    'name': order_product.product.name,
                    'price': order_product.price,
                    'quantity': order_product.quantity
                }
                for order_product in self.order_products
            ]
        }

class OrderProduct(db.Model, SerializerMixin):
    __tablename__='order_product'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

    order = db.relationship('Order', back_populates='order_products')
    product = db.relationship('Product', back_populates='order_products')

    def __repr__(self):
        return f'product {product_id} has {quantity} unit(s) in {order_id}'

class Cart(db.Model, SerializerMixin):
    __tablename__ = 'carts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id= db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', back_populates='carts')
    product = db.relationship('Product', back_populates='carts')

    def __repr__(self):
        return f"Product{product_id} is already in user {user_id}'s shopping cart"

    def to_dict(self):
        return {
            'id':self.id,
            'user_id': self.user_id,
            'product': self.product.to_dict() if self.product else None,
            'quantity': self.quantity
        }

# class Rating(db.Model, SerializerMixin):
#     __tablename__='ratings'

#     id = db.Column(db.Integer, primary_key=True)
#     user_id= db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     product_id= db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
#     rating = db.Column(db.Integer, nullable=False)

#     def __repr__(self):
#         return f" Product {product_id}  has {rating} star(s)"

class Admin(db.Model, SerializerMixin):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    _password_hash = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'admin {self.id} has {self.usename}'
    
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

    