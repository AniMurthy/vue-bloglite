from flask import Flask,request,jsonify,send_file
import datetime

from io import BytesIO

from sqlalchemy import null
from models import *
from flask_security import auth_required
from flask import current_app as app
from flask_login import current_user

import base64

from workers import *
import tasks

#New Authhor ----------------------------------------------------------------
@app.route('/get_id',methods=['GET','POST'])
@auth_required("token")
def get_id():
  user_id=current_user.id
  username=current_user.username
  if request.method=='GET':
    print(user_id)
    return jsonify({"author_id":user_id})
  # if request.method=='POST':
  #   name=request.json['name']
  #   email=request.json['email']
  #   pwd=request.json['pwd']
  #   emails=Users.query.filter(Users.email_id==email).first()
  #   if emails:
  #     return jsonify('Email already registered. Please register with a diffrent email or login')
  #   else:
  #     user = Users(name=name,email_id=email,password=pwd)
  #     db.session.add(user)
  #     db.session.commit()
  #     return jsonify("name created successfully")


# Author Actions ------------------------------------------------------------
@app.route('/author',methods=['GET'])
@auth_required("token")
def authors():
  user_id=current_user.id
  username=current_user.username
  if request.method == 'GET':
    author=Users.query.filter(Users.id==user_id).first()
    posts=len(Posts.query.filter(Posts.author_id==user_id).all())
    follow=len(Followers.query.filter(Followers.user_id==user_id).all())
    following=len(Followers.query.filter(Followers.following_id==user_id).all())
    # pic = base64.b64encode(Users.profile_pic).decode('utf-8')
    if author==None:
      return jsonify('Author doesn\'t exist ')
    else:
      return jsonify({"Name":author.username,"Author_id":author.id,"Author_Email":author.email,"no_follows":follow,"no_posts":posts,"no_following":following})



@app.route('/author/pic',methods=['GET','POST'])
@auth_required("token")
def authors_profile_pic():
  user_id=current_user.id
  username=current_user.username
  if request.method == 'GET':
    pic = base64.b64encode(Users.query.filter(Users.id==user_id).first().profile_pic).decode('utf-8')
    print(pic)
    return jsonify({"pic":pic})


@app.route('/jobs',methods=['GET','POST'])
@auth_required("token")
def jobs():
  user_id=current_user.id
  username=current_user.username
  if request.method == 'GET':
    job=tasks.sayHello.delay(username)
    result = job.wait()
    return str(result)


@app.route('/author/profile/<id>',methods=['GET'])
@auth_required("token")
# @login_required
def authors_profile(id):
  user_id=current_user.id
  username=current_user.username
  if request.method == 'GET':
    author=Users.query.filter(Users.id==id).first()
    posts=len(Posts.query.filter(Posts.author_id==id).all())
    follow=len(Followers.query.filter(Followers.user_id==id).all())
    following=len(Followers.query.filter(Followers.following_id==id).all())
    followMe=bool(Followers.query.filter(Followers.following_id==id).filter(Followers.user_id==user_id).first())
    post=Posts.query.filter(Posts.author_id==id).all()
    result=[]
    if post:
      for i in range(len(post)):
        author=Users.query.filter(Users.id==post[i].author_id).first()
        paragraphs=[]
        paragraphs=((post[i].content.split('\\n')))
        result.append({"Title":post[i].title,"Content":paragraphs,"Date":post[i].date_created})
    if author==None:
      return jsonify('Author doesn\'t exist ')
    else:
      return jsonify({"Name":author.username,"Author_id":author.id,"Author_Email":author.email,"no_follows":follow,"no_posts":posts,"no_following":following,"posts":result,"followMe":followMe})

@app.route('/author/following',methods=['GET'])
@auth_required("token")
def author_following():
  user_id=current_user.id
  username=current_user.username
  if request.method == 'GET':
    following=Followers.query.filter(Followers.following_id==user_id).all()
    follow=[]
    for i in range(len(following)):
      id=following[i].user_id
      name=Users.query.filter(Users.id==id).first().username
      follow.append({"id":id,"name":name})
      # print(follow)
    if follow==None:
      return jsonify('Following don\'t exist ')
    else:
      return follow
    
@app.route('/author/followers',methods=['GET'])
@auth_required("token")
def author_followers():
  user_id=current_user.id
  username=current_user.username
  if request.method == 'GET':
    following=Followers.query.filter(Followers.user_id==user_id).all()
    follow=[]
    for i in range(len(following)):
      id=following[i].following_id
      name=Users.query.filter(Users.id==id).first().username
      follow.append({"id":id,"name":name})
      # print(follow)
    if follow==None:
      return jsonify('Following don\'t exist ')
    else:
      return follow

