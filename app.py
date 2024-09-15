#!/usr/bin/env python3

import os

from flask import Flask, jsonify, request, make_response, session
from flask_restful import Resource
from config import db, api, app
from models import Product, User, Admin, Order, OrderProduct, wishlist, Brand, Category, Cart
import stripe

# app.permanent_session_lifetime = timedelta(minutes=5)
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

# done
class Products(Resource):
    def get(self):
        products = [product.to_dict() for product in Product.query.all()]
        return make_response(jsonify(products), 200)
api.add_resource(Products, '/products')
# done
class ProductByID(Resource):
    def get(self, id):
        product = Product.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(product), 201)

    def post(self, id):
        user_id = request.get_json()
        # user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        product = Product.query.filter_by(id=id).first()

        if not user or not product:
            return make_response(jsonify({'error':'Invalid data'}), 400)

        if user and product:
            if product in user.products:
                return make_response(jsonify({'message': 'product already in the wishlist'}),400)
            else:
                user.products.append(product)
                db.session.commit()
                return make_response(jsonify({'message':f'{product.name} added to wishlist successfully'}), 201)
        else:
            return make_response(jsonify({'error': 'User or product not found'}), 404)
        

    def patch(self,id):
        data = request.get_json()
        product = Product.query.filter_by(id=id).first()
        for key,value in data.items():
            if key == 'category':
                category = Category.query.filter_by(category_name=value).first()
                if not category:
                    category = Category(category_name = value)
                    db.session.add(category)
                    db.session.commit()
                setattr(product, 'category_id', category.id)
            elif key == 'brand':
                brand = Brand.query.filter_by(brand_name = value).first()
                if not brand:
                    brand = Brand(brand_name = value)
                    db.session.add(brand)
                    db.session.commit()
                setattr(product, 'brand_id', brand.id)
            else:
                if hasattr(product, key):
                    setattr(product, key, value)

        db.session.merge(product)
        db.session.commit()

        response_dict = product.to_dict()
        return make_response(response_dict, 200)

    def delete(self, id):
        user_id = request.get_json()
        user = User.query.filter(User.id == user_id).first()
        product = Product.query.filter_by(id=id).first()
        
        if product and user:
            user.products.remove(product)
            db.session.commit()
            return make_response(jsonify({'message':'remove from successfully'}), 200)
        else:
            return make_response(jsonify({'error':'product not found'}), 404)
api.add_resource(ProductByID, '/products/<int:id>')
# class CartRetrive(Resource):
#     def get(self):
#         user_id= request.args.get('userID')
        
#         cart_items= Cart.query.filter_by(user_id=user_id).all()
#         if not cart_items:
#             return make_response(jsonify({'error':'No cart items found'}))
        
#         cart_items_dict = [item.to_dict() for item in cart_items]
        
#         return make_response(jsonify(cart_items_dict),200)
# api.add_resource(CartRetrive, '/checkcart')
class AddToCart(Resource):
    def post(self, id):
        data = request.get_json()
        user_id = data.get('userLoginID')
        quantity = data.get('quantity')

        user = User.query.filter_by(id=user_id).first()
        product= Product.query.filter_by(id=id).first()
        if not product or not user:
            return make_response(jsonify({'message':'Invalid data'}),400)

        cart_item = Cart.query.filter_by(user_id=user_id, product_id=id).first()
        if cart_item:
            cart_item.quantity=quantity
        else:
            cart_item = Cart(
                user_id=user_id,
                product_id=id,
                quantity=quantity
            )
            db.session.add(cart_item)
        db.session.commit()
        return make_response(jsonify({'message': f'{product.name} is added successfully to cart'}),200)

    # def patch(self, id):
    #     data = request.get_json()
    #     user_id = data.get('user_id')
    #     new_quantity = data.get('quantity')

    #     user = User.query.filter_by(id=user_id).first()
    #     product= Product.query.filter_by(id=id).first()
    #     if not product or not user:
    #         return make_response(jsonify({'message':'Invalid data'}),400)

    #     cart_item = Cart.query.filter_by(user_id=user_id, product_id=id).first()
    #     if not cart_item:
    #         return make_response(jsonify({'error':'item not found'}),404)

    #     cart_item.quantity = new_quantity
    #     db.session.commit()
        
    #     # for attr, value in data.item():
    #     #     if hasattr(cart_item, attr):
    #     #         setattr(cart_item, attr, value)
    #     # db.session.merge(cart_item)
    #     db.session.commit() 

    #     return make_response(jsonify({'message': 'Cart quantity updated successfully'}), 200)
        
    def delete(self, id):
        user_id = request.get_json()
        
        user = User.query.filter_by(id=user_id).first()
        product= Product.query.filter_by(id=id).first()

        if not user or not product:
            return make_response(jsonify({'error':'invalid data'}),404)
        
        cart_item = Cart.query.filter_by(user_id=user_id, product_id=id).first()
        if not cart_item:
            return make_response(jsonify({'error':'item not found'}),404)
        
        db.session.delete(cart_item)
        db.session.commit()
        return make_response(jsonify({'message':'Product removed from cart successfully'}),200)
