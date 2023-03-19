# from controllers import *
from flask_security import UserMixin, RoleMixin
from database import db

roles_users = db.Table('roles_users',
                db.Column('user_id',db.Integer(),db.ForeignKey('users.id')),
                db.Column('role_id',db.Integer(),db.ForeignKey('role.id')))

#define user
class Users(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    profile_pic = db.Column(db.LargeBinary,nullable = True)
    username = db.Column(db.String,nullable = False)
    email = db.Column(db.String,nullable = False,unique = True)
    password = db.Column(db.String,nullable = False)
    active = db.Column(db.Boolean())
    fs_uniquifier =db.Column(db.String(255),unique=True, nullable = False)
    users_posts = db.relationship('Posts',backref = 'users',cascade = 'all,delete')
    roles = db.relationship('Role', secondary= roles_users, backref= db.backref('users'))
#role -----------------
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String,nullable = False,unique = True)
    decription = db.Column(db.String(255))

#define posts
class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    title = db.Column(db.String,nullable = False)
    content = db.Column(db.Text,nullable = False)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id', ondelete = 'CASCADE'),nullable = False)
    date_created = db.Column(db.DateTime,server_default=db.func.now())
    date_modified = db.Column(db.DateTime)
    

#define followers
class Followers(db.Model):
    __tablename__ = 'followers'
    id = db.Column(db.Integer,primary_key = True,autoincrement = True)
    user_id = db.Column(db.Integer,db.ForeignKey('users.id', ondelete = 'CASCADE'))
    following_id = db.Column(db.Integer,db.ForeignKey('users.id', ondelete = 'CASCADE'))
    followers = db.relationship('Users',foreign_keys = [following_id],cascade = 'all,delete')
    user = db.relationship('Users',backref='followers',foreign_keys = [user_id],cascade = 'all,delete')

#define following
# class Followings(db.Model):
#     __tablename__ = 'followings'
#     id = db.Column(db.Integer,primary_key = True,autoincrement = True)
#     user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
#     following_id = db.Column(db.Integer)
#     followings = db.relationship('Users',passive_deletes = False,backref='followings')
