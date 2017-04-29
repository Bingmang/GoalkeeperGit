from flask import render_template, redirect, request, url_for, flash
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
                                 owner=current_user._get_current_object())
        db.session.add(goalkeeper)
        flash('成功添加 ' + form.item_name.data + ' 到您的物品中')
        return redirect(url_for('goalkeeper.itemregistrate'))
    return render_template("goalkeeper/itemregistrate.html", form=form)


@goalkeeper.route('/itemboard', methods=['GET', 'POST'])
@login_required
def itemboard():
    user = current_user
    items = user.goalkeepers.order_by(Goalkeepers.timestamp)
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
        db.session.add(item)
        flash('成功更新物品信息')
        return redirect(url_for('goalkeeper.itemboard', username=user.username))
    form.item_id.data = item.item_id
    form.item_name.data = item.item_name
    form.alarm_state.data = item.alarm_state
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
