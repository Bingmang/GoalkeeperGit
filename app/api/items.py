from flask import jsonify, request, g, abort, url_for, current_app
from .. import db
from ..models import Goalkeepers, User
from . import api
from .decorators import permission_required
from .errors import forbidden


@api.route('/get_goalkeeper/<path:item_id>')
def get_goalkeeper(item_id):
    goalkeeper = Goalkeepers.query.filter_by(item_id=item_id).first()
    if goalkeeper is not None:
        if g.current_user == goalkeeper.owner:
            return jsonify(goalkeeper.to_json())
        return forbidden('The Goalkeeper is NOT BELONGS to you! --By Goalkeeper')
    return forbidden('The Goalkeeper is NOT EXIST! --By Goalkeeper')


@api.route('/get_user_goalkeepers/<path:user_email>')
def get_user_goalkeepers(user_email):
    goalkeepers = g.current_user.goalkeepers.order_by(Goalkeepers.registe_time)
    if goalkeepers is not None:
        if user_email == g.current_user.email:
            json_goalkeepers = {"goalkeepers": []}
            for goalkeeper in goalkeepers:
                json_goalkeepers["goalkeepers"].append(goalkeeper.to_json())
            return jsonify(json_goalkeepers)
        return forbidden('The Goalkeeper is NOT BELONGS to you! --By Goalkeeper')
    return forbidden('The Goalkeeper is NOT EXIST! --By Goalkeeper')

@api.route('/change_range/<path:id_range>')
def change_range(id_range):
    #/change_range/liyanxing_angle_range=1
    goalkeeper_id = id_range[:-14]
    goalkeeper = Goalkeepers.query.filter_by(item_id=goalkeeper_id).first()
    if goalkeeper is not None:
        if g.current_user == goalkeeper.owner:
            goalkeeper.angle_range=id_range[-1]
            db.session.add(goalkeeper)
            return '1'
        return forbidden('The Goalkeeper is NOT BELONGS to you! --By Goalkeeper')
    return forbidden('The Goalkeeper is NOT EXIST! --By Goalkeeper')
