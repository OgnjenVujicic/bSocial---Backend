from flask import url_for, redirect, jsonify, request, make_response
from bSocial import app, argon2
from bSocial.models import User
from functools import wraps
import jwt, datetime, re
import bSocial.services as service
from bSocial.data_checker import data_is_valid


def data_invalid():
    return jsonify({"error": "Inavlid data"}), 400

def token_encode(user):
    token = jwt.encode({
            'email' : user.email,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
        }, app.config['SECRET_KEY'])
    return jsonify({'token' : token.decode('UTF-8')})


def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        token = None
        if 'access-token' in request.headers:
            token = request.headers['access-token']

        if not token:
            return jsonify({'message': 'No token.'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(email=data['email']).first()
        except:
            return jsonify({'message': 'Invalid token'}), 403
        return func(current_user,*args, **kwargs)
    return wrapped
    

@app.route("/register", methods=['GET', 'POST'])
def register():
    data = request.get_json()
    required = ['first_name','last_name','username','email','password']
    if not data_is_valid(data,required):
        return data_invalid()
    if not re.match(r"[^@]+@[^@]+\.[^@]+", data['email']):
        return jsonify({"error": "email is invalid"}), 400    
    return service.insert_user(data)


@app.route("/login", methods=['GET', 'POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})
    user = User.query.filter_by(email=auth.username).first()
    if user and argon2.check_password_hash(user.password, auth.password):
        return token_encode(user)
    return make_response('could not verify',  401, {'WWW.Authentication': 'Basic realm: "login required"'})


@app.route("/refresh_token", methods=['GET', 'POST'])
@check_for_token
def refresh_token(current_user):
    return token_encode(current_user)


@app.route("/post/new", methods=['GET', 'POST'])
@check_for_token
def new_post(current_user):
    data = request.get_json()
    required = ['title','content']
    if not data_is_valid(data,required):
        return data_invalid()
    return service.insert_post(data, current_user)


@app.route("/comment/new", methods=['GET', 'POST'])
@check_for_token
def new_comment(current_user):
    data = request.get_json()
    required = ['post_id','content']
    if not data_is_valid(data,required):
        return data_invalid()
    return service.insert_comment(data, current_user)


@app.route("/follow", methods=['GET', 'POST'])
@check_for_token
def follow(current_user):
    data = request.get_json()
    required = ['user_id']
    if not data_is_valid(data,required):
        return data_invalid()
    return service.insert_follower(data, current_user)


@app.route("/comments")
@check_for_token
def comments(current_user):
    post_id = request.args.get('post_id',type=int)
    if not post_id:
        return data_invalid()
    return service.get_commments(post_id)


@app.route("/feed")
@check_for_token
def feed(current_user):
    page = request.args.get('page',1,type=int)
    return service.get_feed(current_user,page)


@app.route("/comments/notifications")
@check_for_token
def comments_notifications(current_user):
    return service.get_comments_notifications(current_user)
