from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    def json(self):
        return {'id': self.id, 'username': self.username, 'email': self.email}


@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'The server is running'})

@app.route('/api/flask/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        new_user = User(username=data['username'], email=data['email'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            'id': new_user.id,
            'username': new_user.username,
            'email': new_user.email
        }), 201
    except Exception as e:
        return make_response(jsonify({'error creating user': str(e)}), 500)

@app.route('/api/flask/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        users_data = [{'id': user.id, 'username': user.username, 'email': user.email} for user in users]
        return jsonify(users_data), 200
    except Exception as e:
        return make_response(jsonify({'error getting users': str(e)}), 500)

@app.route('/api/flask/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            return make_response(jsonify({'user': user.json()}), 200)
    except Exception as e:
        return make_response(jsonify({'error getting user': str(e)}), 500)

@app.route('/api/flask/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.username = data['username']
            user.email = data['email']
            db.session.commit()
            return make_response(jsonify({'message': 'user updated'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'error updating user': str(e)}), 500)

@app.route('/api/flask/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = User.query.filter_by(id=id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return make_response(jsonify({'message': 'user deleted'}), 200)
        return make_response(jsonify({'message': 'user not found'}), 404)
    except Exception as e:
        return make_response(jsonify({'error deleting user': str(e)}), 500)


with app.app_context():
    db.create_all()
