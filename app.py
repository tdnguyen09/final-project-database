#!/usr/bin/env python3

import os

from flask import Flask, jsonify, request, make_response, redirect, url_for, session
from flask_restful import Resource
from config import db, api, app
from models import Product, User, Admin, Order, order_product, wishlist
# from datetime import timedelta

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
            user.products.append(product)
            db.session.commit()
            return make_response(jsonify({'message':f'{product.name} added to wishlist successfully'}), 201)
        else:
            return make_response(jsonify({'error': 'User or product not found'}), 404)
        

    def patch(self,id):
        data = request.get_json()
        product = Product.query.filter_by(id=id).first()
        for attr in data:
            if hasattr(product, attr):
                setattr(product, attr, data.get(attr))

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
#done
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

        return {'error':'Invalid email or password'}, 401
api.add_resource(Login, '/login')

# class GetSession(Resource):
#     def get(self):
#         session['user_id'] = 2  # Example of setting a user ID in the session
#         session.permanent = True  # Make session permanent
#         return "Session is set!"
# api.add_resource(GetSession,'/getsession')

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
        for attr in data:
            if hasattr(user, attr):
                setattr(user, attr, data.get(attr))
        db.session.merge(user)
        db.session.commit()

        response_dict = user.to_dict()
        return make_response(response_dict, 200)
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
            return jsonify({'message':'Email already registed'}), 400
        
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

        new_user_dict = new_user.to_dict()

        return make_response(jsonify(new_user_dict), 200)
api.add_resource(Signup, '/signup')

class UserInfo(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return make_response(jsonify(users), 200)

api.add_resource(UserInfo, '/users')



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
            db.session.execute(order_product.insert().values(order_id=order.id, product_id=product_id, quantity=quantity))

        db.session.commit()
        product_data = db.session.query(Product, order_product.c.quantity).join(order_product).filter(order_product.c.order_id == order.id).all()
        order_dict = {
            'id': order.id,
            'total': order.total,
            'order_date': order.order_date.isoformat(),
            'products': [
                {
                    'id': product.id,
                    'name': product.name,
                    'quantity': quantity
                }
                for product, quantity in product_data
            ]
        }
        return make_response(jsonify(order_dict), 200)    
api.add_resource(Orders, '/checkout')

class Admins(Resource):
    def get (self):
        admins = [admin.to_dict() for admin in Admin.query.all()]
        return make_response(jsonify(admins), 200)
    def post(self):
        usename = request.get_json()['username']
        password = request.get_json()['password']

        new_admin = Admin(
            usename = usename
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
        password = request.get_json()['password']

        admin = Admin.query.filter(Admin.username == usename)

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
        
        brand = Brand.query.filter(Brand.name == brand_name).first()
        if not brand:
            new_brand = Brand(brand_name=brand_name)
            db.session.add(new_brand)
            db.session.commit()

        category = Catergory.query.filter(Catergory.name == category_name).first()
        if not category:
            new_category = Category(catergory_name = category_name)
            db.session.add(new_category)
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
            catergory_id=catergory.id)

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

# return redirect(url_for('home'))
# render_template