api.add_resource(AddToCart, '/products/<int:id>/cart')
#done

class Categories(Resource):
    def get(self):
        categories = [category.to_dict() for category in Category.query.all()]
        return make_response(jsonify(categories), 200)
api.add_resource(Categories, '/categories')

class Hello(Resource):
    def get(seelf):
        print('hello world')
        return 'Hello World'
api.add_resource(Hello, '/')

class Login(Resource):
    def post(self):

        email = request.get_json()['email']
        user = User.query.filter(User.email == email).first()

        password = request.get_json()['password']

        if user and user.authenticate(password):
            session['user_id'] = user.id
            session.permanent = True
            return user.to_dict(), 200

        return make_response(jsonify({'error':'Invalid email or password'}), 401)
api.add_resource(Login, '/login')

class GetSession(Resource):
    def get(self):
        user_id = session.get('user_id', 'Not set')
        session.permanent = True  
        return jsonify({'user_id': user_id})  
api.add_resource(GetSession,'/getsession')

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id is None:
            return {'message':'401: Not Authorized'}, 401
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            return user.to_dict()
        else:
            return {'message':'401: Not Authorized'}, 401
api.add_resource(CheckSession, '/checksession')

class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {'message': '204: No Content'}, 204
api.add_resource(Logout, '/logout')

class UserUpdate(Resource):
    def patch(self):
        data = request.get_json()
        # user = User.query.filter(User.id == session.get('user_id')).first()
        user = User.query.filter(User.id == data.get('id')).first()
        if user is None:
            return make_response(jsonify({'message':'user not found'}), 400)
        else:
            for attr, value in data.items():
                if hasattr(user, attr):
                    if attr in ['orders', 'products']:
                        continue
                    setattr(user, attr, value)
            db.session.merge(user)
            db.session.commit()

        response_dict = user.to_dict()
        return make_response(response_dict, 200)
        # return make_response(user)
api.add_resource(UserUpdate, '/update-detail')
#done
class Signup(Resource):
    def post(self):

        firstname = request.get_json()['firstname']
        lastname = request.get_json()['lastname']
        email = request.get_json()['email']
        password = request.get_json()['password']
        address =request.get_json()['address']
        state = request.get_json()['state']
        postcode = request.get_json()['postcode']
        phonenumber = request.get_json()['phone']
        suburb = request.get_json()['suburb']

        if not firstname or not lastname or not email or not password:
            return jsonify({'message':'All fields are required'}), 400
        
        user = User.query.filter(User.email == email).first()
        if user:
            return make_response(jsonify({'message':'Email already registed'}), 400)
        
        new_user = User(
            firstname=firstname, 
            lastname=lastname,
            email=email,
            address=address,
            state=state,
            postcode=postcode,
            suburb=suburb,
            phonenumber=phonenumber)
        new_user.password_hash = password

        db.session.add(new_user)
        db.session.commit()
       
        session['user_id']=new_user.id

        new_user_dict = new_user.to_dict()

        return make_response(jsonify(new_user_dict), 200)
api.add_resource(Signup, '/signup')

class UserInfo(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return make_response(jsonify(users), 200)
api.add_resource(UserInfo, '/users')

class CheckEmail(Resource):
    def get(self):
        email = request.args.get('email')
        if not email:
            return make_response(jsonify({'error':'Email is required'}),400)

        user = User.query.filter_by(email=email).first()
        if user:
            return make_response(jsonify({'available': False}),201)

        return make_response(jsonify({'available': True}),200)
api.add_resource(CheckEmail, '/checkemail')

class CreatePaymentIntent(Resource):
    def post(self):
        data = request.get_json()
        amount = data.get('amount')
        try:
            # Create PaymentIntent with the amount
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd'
            )
            print('Stripe Response:', intent)  # Log response for debugging
            return {'clientSecret': intent.client_secret}
        except Exception as e:
            print('Error:', str(e))  # Log errors for debugging
            return {'error': str(e)}, 400
api.add_resource(CreatePaymentIntent, '/create-payment-intent')

