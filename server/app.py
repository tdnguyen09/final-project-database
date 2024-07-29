#!/usr/bin/env python3

import os

# from flask import Flask, jsonify, request, make_response
# from flask_migrate import Migrate
from flask_restful import Resource
# from flask_bcrypt import Bcrypt
# from flask_cors import CORS

from models import Product, User
from config import db, api, app

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.json.compact = False

# migrate = Migrate(app, db)
# db.init_app(app)

# api = Api(app)
# bcrypt = Bcrypt(app)
# CORS(app)

class Products(Resource):
    def get(self):
        products = [product.to_dict() for product in Product.query.all()]
        return make_response(jsonify(products), 200)

api.add_resource(Products, '/products')

class ProductByID(Resource):
    def get(self, id):
        product = Product.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(product), 201)

    def post(self, id):

        user = User.query.filter(User.id == session.get('user_id')).first()
        product = Product.query.filter_by(id=id).first()

        if not user or not product:
            return jsonify({'error':'Invalid data'}), 400

        db.session.execute(wishlist.insert().values(product_id=product.id, user_id=user.id))
        db.session.commit()
        return jsonify({'message':f'{product.name} added to wishlist successfully'}), 201
api.add_resource(ProductByID, '/products/<int:id>')


class Login(Resource):
    def post(self):
        email = request.get_json()['email']
        user = User.query.filter(User.email == email)

        password = request.get_json()['password']

        if user.authenticate(password):
            session['user_id'] = user.id
            return user.to_dict(), 200

        return {'error':'Invalid email or password'}, 401
api.add_resource(Login, '/login')

class CheckSession(Resource):
    def get(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            return jsonify(user.to_dict())
        else:
            return jsonify({'message':'401: Not Authorized'}), 401
api.add_resource(CheckSession, '/user')

class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return jsonify({'message': '204: No Content'}), 204
api.add_resource(Logout, '/logout')

class UserUpdate(Resource):
    def patch(self):
        data = request.get_json()
        user = User.query.filter(User.id == session.get('user_id')).first()
        for attr in data:
            setattr(user, attr, data.get(attr))
        db.session.add(user)
        db.session.commit()

        response_dict = user.to_dict()
        return make_response(response_dict, 200)
api.add_resource(UserUpdate, '/user/update-detail')

class Signup(Resource):
    def post(self):
        data = request.get_json()

        first_name = data.get('firstname')
        last_name = data.get('lastname')
        email = data.get('email')
        password = data.get('password')
        address = data.get('address')
        state = data.get('state')
        postcode = data.get('postcode')
        phone_number = data.get('phonenumber')

        if not first_name or not last_name or not email or not password:
            return jsonify({'message':'All fields are required'}), 400
        
        user = User.query.filter(User.email == email).first()
        if user:
            return jsonify({'message':'Email already registed'}), 400
        
        new_user = User(
            first_name=first_name, 
            last_name=last_name,
            email=email,
            password=password,
            address=address,
            state=state,
            postcode=postcode,
            phone_number=phone_number)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201
api.add_resource(Signup, '/signup')

class Order(Resource):
    def post(self):
        data = request.get_json()

        user_id = data.get('user_id') 
        product_list = data.get('products')
        total_items = data.get('totalQuanity')
        total = data.get('total')
        order_date = data.get('orderDate')

        if not user_id or not product_list:
            return jsonify({'error':'Invalid data'}), 400

        # user = User.query.get(user_id)
        user = User.query.filter(User.id == session.get('user_id')).first()
        if not user:
            return #assign new id for guest check out

        order = Order(
            user_id=user_id,
            total_items=total_items,
            total=total,
            order_date=order_date
        ) 
        db.session.add(order)
        db.session.flush()

        for product_data in product_list:
            product_id = product_data['product_id']
            quantity = product_data['quantity']
            product=Product.query.get(product_id)
            if not product:
                return jsonify({'error':f'Product with id {product_id} not found'}), 404
            db.session.execute(order_product.insert().values(order_id=order.id, product_id=product_id, quantity=quantity))
# ask andre for add and execute in joint tables

        db.session.commit()
        return jsonify({'message':'Order submitted successfully'}), 201       
api.add_resource(Order, '/checkout')

