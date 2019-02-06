#__author__ = ritvikareddy2
#__date__ = 2019-02-06

from flask import Flask, render_template
from flask_restful import Api, Resource, reqparse

import json

app = Flask(__name__)
api = Api(app)


@app.route('/')
def home():
    return render_template('home.html')


def load_data():
    with open('users.json') as f:
        data = json.load(f)
    # print(data)
    return data


class User(Resource):

    users = load_data()

    def get(self, name):
        for user in self.users:
            if name == user['name']:
                return user, 200
        return 'User doesnt exist', 404

    def post(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in self.users:
            if name == user['name']:
                return 'User already exists', 400

        user = {
            'name': name,
            'age': args['age'],
            'occupation': args['occupation']
        }

        self.users.append(user)

        return user, 201

    def put(self, name):
        parser = reqparse.RequestParser()
        parser.add_argument("age")
        parser.add_argument("occupation")
        args = parser.parse_args()

        for user in self.users:
            if name == user['name']:
                user['age'] = args['age']
                user['occupation'] = args['occupation']
                return user, 200

        user = {
            'name': name,
            'age': args['age'],
            'occupation': args['occupation']
        }
        self.users.append(user)

        return user, 201

    def delete(self, name):
        self.users = [user for user in self.users if user['name'] != name]
        return 'User deleted', 200


if __name__ == '__main__':
    api.add_resource(User, '/user/<string:name>')
    app.run(debug=True)
