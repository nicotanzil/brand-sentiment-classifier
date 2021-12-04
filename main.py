from enum import unique
from flask import Flask, json, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_cors import CORS, cross_origin
import jwt
import datetime
import uuid
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import traceback

from twitter.stream_tweets import Twitter

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

CORS(app)

# Connect to Postgresql
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost/sentiment_analysis'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    member = db.Column(db.Boolean)

twitter = Twitter()

class Keyword(Resource):
    def get(self, keyword):
        popular_tweets = twitter.fetch_tweet_by_query(query=keyword, count=25, result_type="popular")
        recent_tweets = twitter.fetch_tweet_by_query(query=keyword, count=25, result_type="recent")
        graph_data = twitter.fetch_last_week_tweets(query=keyword, count=50)
        return {
            "data": popular_tweets,
            "recent_data": recent_tweets,
            "graph_data": graph_data
        }

api.add_resource(Keyword, "/keyword/<string:keyword>")

# class KeywordStreamingBigData(Resource):
#     def get(self, keyword):
#         tweets = twitter.fetch_tweet_by_query(query=keyword, count=100, result_type="popular")
#         tweet_texts = [tweet['text'] for tweet in tweets]
#         return tweet_texts

# api.add_resource(KeywordStreamingBigData, "/keyword/streaming/<string:keyword>")

class UserQuery(Resource):
    def get(self, screen_name):
        tweets = twitter.fetch_tweet_by_user(screen_name=screen_name, count=15)
        return {
            "data": tweets
        }

api.add_resource(UserQuery, "/user/<string:screen_name>")

# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
        
#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']

#         if not token:
#             return jsonify({'message' : 'Token is missing!'}), 401

#         try: 
#             data = jwt.decode(token, app.config['SECRET_KEY'])
#             current_user = User.query.filter_by(public_id=data['public_id']).first()
#         except:
#             traceback.print_exc()
#             return jsonify({'message' : 'Token is invalid!'}), 401

#         return f(current_user, *args, **kwargs)
#     return decorated


# @app.route('/user', methods=['GET'])
# @token_required
# def get_all_users(current_user):

#     if not current_user.member:
#         return jsonify({'message' : 'Not authorized!'})

#     users = User.query.all()
#     output = []

#     for user in users:
#         user_data = {}
#         user_data['public_id'] = user.public_id
#         user_data['name'] = user.name
#         user_data['email'] = user.email
#         user_data['member'] = user.member
#         user_data['username'] = user.username
#         output.append(user_data)

#     return jsonify({'users': output})

# @app.route('/user/<public_id>', methods=['GET'])
# @token_required
# def get_user(current_user, public_id):
    
#     if not current_user.member:
#         return jsonify({'message' : 'Not authorized!'})

#     user = User.query.filter_by(public_id=public_id).first()

#     if not user:
#         return jsonify({'message' : 'User not found!'})

#     user_data = {}
#     user_data['public_id'] = user.public_id
#     user_data['name'] = user.name
#     user_data['email'] = user.email
#     user_data['member'] = user.member
#     user_data['username'] = user.username

#     return jsonify({'user' : user_data})

# @app.route('/current', methods=['GET'])
# @token_required
# def get_current_user(current_user):
#     if not current_user.member:
#         return jsonify({'message' : 'Not authorized!'})

#     user = User.query.filter_by(public_id=current_user.public_id).first()

#     if not user:
#         return jsonify({'message' : 'User not found!'})

#     user_data = {}
#     user_data['public_id'] = user.public_id
#     user_data['name'] = user.name
#     user_data['email'] = user.email
#     user_data['member'] = user.member
#     user_data['username'] = user.username

#     return jsonify({'user' : user_data})


# @app.route('/user', methods=['POST'])
# def create_user():
#     data = request.get_json()

#     hashed_password = generate_password_hash(data['password'], method='sha256')

#     new_user = User(
#                 public_id=str(uuid.uuid4()), 
#                 name=data['name'], 
#                 password=hashed_password, 
#                 email=data['email'],
#                 username=data['username'],
#                 member=True)

#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({'message' : 'New User Created!'})

# @app.route('/login', methods=['POST'])
# @cross_origin(origin='*')
# def login():
#     auth = request.authorization
#     print('AUTHENTICATION')
#     # print(auth.username)
#     # print(auth.password)

#     if not auth or not auth.username or not auth.password:
#         print('no auth')
#         return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

#     user = User.query.filter_by(username=auth.username).first()

#     if not user: 
#         print('no user')
#         return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

#     if check_password_hash(user.password, auth.password):
#         token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(hours=1)}, app.config['SECRET_KEY'])

#         return jsonify({
#                 'token' : token.decode('utf-8'),
#                 # 'public_id' : user.public_id,
#                 # 'name' : user.name,
#                 # 'email' : user.email,
#                 # 'member' : user.member,
#                 # 'username' : user.username,
#             })

#     return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    


if __name__ == "__main__":
    app.run(debug=True)
