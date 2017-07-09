from flask import render_template, redirect, request, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import goalkeeper
from .. import db
from ..models import User, Permission, Goalkeepers
from ..email import send_email
from .forms import ItemRegistrationForm, EditItemForm


@goalkeeper.route('/itemregistrate', methods=['GET', 'POST'])
@login_required
def itemregistrate():
    form = ItemRegistrationForm()
    if form.validate_on_submit():
        goalkeeper = Goalkeepers(item_id=form.item_id.data,
                                 item_name=form.item_name.data,
                                 angle_range=form.angle_range.data,
                                 owner=current_user._get_current_object())
        db.session.add(goalkeeper)
        flash('成功添加 ' + form.item_name.data + ' 到您的物品中')
        return redirect(url_for('goalkeeper.itemboard'))
    return render_template("goalkeeper/itemregistrate.html", form=form)


@goalkeeper.route('/itemboard', methods=['GET', 'POST'])
@login_required
def itemboard():
    user = current_user
    items = user.goalkeepers.order_by(Goalkeepers.registe_time)
    return render_template('goalkeeper/itemboard.html', user=user, items=items)


@goalkeeper.route('/edit-item/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_item(id):
    user = current_user
    item = Goalkeepers.query.get_or_404(id)
    if user != item.owner:
        flash('你没有该物品的编辑权限！')
        return redirect(url_for('goalkeeper.itemboard', username=user.username))
    form = EditItemForm(item=item)
    if form.validate_on_submit():
        item.item_id = form.item_id.data
        item.item_name = form.item_name.data
        item.alarm_state = form.alarm_state.data
        item.angle_range = form.angle_range.data
        db.session.add(item)
        flash('成功更新物品信息')
        return redirect(url_for('goalkeeper.itemboard', username=user.username))
    form.item_id.data = item.item_id
    form.item_name.data = item.item_name
    form.alarm_state.data = item.alarm_state
    form.angle_range = item.angle_range
    return render_template('goalkeeper/edit_item.html', form=form)


@goalkeeper.route('/delete-item/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    user = current_user
    item = Goalkeepers.query.get_or_404(id)
    if current_user == item.owner:
        db.session.delete(item)
        flash('成功删除物品')
        return redirect(url_for('goalkeeper.itemboard', username=user.username))
    return render_template('.index.html')

#以下为单片机用API

@goalkeeper.route('/get_state/<path:item_id>', methods=['GET','POST'])
def get_state(item_id):
    goalkeeper = Goalkeepers.query.filter_by(item_id=item_id).first()
    if goalkeeper is None:
        abort(404)
    return (str(1) if(goalkeeper.alarm_state) else str(0))


@goalkeeper.route('/change_state/<path:item_id>', methods=['GET', 'POST'])
def change_state(item_id):
    goalkeeper = Goalkeepers.query.filter_by(item_id=item_id).first()
    if goalkeeper is None:
        abort(404)
    goalkeeper.alarm_state = False if goalkeeper.alarm_state else True
    db.session.add(goalkeeper)
    return (str(1) if(goalkeeper.alarm_state) else str(0))  

@goalkeeper.route('/get_angle/<path:item_id>', methods=['GET','POST'])
def get_angle(item_id):
    goalkeeper = Goalkeepers.query.filter_by(item_id=item_id).first()
    if goalkeeper is None:
        abort(404)
    return (str(goalkeeper.angle_range))

@goalkeeper.route('/post_gps/<path:item_id>', methods=['POST'])
def post_gps(item_id):
    goalkeeper = Goalkeepers.query.filter_by(item_id=item_id).first()
    if goalkeeper is None:
        abort(404)
    location = request.form.get('location', '')
    #存在逗号
    split = location.find(',')
    if(split != -1):
        latitude = float(location[:split])
        longitude = float(location[split+1:])
        goalkeeper.latitude = latitude
        goalkeeper.longitude = longitude
        db.session.add(goalkeeper)
        return (str(1))
    return (str(0))