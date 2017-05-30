import os
from . import main
from flask import render_template,flash,redirect,url_for,current_app,request
from form import NameForm,EditProfileAdminForm,EditForm
from flask.ext.login import current_user,login_required
from ..decorators import admin_required
from ..modles import User,Role,Post,Permission
from .. import db,moment
import random

@main.route('/upload', methods=['GET', 'POST'])
def upload(pageid):
	post = Post.query.filter_by(id=pageid).first()
	if request.method == 'GET':
		return render_template('upload.html')
	elif request.method == 'POST':
		f = request.files['file']
		fname = f.filename
		post.enclosurestore=fname
		db.session.add(post)
		db.session.commit()
		f.save('./static/'+fname)	
	return redirect(url_for('.index'))
@main.route('/edit',methods=['GET','POST'])
@login_required
@admin_required
def edit_admin():
	id = request.args.get('id')
	user = None
	if id is not None:
		user = Post.query.get(id)
	form = EditForm(user)
	if form.validate_on_submit():
		post = Post(title=form.title.data,body=form.ckeditor.data,author=current_user._get_current_object(),classify_id=form.classify.data)
		#if form.enclosure.data is not None:
		#	post.ifenclosure = True
		db.session.add(post)
		db.session.commit()
		#if post.ifenclosure:
		#	return redirect(url_for('.upload',pageid=post.id))
		posts = Post.query.filter_by(classify_id=3).order_by(Post.timestamp.desc()).all()
		news = Post.query.filter_by(classify_id=2).order_by(Post.timestamp.desc()).all()
		essays = Post.query.filter_by(classify_id=1).order_by(Post.timestamp.desc()).all()
		writings = Post.query.filter_by(classify_id=4).order_by(Post.timestamp.desc()).all()
		return redirect(url_for('.index',posts = posts,news=news,essays=essays,writings=writings))
	if user is not None:
		form.ckeditor.data = user.body
		form.title.data = user.title
		form.classify.data = user.classify_id
	return render_template('admin/edit.html',form=form)
@main.route('/delete',methods=['GET'])
@login_required
@admin_required
def delete():
	id = request.args.get('id')
	user = None
	if id is not None:
		user = Post.query.get(id)
	db.session.delete(user)
	db.session.commit()
	posts = Post.query.filter_by(classify_id=3).order_by(Post.timestamp.desc()).all()
	news = Post.query.filter_by(classify_id=2).order_by(Post.timestamp.desc()).all()
	essays = Post.query.filter_by(classify_id=1).order_by(Post.timestamp.desc()).all()
	writings = Post.query.filter_by(classify_id=4).order_by(Post.timestamp.desc()).all()
	return render_template('index.html',posts = posts,news=news,essays=essays,writings=writings)
@main.route('/ckupload/', methods=['POST', 'OPTIONS'])
def ckupload():
    form = EditForm()
    response = form.upload(endpoint=main)
    return response
@main.route('/')
def index():
	posts = Post.query.filter_by(classify_id=3).order_by(Post.timestamp.desc()).limit(15)
	news = Post.query.filter_by(classify_id=2).order_by(Post.timestamp.desc()).limit(15)
	essays = Post.query.filter_by(classify_id=1).order_by(Post.timestamp.desc()).limit(11)
	writings = Post.query.filter_by(classify_id=4).order_by(Post.timestamp.desc()).limit(11)
	return render_template('index.html',posts = posts,news=news,essays=essays,writings=writings)
@main.route('/page/<pageid>')
def page(pageid):
	post = Post.query.filter_by(id=pageid).first()
	if post is None:
		return render_template('404.html')
	return render_template('page.html',post=post)
@main.route('/user/<username>')
def user(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		abort(404)
	return render_template('admin/user.html',user=user)
@main.route('/edit-profile/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def edit_profile_admin(id):
	post = Post(title=form.title.data,body=form.ckeditor.data,author=current_user._get_current_object(),classify_id=form.classify.data,enclosure=form.enclosure.data)
	user = User.query.get_or_404(id)
	form = EditProfileAdminForm(user=user)
	if form.validate_on_submit():
		user.email = form.email.data
		user.username = form.username.data
		user.confirmed = form.confirmed.data
		user.role = Role.query.get(form.role.data)
		user.name = form.name.data
		user.location = form.location.data
		user.about_me = form.about_me.data
		db.session.add(user)
		flash('The profile has been updated.')
		return redirect(url_for('.user',username=user.username))
	form.email.data = user.email
	form.username.data = user.username
	form.confirmed.data = user.confirmed
	form.role.data = user.role_id
	form.name.data = user.name
	form.location.data = user.location
	form.about_me.data = user.about_me
	return render_template('admin/edit_profile.html',form=form,user=user)
@main.route('/posts')
def posts():
	posts = Post.query.filter_by(classify_id=3).order_by(Post.timestamp.desc()).all()
	return render_template('contents.html',posts=posts)
@main.route('/news')
def news():
	posts = Post.query.filter_by(classify_id=2).order_by(Post.timestamp.desc()).all()
	return render_template('contents.html',posts=posts)

@main.route('/essays')
def essays():
	posts = Post.query.filter_by(classify_id=1).order_by(Post.timestamp.desc()).all()
	return render_template('contents.html',posts=posts)

@main.route('/writings')
def writings():
	posts = Post.query.filter_by(classify_id=4).order_by(Post.timestamp.desc()).all()
	return render_template('contents.html',posts=posts)
