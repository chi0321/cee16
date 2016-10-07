import os
from . import main
from flask import render_template,flash,redirect,url_for,current_app,request
from form import NameForm,EditProfileAdminForm,EditForm
from flask.ext.login import current_user,login_required
from ..decorators import admin_required
from ..modles import User,Role,Post,Permission
from .. import db,moment
import random

@main.route('/edit',methods=['GET','POST'])
@login_required
@admin_required
def edit_admin():
	id = request.args.get('id')
	post = None
	if id is not None:
		post = Post.query.get(id)
	else:
		post = Post()
	form = EditForm(post)
	if form.validate_on_submit():
		post.title=form.title.data
		post.body=form.ckeditor.data
		post.author=current_user._get_current_object()
		post.classify_id=form.classify.data
		db.session.add(post)
		db.session.commit()
		posts = Post.query.filter_by(classify_id=3).order_by(Post.timestamp.desc()).all()
		news = Post.query.filter_by(classify_id=2).order_by(Post.timestamp.desc()).all()
		essays = Post.query.filter_by(classify_id=1).order_by(Post.timestamp.desc()).all()
		writings = Post.query.filter_by(classify_id=4).order_by(Post.timestamp.desc()).all()
		return redirect(url_for('.index',posts = posts,news=news,essays=essays,writings=writings))
	if post is not None:
		form.ckeditor.data = post.body
		form.title.data = post.title
		form.classify.data = post.classify_id
	return render_template('admin/edit.html',form=form)
@main.route('/ckupload/', methods=['POST', 'OPTIONS'])
def ckupload():
    form = EditForm()
    response = form.upload(endpoint=main)
    return response
@main.route('/')
def index():
	page = request.args.get('page',1,type=int)
	posts = Post.query.filter_by(classify_id=3).order_by(Post.timestamp.desc()).paginate(
		page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE_1'],error_out=False).items
	news = Post.query.filter_by(classify_id=2).order_by(Post.timestamp.desc()).paginate(
		page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE_1'],error_out=False).items
	essays = Post.query.filter_by(classify_id=1).order_by(Post.timestamp.desc()).paginate(
		page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE_2'],error_out=False).items
	writings = Post.query.filter_by(classify_id=4).order_by(Post.timestamp.desc()).paginate(
		page,per_page=current_app.config['FLASKY_POSTS_PER_PAGE_2'],error_out=False).items
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
