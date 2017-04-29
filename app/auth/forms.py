# -*- coding:utf-8 -*-
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField('登陆邮箱', validators=[Required(), Length(1, 64),
                                            Email()])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登陆')


class RegistrationForm(Form):
    email = StringField('登陆邮箱', validators=[Required(message='邮箱不能为空，你这智障'), Length(1, 64),
                                            Email()])
    username = StringField('用户名', validators=[
        Required(message='用户名不能为空，你是不是傻'), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                 '用户名只能是英文或下划线啊，咱暂时不支持中文')])
    password = PasswordField('密码', validators=[
        Required(message='密码是空的，你想被盗号啊？'), EqualTo('password2', message='两次输入的密码必须相同啊智障.')])
    password2 = PasswordField('密码确认', validators=[Required(message='别偷懒好吗')])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已经被注册.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用.')


class ChangePasswordForm(Form):
    old_password = PasswordField('Old password', validators=[Required()])
    password = PasswordField('New password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm new password', validators=[Required()])
    submit = SubmitField('Update Password')


class PasswordResetRequestForm(Form):
    email = StringField('邮箱', validators=[Required(message='没邮箱你重置个屁啊你重置'), Length(1, 64),
                                          Email(message='这他妈是个假邮箱吧')])
    submit = SubmitField('重置密码')


class PasswordResetForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('New Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


class ChangeEmailForm(Form):
    email = StringField('New Email', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
