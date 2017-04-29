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
        else:
            return forbidden('You have no Permission! --By Goalkeeper')
    else:
        return forbidden('You have no Permission!!! --By Goalkeeper')


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
