#!/usr/bin/env python3

from flask import Flask, jsonify,make_response,request
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound


from models import db, Episode,Guest,Appearance

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

# Routes

@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    episode_list = []
    for episode in episodes:
        episode_data = {
            'id': episode.id,
            'date': episode.date,
            'number': episode.number
        }
        episode_list.append(episode_data)
    return jsonify(episode_list)


@app.route('/episodes/<int:episode_id>', methods=['GET'])
def get_episode(episode_id):
    episode = Episode.query.get(episode_id)
    if episode:
        guest_list = []
        for appearance in episode.appearances:
            guest_data = {
                'id': appearance.guest.id,
                'name': appearance.guest.name,
                'occupation': appearance.guest.occupation
            }
            guest_list.append(guest_data)
        episode_data = {
            'id': episode.id,
            'date': episode.date,
            'number': episode.number,
            'guests': guest_list
        }
        return jsonify(episode_data)
    else:
        return jsonify({'error': 'Episode not found'}), 404


@app.route('/episodes/<int:episode_id>', methods=['DELETE'])
def delete_episode(episode_id):
    episode = Episode.query.get(episode_id)
    if episode:
        for appearance in episode.appearances:
            db.session.delete(appearance)
        db.session.delete(episode)
        db.session.commit()
        return '', 204
    else:
        return jsonify({'error': 'Episode not found'}), 404


@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    guest_list = []
    for guest in guests:
        guest_data = {
            'id': guest.id,
            'name': guest.name,
            'occupation': guest.occupation
        }
        guest_list.append(guest_data)
    return jsonify(guest_list)


@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()
    rating = data.get('rating')
    episode_id = data.get('episode_id')
    guest_id = data.get('guest_id')

    try:
        # Retrieve the episode by id
        episode = Episode.query.filter_by(id=episode_id).one()
    except NoResultFound:
        return jsonify({'error': 'Episode not found'}), 404

    try:
        appearance = Appearance(rating=rating, episode_id=episode_id, guest_id=guest_id)
        db.session.add(appearance)
        db.session.commit()

        appearance_data = {
            'id': appearance.id,
            'rating': appearance.rating,
            'episode': {
                'id': episode.id,
                'date': episode.date.strftime('%m/%d/%y'),
                'number': episode.number
            },
            'guest': {
                'id': appearance.guest.id,
                'name': appearance.guest.name,
                'occupation': appearance.guest.occupation
            }
        }
        return jsonify(appearance_data), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'errors': ['validation errors']}), 400

# ...

if __name__ == '__main__':
    app.run(port=5555)
