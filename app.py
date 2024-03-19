from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

db = SQLAlchemy(app)
CORS(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return {'products': [{'name': product.name, 'price': product.price} for product in products]}

@app.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get(id)
    if product:
        return {'id': product.id, 'name': product.name, 'price': product.price, 'description': product.description}
    return {'message': '404 Item Not Found'}

@app.route('/api/products/add', methods=['POST'])
def add_products():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data['name'], price=data['price'], description=data['description'])
        db.session.add(product)
        db.session.commit()
        return "Data inserted successfully!", 201
    return "This item already exists!", 400

@app.route('/api/products/delete', methods=['DELETE'])
def delete_products():
    data = request.json
    if 'name' in data:
        product = Product.query.filter_by(name=data['name']).first()
        db.session.delete(product)
        db.session.commit()
        return "Data deleted successfully!", 200
    return "This item does not exist!", 404

@app.route('/api/products/update/<int:id>', methods=['PUT'])

def update_products(id):
    product = Product.query.get_or_404(id)
    data = request.json

    if 'name' in data:
        product.name = data['name']

    if 'price' in data:
        product.price = data['price']
    
    if 'description' in data:
        product.description = data['description']

    db.session.commit()
    return "Data updated successfully!", 200

@app.route('/')
def index():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run(debug=True)
