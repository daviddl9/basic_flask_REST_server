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
    has_quota = db.Column(db.Boolean, default=False)
    quota = db.Column(db.Integer)
    resource_count = db.Column(db.Integer)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({
                'message' : 'Token is missing'
            }), 401

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
        }), 401

    users = User.query.all()
    output = []
    for user in users:
        user_data = {
            'public_id':user.public_id,
            'name' : user.name,
            'password' : user.password,
            'admin' : user.admin,
            'has_quota': user.has_quota,
            'quota': user.quota,
            'resource_count': user.resource_count
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
        }), 401

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({
            'message' : 'No user found!'
        }), 401

    user_data = {
        'public_id' : user.public_id,
        'name' : user.name,
        'password' : user.password,
        'admin' : user.admin,
        'has_quota': user.has_quota,
        'quota':user.quota,
        'resource_count': user.resource_count
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
        }), 401
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False, has_quota=False,resource_count=0)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'message': 'New user created!'
    })

@app.route('/user/setquota/<public_id>', methods=['PUT'])
@token_required
def set_quota(current_user, public_id):
    if not current_user.admin:
        return jsonify({
            'message':'Unauthorised: No admin permissions'
        })
    data = request.get_json()

    if not data:
        return jsonify({
            'message' : 'Invalid quota'
        }), 401

    quota = int(data['quota'])

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({
            'message':'No such user found!'
        }), 401

    user.has_quota = True
    user.quota = quota
    db.session.commit()

    return jsonify({
        'message':'Quota set!'
    })

@app.route('/user/<public_id>', methods=['PUT'])
@token_required
def promote_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({
            'message' : 'Unauthorised: No admin permissions'
        }), 401
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({
            'message': 'No user found!'
        }), 401

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
        }), 401
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({
            'message': 'No user found!'
        }), 401

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
        }), 401

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return jsonify({
            'message' : 'no user found'
        }), 401

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({
            'public_id':user.public_id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'])
        return jsonify({
            'token' : token.decode('UTF-8')
        })

    return jsonify({
        'message' : 'Could not verify user'
    })


@app.route('/resource/all', methods=['GET'])
@token_required
def admin_list_all_resources(current_user):
    if not current_user.admin:
        return jsonify({
            'message' : 'No permissions to view all resources'
        }), 401
    resources = Resource.query.all()

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
        if current_user.admin:
            resource = Resource.query.filter_by(id=resource_id).first()
            if resource:
                return jsonify({
                    'id': resource.id,
                    'text': resource.text,
                    'user_id': resource.user_id
                })
        return jsonify({
            'message' : 'No such resource'
        }), 401

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

    if current_user.has_quota:
        if current_user.resource_count == current_user.quota:
            return jsonify({
                'message' : 'Invalid request: Resource quota reached.'
            }), 401

    current_user.resource_count += 1
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
        # If admin can access the resource
        if (current_user.admin):
            resource = Resource.query.filter_by(id=resource_id).first()
            if resource:
                user = User.query.filter_by(id=resource.user_id).first()
                user.resource_count -= 1
                db.session.delete(resource)
                db.session.commit()
                return jsonify({
                    'message' : 'Resource deleted by admin'
                })
        return jsonify({
            'message': 'No such resource'
        }), 401

    current_user.resource_count -= 1
    db.session.delete(resource)
    db.session.commit()
    return jsonify({
        'message': 'Resource deleted by user'
    })

if __name__ == '__main__':
    app.run(debug=True)