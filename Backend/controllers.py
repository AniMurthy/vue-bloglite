from flask import Flask,request,jsonify,send_file
import datetime

import flask_excel as excel
import csv

from io import BytesIO

from sqlalchemy import null
from models import *
from flask_security import auth_required
from flask import current_app as app

from main import cache

from flask_login import current_user

import base64

from workers import *
import tasks
from template import *




# Author Actions ------------------------------------------------------------

@cache.cached(timeout=10,key_prefix="get_auth_details")
def get_auth_details():
  user_id=current_user.id
  author=Users.query.filter(Users.id==user_id).first()
  posts=len(Posts.query.filter(Posts.author_id==user_id).all())
  follow=len(Followers.query.filter(Followers.user_id==user_id).all())
  following=len(Followers.query.filter(Followers.following_id==user_id).all())
  return author,posts,follow,following

#returns the info about the currnt user
@app.route('/author',methods=['GET'])
@auth_required("token")
def authors():
  user_id=current_user.id
  username=current_user.username
  if request.method == 'GET':
    # author=Users.query.filter(Users.id==user_id).first()
    author,posts,follow,following=get_auth_details()
    # posts=len(Posts.query.filter(Posts.author_id==user_id).all())
    # follow=len(Followers.query.filter(Followers.user_id==user_id).all())
    # following=len(Followers.query.filter(Followers.following_id==user_id).all())
    # pic = base64.b64encode(Users.profile_pic).decode('utf-8')
    if author==None:
      return jsonify('Author doesn\'t exist ')
    else:
      return jsonify({"Name":author.username,"Author_id":author.id,"Author_Email":author.email,"no_follows":follow,"no_posts":posts,"no_following":following})

# @app.route('/author/pic',methods=['GET','POST'])
# @auth_required("token")
# def authors_profile_pic():
#   user_id=current_user.id
#   username=current_user.username
#   if request.method == 'GET':
#     pic = base64.b64encode(Users.query.filter(Users.id==user_id).first().profile_pic).decode('utf-8')
#     print(pic)
#     return jsonify({"pic":pic})

#returns the info about the user with the given id
@app.route('/author/profile/<id>',methods=['GET'])
@auth_required("token")
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

#returns the users following the current user
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
    if follow==None:
      return jsonify('Following don\'t exist ')
    else:
      return follow

#returns the users the current user is following   
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
    if follow==None:
      return jsonify('Following don\'t exist ')
    else:
      return follow

#used to follow another user
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

#used to unfollow another user
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

#used to search for users
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
          if user.id!=user_id:
            followMe=bool(Followers.query.filter(Followers.following_id==user.id).filter(Followers.user_id==user_id).first())
            username_list.append({"id":user.id,"name":user.username,"following":followMe})
            print(username_list)
        return username_list
      else:
        return jsonify('No such user')
    else:
      return []

#the "GET" method returns all the posts of the current user
#the  "POST" method used to create a new post by current user
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
      return result
    else:
      return []
  if request.method == 'POST':
    title=request.json['title']
    content=request.json['content']
    date=datetime.datetime.now()
    post = Posts(title=title,content=content.replace('\n','\\n'),author_id=user_id,date_created=date)
    db.session.add(post)
    db.session.commit()
    return jsonify({"Title":title,"Content":content,"Author_id":user_id,"Date":date})

#used to delete current user account
@app.route('/author/delete',methods=['POST'])
@auth_required("token")
def user_del():
  user_id=current_user.id
  if request.method == 'POST':
    user=Users.query.filter(Users.id==user_id).first()
    if user:
      temp=Followers.query.filter(Followers.user_id==user_id).all()
      if temp:
        Followers.query.filter(Followers.user_id==user_id).delete()
      temp=Followers.query.filter(Followers.following_id==user_id).all()
      if temp:
        Followers.query.filter(Followers.following_id==user_id).delete()
      temp=Posts.query.filter(Posts.author_id==user_id).all()
      if temp:
        Posts.query.filter(Posts.author_id==user_id).delete()
      Users.query.filter(Users.id==user_id).delete()
      db.session.commit()
      return jsonify('Deleted successfully')
    else:
      return jsonify('No such user exists')

#Post Actions--------------------------------------------------------------------------

#returns all the posts by all the users for the feed page
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

#used to delete the post with "post_id" of the current user
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

#used to edit the post with "post_id" of the current user
#the "get" method returns the currently populated values of title and content
#the "post" method edits the new values to the database
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

#celery jobs-------------------------------------------------------------------------------

#----------------------------Creates a CSV file which is downloadable
@app.route('/DownloadCSV',methods=['GET'])
@auth_required("token")
def downloadcsv():
  user_id=current_user.id
  username=current_user.username
  if request.method == 'GET':
    posts=Posts.query.filter(Posts.author_id==user_id).all()
    author=Users.query.filter(Users.id==user_id).first()
    d1=[['Title','Content','Date created','Date modified']]
    if posts:
      for i in range(len(posts)):
        post=[]
        post.append(posts[i].title)
        post.append(posts[i].content)
        post.append(posts[i].date_created)
        if posts[i].date_modified:
          post.append(posts[i].date_modified)
        else:
          post.append('Not modified')
        d1.append(post)
    extension_type = "csv"
    filename = "../data/"+username + "." + extension_type
    tasks.downloadcsv.delay(d1,filename,current_user.email)
    return jsonify("Successfully created CSV")

#----------------------------creates a downloadable PDF report
@app.route('/report',methods=['GET'])
@auth_required("token")
def pdf_report():
  user_id=current_user.id
  username=current_user.username
  if request.method == 'GET':
    posts=Posts.query.filter(Posts.author_id==user_id).all()
    post=len(Posts.query.filter(Posts.author_id==user_id).all())
    follow=len(Followers.query.filter(Followers.user_id==user_id).all())
    following=len(Followers.query.filter(Followers.following_id==user_id).all())
    data={}
    data["id"]=user_id
    data["username"]=username
    data["followers_no"]=follow
    data["following_no"]=following
    data["no_posts"]=post
    result=[]
    if posts:
      for i in range(len(posts)):
        paragraphs=[]
        paragraphs=((posts[i].content.split('\\n')))
        result.append({"Title":posts[i].title,"Content":paragraphs,"Date":posts[i].date_created,"Date_m":posts[i].date_modified})
    data["posts"]=result
    create_pdf(data,username)
    file_name=str("../data/"+username)+".pdf"
    tasks.pdf.delay(current_user.email,file_name)
    return jsonify("Successfully created PDF")

@app.route('/reminder',methods=['GET'])
@auth_required("token")
def rem():
  res = tasks.daily_rem.delay()
  # job=tasks.hello.delay()
  return str(res),200
#----------------------------------------------END OF FILE-----------------------------------------------------------