@app.route('/author/follow/<id>',methods=['POST'])
@auth_required("token")
def author_follow(id):
  user_id=current_user.id
  username=current_user.username
  if request.method == 'POST':
    user=Followers.query.filter(Followers.user_id==user_id).filter(Followers.following_id==id).first()
    if user:
      return jsonify('Already following')
    elif int(id)==user_id:
      return jsonify('This is you')      
    else:
      follow=Followers(user_id=user_id,following_id=id)
      db.session.add(follow)
      db.session.commit()
      return jsonify('Followed')

@app.route('/author/unfollow/<id>',methods=['POST'])
@auth_required("token")
def author_unfollow(id):
  user_id=current_user.id
  username=current_user.username
  if request.method == 'POST':
    user=Followers.query.filter(Followers.user_id==user_id).filter(Followers.following_id==id).all()
    if user:
      Followers.query.filter(Followers.user_id==user_id).filter(Followers.following_id==id).delete()
      db.session.commit()
      return jsonify('Deleted')
    else:
      return jsonify('Not following')

@app.route('/author/search',methods=['POST'])
@auth_required("token")
def author_search():
  user_id=current_user.id
  if request.method == 'POST':
    partial=request.json['partial']
    user_list = []
    if partial:
      user_list = Users.query.filter(Users.username.like(partial+"%")).all()
      if user_list:
        username_list=[]
        for user in user_list:
          if user.id==user_id:
            pass
          else:
            username_list.append({"id":user.id,"name":user.username})
        return username_list
      else:
        return jsonify('No such user')
    else:
      return []

@app.route('/author/post',methods=['GET','POST'])
@auth_required("token")
def author_posts():
  user_id=current_user.id
  username=current_user.username
  if request.method == 'GET':
    post=Posts.query.filter(Posts.author_id==user_id).all()
    if post:
      result=[]
      for i in range(len(post)):
        author=Users.query.filter(Users.id==post[i].author_id).first()
        paragraphs=[]
        paragraphs=((post[i].content.split('\\n')))
        result.append({"Title":post[i].title,"Content":paragraphs,"Date":post[i].date_created,"Date_m":post[i].date_modified,"Id":post[i].id})
        # print(result)
      return result
    else:
      return []
          
  if request.method == 'POST':
    title=request.json['title']
    content=request.json['content']
    date=datetime.datetime.now()
    post = Posts(title=title,content=content.replace('\n','\\n'),author_id=user_id)
    db.session.add(post)
    db.session.commit()
    return jsonify({"Title":title,"Content":content,"Author_id":user_id,"Date":date})

@app.route('/author/delete',methods=['POST'])
@auth_required("token")
def user_del():
  user_id=current_user.id
  username=current_user.username
  if request.method == 'POST':
    user=Users.query.filter(Users.id==user_id).first()
    if user:
      Users.query.filter(Users.id==user_id).delete()
      db.session.commit()
      return jsonify('Deleted successfully')
    else:
      return jsonify('No such user exists')

#Post Actions--------------------------------------------------------------------------
@app.route('/post',methods=['GET'])
@auth_required("token")
def posts():
  if request.method == 'GET':
    currid=current_user.id
    post=Posts.query.all()
    if post:
      result=[]
      for i in range(len(post)):
        author=Users.query.filter(Users.id==post[i].author_id).first()
        paragraphs=[]
        paragraphs=((post[i].content.split('\\n')))
        result.append({"currid":currid,"Title":post[i].title,"Content":paragraphs,"Author_name":author.username,"Date":post[i].date_created,"Date_m":post[i].date_modified,"post_d":post[i].id,"author_id":post[i].author_id})
      return result
    else:
      return []

@app.route('/author/post/<post_id>/delete',methods=['POST'])
@auth_required("token")
def posts_del(post_id):
  user_id=current_user.id
  username=current_user.username
  if request.method == 'POST':
    post=Posts.query.filter(Posts.id==post_id).first()
    if post:
      Posts.query.filter(Posts.id==post_id).delete()
      db.session.commit()
      return jsonify('Deleted successfully')
    else:
      return jsonify('No such post exists')

@app.route('/author/post/<post_id>/edit',methods=['GET','POST'])
@auth_required("token")
def posts_update(post_id):
  user_id=current_user.id
  username=current_user.username
  if request.method == 'GET':
    post=Posts.query.filter(Posts.id==post_id).first()
    if post:
      result=[]
      paragraphs=[]
      paragraphs=((post.content.split('\\n')))
      result.append({"title":post.title,"content":paragraphs,"Id":post.id})
      return result
  if request.method == 'POST':
    title=request.json['title']
    content=request.json['content']
    content=content.replace('\n','\\n')
    date=datetime.datetime.now()
    post=Posts.query.filter(Posts.id==post_id).first()
    post.title=title
    post.content=content
    post.date_modified=datetime.datetime.now()
    db.session.commit()
    return jsonify({"Title":title,"Content":content,"Author_id":user_id,"Date":date})
