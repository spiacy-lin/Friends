from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ori.db'
db = SQLAlchemy(app)


class Friends (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(50))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Friend %d>' % self.id


db.create_all()


class FriendsSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Friends
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=True)


@app.route('/friends', methods=['GET'])
def index():
    get_friends = Friends.query.all()
    friend_schema = FriendsSchema(many=True)
    friends, error = friend_schema.dump(str(get_friends))
    return make_response(jsonify({"friends": friends}))


@app.route('/friends/<id>', methods=['GET'])
def get_friend_by_id(id):
    get_friend = Friends.query.get(id)
    friend_schema = FriendsSchema()
    friend, error = friend_schema.dump(get_friend)
    return make_response(jsonify({"friend": friend}))


@app.route('/friends/<id>', methods=['PUT'])
def update_friend_by_id(id):
    data = request.get_json()
    get_friend = Friends.query.get(id)
    if data.get('description'):
        get_friend.description = data['discription']
    if data.get('name'):
        get_friend.name = data['name']
    db.session.add(get_friend)
    db.session.commit()
    friend_schema = FriendsSchema(only=['id', 'name', 'description'])
    friend, error = friend_schema.dump(get_friend)
    return make_response(jsonify({"friend": friend}))


@app.route('/friends/<id>', methods=['DELETE'])
def delete_friend_by_id(id):
    get_friend = Friends.querry.get(id)
    db.session.delete(get_friend)
    db.session.commit()
    return make_response("", 204)


@app.route('/friends', methods=['POST'])
def create_friend():
    data = request.get_json()
    friend_schema = FriendsSchema()
    friend, error = friend_schema.load(data)
    result = friend_schema.dump(friend.create()).data
    return make_response(jsonify({"friend": result}), 200)


if __name__ == '__main__':
    app.run(debug=True)
