# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import Goalkeepers


class ItemRegistrationForm(Form):
    item_id = StringField('物品ID', validators=[
                          Required(message='必须输入物品ID'), Length(1, 32)])
    item_name = StringField(
        '物品名称', validators=[Required(message='给物品起个名字吧'), Length(1, 64)])
    submit = SubmitField('注册物品')

    def validate_item_id(self, field):
        if Goalkeepers.query.filter_by(item_id=field.data).first():
            raise ValidationError('The ID already been taken.')


class EditItemForm(Form):
    item_id = StringField('物品ID', validators=[
                          Required(message='必须输入物品ID'), Length(1, 32)])
    item_name = StringField(
        '物品名称', validators=[Required(message='给物品起个名字吧'), Length(1, 64)])
    alarm_state = BooleanField('报警状态')
    submit = SubmitField('更改物品')

    def validate_item_id(self, field):
        if Goalkeepers.query.filter_by(item_id=field.data).first():
            raise ValidationError('The ID already been taken.')

    def __init__(self, item, *args, **kwargs):
        super(EditItemForm, self).__init__(*args, **kwargs)
        self.item = item
