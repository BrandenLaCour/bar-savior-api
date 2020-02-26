import models
from flask import request, jsonify, Blueprint
from flask_login import login_required, current_user

from playhouse.shortcuts import model_to_dict

rooms = Blueprint('rooms', 'rooms')

#Index Route
@rooms.route('/all', methods=['GET'])
@login_required
def show_rooms():
    rooms = models.Room.select()
    rooms_dict = [model_to_dict(room) for room in rooms]
    return jsonify(data=rooms_dict, message='retrieved {} rooms'.format(len(rooms_dict)), status=200),200

#Show route
@rooms.route('/<id>', methods=['GET'])
@login_required
def show_room(id):
    room = models.Room.get_by_id(id)
    room_dict = model_to_dict(room)
    return jsonify(data=room_dict, message='retrieved room {}'.format(room.name), status=200),200

#Create Route
@rooms.route('/', methods=['POST'])
@login_required
def create_room():
    payload = request.get_json()
    #Only create if admin
    if current_user.admin:
        created_room = models.Room.create(name=payload['name'], companyId=current_user.companyId)
        created_room_dict = model_to_dict(created_room)
        return jsonify(data=created_room_dict, message=f'successfully created room {created_room.name}', status=200),200
    else:
        return jsonify(data={}, message="you don't have the access rights to do that", status=200), 200

#Update Route
@rooms.route('/<id>', methods=['PUT'])
@login_required
def update_room(id):
    payload = request.get_json()
    #only update if admin
    if current_user.admin:
        update_query = models.Room.update(name=payload["name"]).where(models.Room.id == id)
        update_query.execute()
        updated_room = models.Room.get_by_id(id)
        return jsonify(data=updated_room.name, message=f'successfully update room {updated_room.name}', status=200),200

    else:
        return jsonify(data={}, message="you don't have the access rights to do that", status=200), 200

#Delete Route
@rooms.route('/<id>', methods=['Delete'])
@login_required
def delete_room(id):
    #only delete if admin
    if current_user.admin:
        delete_query = models.Room.delete().where(models.Room.id == id)
        delete_query.execute()
        return jsonify(data={}, message='successfully deleted room at id {}'.format(id), status=200), 200
    else:
        return jsonify(data={}, message="you don't have the access rights to do that", status=200), 200