class Orders(Resource):
    def post(self):
        data = request.get_json()

        user_id = data.get('user_id') 
        product_list = data.get('products')
        total = data.get('total')
        order_date = data.get('orderDate')

        if not user_id or not product_list:
            return make_response(jsonify({'error':'Invalid data'}), 400)

        # user = User.query.get(user_id)
        user = User.query.filter(User.id == user_id).first()
        if not user:
            return make_response(jsonify({"error":'invalid data'}), 400)

        order = Order(
            user_id=user_id,
            total=total,
            order_date=order_date or datetime.utcnow()
        ) 
        db.session.add(order)
        db.session.flush()

        for product_data in product_list:
            product_id = product_data['id']
            quantity = product_data['quantity']
            product=Product.query.get(product_id)
            if not product:
                return make_response(jsonify({'error':f'Product with id {product_id} not found'}), 404)
            order_product = OrderProduct(order_id=order.id, product_id=product_id, quantity=quantity, price=product.price)
            db.session.add(order_product)
        
        db.session.commit()

        order_dict = order.to_dict()
        return make_response(jsonify(order_dict), 200)    
api.add_resource(Orders, '/checkout')

class RetriveOrder(Resource):
    def get(self):
        orders = [order.to_dict() for order in Order.query.all()]
        return make_response(jsonify(orders), 200)
api.add_resource(RetriveOrder, '/orders')

class Admins(Resource):
    def get (self):
        admins = [admin.to_dict() for admin in Admin.query.all()]
        return make_response(jsonify(admins), 200)
    def post(self):
        usename = request.get_json()['username']
        password = request.get_json()['password']

        new_admin = Admin(
            username = usename
        )

        new_admin.password_hash = password

        db.session.add(new_admin)
        db.session.commit()

        new_admin_dict=new_admin.to_dict()

        return make_response(jsonify(new_admin_dict), 200)
api.add_resource(Admins, '/admin')

class AdminLogin(Resource):
    def post(self):
        username = request.get_json()['username']
        admin = Admin.query.filter_by(username=username).first()
        password = request.get_json()['password']

        if admin.authenticate(password):
            session['admin_id'] = admin.id
            return admin.to_dict(), 200

        return {'error':'Invalid email or password'}, 401
api.add_resource(AdminLogin, '/admin/login')

class AdminDashboard(Resource):
    def post(self):
        data = request.get_json()

        name = data.get('name')
        image = data.get('image')
        price = data.get('price',None)
        description = data.get('description')
        product_depth= data.get('depth',None)
        product_weight = data.get('weight',None)
        product_height = data.get('height',None)
        product_width = data.get('width',None)
        discount = data.get('discount',None)
        is_it_new = data.get('new')
        is_it_clearance = data.get('clearance')
        is_it_onsale = data.get('sale')
        is_it_preorder = data.get('preorder')
        brand_name = data.get('brand')
        category_name = data.get('category')

        # if product_weight:
        #     try:
        #         float_product_weight = float(product_weight)
        #         return float_product_weight
        #     except ValueError:
        #         return make_response(jsonify({'error':'Invalid float conversion'}),400)
        # else:
        #     return make_response(jsonify({'error':'no data provided'}), 400)
        
        if not name or not image or not price or not description:
            return make_response(jsonify({'message':'All fields are required'}), 400)

        product = Product.query.filter(Product.name == name).first()
        if product:
            return make_response(jsonify({'message':'Product already existed'}), 400)
        
        brand = Brand.query.filter(Brand.brand_name == brand_name).first()
        if not brand:
            brand = Brand(brand_name=brand_name)
            db.session.add(brand)
            db.session.commit()

        category = Category.query.filter(Category.category_name == category_name).first()
        if not category:
            category = Category(category_name = category_name)
            db.session.add(category)
            db.session.commit()
        
        new_product = Product(
            name=name,
            image=image,
            price=price,
            description=description,
            product_depth=product_depth,
            product_weight=product_weight,
            product_height=product_height,
            product_width=product_width,
            discount=discount,
            is_it_new=is_it_new,
            is_it_clearance=is_it_clearance,
            is_it_onsale=is_it_onsale,
            is_it_preorder=is_it_preorder,
            brand_id=brand.id,
            category_id=category.id)

        db.session.add(new_product)
        db.session.commit()

        new_product_dict = new_product.to_dict()

        return make_response(jsonify(new_product_dict), 200)


    def delete(self):
        product_id = request.get_json()['id']
        if product_id is None:
            return make_response(jsonify({'message':'product id is required'}), 400)
        product = Product.query.get(product_id)
        if not product:
            return make_response(jsonify({'error':'Product not found'}), 400)
        db.session.delete(product)
        db.session.commit()

        return make_response(jsonify({'message': 'Product deleted successfully'}), 200)
api.add_resource(AdminDashboard, '/dashboard')

