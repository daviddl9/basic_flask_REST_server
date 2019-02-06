from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/David/PycharmProjects/RESTflask/resource.db'

db = SQLAlchemy(app)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(50))
    user_id = db.Column(db.Integer)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True) # id when you decode user's token
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({
                'message' : 'Token is missing'
            })

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({
                'message':'token is invalid'
            }), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):

    if not current_user.admin:
        return jsonify({
            'message' : 'Unauthorised: No admin permissions'
        })

    users = User.query.all()
    output = []
    for user in users:
        user_data = {
            'public_id':user.public_id,
            'name' : user.name,
            'password' : user.password,
            'admin' : user.admin
        }
        output.append(user_data)
    return jsonify({
        'users' : output
    })

@app.route('/user/<public_id>', methods=['GET'])
@token_required
def get_one_user(current_user, public_id):

    if not current_user.admin:
        return jsonify({
            'message' : 'Unauthorised: No admin permissions'
        })

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({
            'message' : 'No user found!'
        })

    user_data = {
        'public_id' : user.public_id,
        'name' : user.name,
        'password' : user.password,
        'admin' : user.admin
    }

    return jsonify({
        'user' : user_data
    })

@app.route('/user', methods=['POST'])
@token_required
def create_user(current_user):
    if not current_user.admin:
        return jsonify({
            'message' : 'Unauthorised: No admin permissions'
        })
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': 'New user created!'
    })

@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({
            'message' : 'Unauthorised: No admin permissions'
        })
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({
            'message': 'No user found!'
        })

    user.admin = True
    db.session.commit()

    return jsonify({
        'message' : 'User has been promoted!'
    })

@app.route('/user/<public_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({
            'message' : 'Unauthorised: No admin permissions'
        })
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({
            'message': 'No user found!'
        })

    db.session.delete(user)
    db.session.commit()

    return jsonify({
        'message' : 'User has been deleted'
    })

@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({
            'message' : 'Invalid login credentials!'
        })

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return jsonify({
            'message' : 'no user found'
        })

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({
            'public_id':user.public_id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
        }, app.config['SECRET_KEY'])
        return jsonify({
            'token' : token.decode('UTF-8')
        })

    return jsonify({
        'message' : 'Could not verify user'
    })


@app.route('/resource', methods=['GET'])
@token_required
def get_all_resources(current_user):
    resources = Resource.query.filter_by(user_id=current_user.id).all()

    output = []

    for resource in resources:
        resource_data = {
            'id' : resource.id,
            'text' : resource.text,
            'user_id' : resource.user_id
        }
        output.append(resource_data)
    return jsonify({
        'resources' : output
    })

@app.route('/resource/<resource_id>', methods=['GET'])
@token_required
def get_one_resource(current_user, resource_id):
    resource = Resource.query.filter_by(id=resource_id, user_id=current_user.id).first()
    if not resource:
        if (current_user.admin):
            resource = Resource.query.filter_by(id=resource_id).first()
            if resource:
                return jsonify({
                    'id': resource.id,
                    'text': resource.text,
                    'user_id': resource.user_id
                })
        return jsonify({
            'message' : 'No such resource'
        })

    return jsonify({
        'id': resource.id,
        'text': resource.text,
        'user_id': resource.user_id
    })

@app.route('/resource', methods=['POST'])
@token_required
def create_resource(current_user):
    data = request.get_json()
    new_resource = Resource(text=data['text'], user_id=current_user.id)
    db.session.add(new_resource)
    db.session.commit()

    return jsonify({
        'message' : 'Resource created!'
    })

@app.route('/resource/<resource_id>', methods=['DELETE'])
@token_required
def user_delete_resource(current_user, resource_id):
    resource = Resource.query.filter_by(id=resource_id, user_id=current_user.id).first()
    if not resource:
        if (current_user.admin):
            resource = Resource.query.filter_by(id=resource_id).first()
            if resource:
                db.session.delete(resource)
                db.session.commit()
                return jsonify({
                    'message' : 'Resource deleted by admin'
                })
        return jsonify({
            'message': 'No such resource'
        })
    db.session.delete(resource)
    db.session.commit()
    return jsonify({
        'message': 'Resource deleted by user'
    })

@app.route('/resource/<resource_id>', methods=['DELETE'])
@token_required
def admin_delete_resource(current_user, todo_id):
    return ''

if __name__ == '__main__':
    app.run(debug=True)