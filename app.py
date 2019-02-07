#__author__ = ritvikareddy2
#__date__ = 2019-02-06

import json
from bson.json_util import dumps
from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse
from pymongo import MongoClient


app = Flask(__name__)
api = Api(app)
client = MongoClient('localhost', 27017)
db = client['sample_db']
users_collection = db.users


@app.route('/')
def home():
    return render_template('home.html')


def load_data():
    users_collection.drop()
    with open('users.json') as f:
        data = json.load(f)
    result = users_collection.insert_many(data)
    # print(data)
    return result


class User(Resource):

    users = load_data()

    def get(self, name):
        res = users_collection.find_one({'name': name}, {"_id": 0})
        if res:
            return res, 200
        return 'User doesnt exist', 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        res = users_collection.find_one({'name': name})
        if res:
            return 'User already exists', 400

        user = {
            'name': name,
            'age': args['age'],
            'occupation': args['occupation']
        }

        users_collection.insert_one(user)
        user.pop('_id')
        return user, 201

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        res = users_collection.find({'name': name})
        if res:
            user = {
                'age': args['age'],
                'occupation': args['occupation']
            }
            users_collection.update_one({'name': name}, {'$set': user})
            return user, 200

        user = {
            'name': name,
            'age': args['age'],
            'occupation': args['occupation']
        }

        users_collection.insert_one(user)
        return user, 201

    def delete(self, name):
        users_collection.delete_one({'name': name})
        return 'User deleted', 200


if __name__ == '__main__':
    # load_data()
    api.add_resource(User, '/user/<string:name>')
    app.run(debug=True)
