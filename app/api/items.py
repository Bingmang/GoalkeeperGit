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
    goalkeepers = g.current_user.goalkeepers.order_by(Goalkeepers.timestamp)
    if goalkeepers is not None:
        if user_email == g.current_user.email:
            json_goalkeepers = {"goalkeepers": []}
            for goalkeeper in goalkeepers:
                json_goalkeepers["goalkeepers"].append(goalkeeper.to_json())
            return jsonify(json_goalkeepers)
        return forbidden('The Goalkeeper is NOT BELONGS to you! --By Goalkeeper')
    return forbidden('The Goalkeeper is NOT EXIST! --By Goalkeeper')

# @api.route('/posts/', methods=['POST'])
# @permission_required(Permission.WRITE_ARTICLES)
# def new_post():
#     post = Post.from_json(request.json)
#     post.author = g.current_user
#     db.session.add(post)
#     db.session.commit()
#     return jsonify(post.to_json()), 201, \
#         {'Location': url_for('api.get_post', id=post.id, _external=True)}


# @api.route('/posts/<int:id>', methods=['PUT'])
# @permission_required(Permission.WRITE_ARTICLES)
# def edit_post(id):
#     post = Post.query.get_or_404(id)
#     if g.current_user != post.author and \
#             not g.current_user.can(Permission.ADMINISTER):
#         return forbidden('Insufficient permissions')
#     post.body = request.json.get('body', post.body)
#     db.session.add(post)
#     return jsonify(post.to_json())
