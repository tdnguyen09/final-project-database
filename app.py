#!/usr/bin/env python3

import os

from flask import Flask, jsonify, request, make_response, redirect, url_for
from flask_restful import Resource
from models import Product, User, Admin
from config import db, api, app

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

        user = User.query.filter(User.id == session.get('user_id')).first()
        product = Product.query.filter_by(id=id).first()

        if not user or not product:
            return jsonify({'error':'Invalid data'}), 400

        db.session.execute(wishlist.insert().values(product_id=product.id, user_id=user.id))
        db.session.commit()
        return jsonify({'message':f'{product.name} added to wishlist successfully'}), 201
api.add_resource(ProductByID, '/products/<int:id>')

class Hello(Resource):
    def get(seelf):
        print('hello world')
        return 'Hello World'
api.add_resource(Hello, '/')

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

        first_name = request.get_json()['firstname']
        last_name = request.get_json()['lastname']
        email = request.get_json()['email']
        password = request.get_json()['password']
        address =request.get_json()['address']
        state = request.get_json()['state']
        postcode = request.get_json()['postcode']
        phone_number = request.get_json()['phone']
        suburb = request.get_json()['suburb']

        if not first_name or not last_name or not email or not password:
            return jsonify({'message':'All fields are required'}), 400
            # return redirect(url_for('signup'))
        
        user = User.query.filter(User.email == email).first()
        if user:
            return jsonify({'message':'Email already registed'}), 400
        
        new_user = User(
            first_name=first_name, 
            last_name=last_name,
            email=email,
            address=address,
            state=state,
            postcode=postcode,
            suburb=suburb,
            phone_number=phone_number)
        new_user.password_hash = password

        db.session.add(new_user)
        db.session.commit()

        return make_response(jsonify(new_user), 200)
api.add_resource(Signup, '/signup')

class UserInfo(Resource):
    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return make_response(jsonify(users), 200)

api.add_resource(UserInfo, '/users')


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

        db.session.commit()
        return jsonify({'message':'Order submitted successfully'}), 201       
api.add_resource(Order, '/checkout')

# class Admin(Resource):
#     def post(self):
#         username = request.get_json()['username']
#         password = request.get_json()['password']

#         admin = Admin.query.filter(Admin.username == usename)

#         if admin.authenticate(password):
#             session['admin_id'] = admin.id
#             return admin.to_dict(), 200

#         return {'error':'Invalid email or password'}, 401
# api.add_resource(Admin, '/admin')

class AdminDashboard(Resource):
    def post(self):
        data = request.get_json()

        name = data.get('productName')
        image = data.get('productImage')
        price = data.get('productPrice')
        description = data.get('productDescription')
        product_depth= data.get('productDepth')
        product_weight = data.get('productWeight')
        product_height = data.get('productHeight')
        product_width = data.get('productWidth')
        discount = data.get('discount')
        is_it_new = data.get('newProduct')
        is_it_clearance = data.get('clearanceProduct')
        is_it_onsale = data.get('saleProduct')

        # categories = data.get('catergory')
        if not name or image or price or description:
            return jsonify({'message':'All fields are required'}), 400

        product = Product.query.filter(Product.name == name).firts()
        if product:
            return jsonify({'message':'Product already existed'}), 400
        
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
            is_it_onsale=is_it_onsale
        )

        db.session.add(new_product)
        db.session.commit()

        return jsonify({"message": "New Product added successfully"}), 201

        def patch(self):
            data = request.get_json()
            product = Product.query.filter(Product.id == product.id).first()
            for attr in data:
                setattr(product, attr, data.get(attr))

        db.session.add(product)
        db.session.commit()

        response_dict = product.to_dict()
        return make_response(response_dict, 200)

        def delete(self):
            product = Product.query.filter(Product.id == product.id).first()
            if not product:
                return jsonify({'error':'Product not found'}), 400
            db.session.delete(product)
            db.session.commit()
            return jsonify({'message': 'Product deleted successfully'}), 200

api.add_resource(AdminDashboard, '/dashboard')

# return redirect(url_for('home'))
# render_template

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

        return make_response(jsonify(new_admin), 200)
api.add_resource(Admins, '/admins')

