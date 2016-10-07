from flask import request, make_response, url_for, current_app
from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField, PasswordField
from wtforms.validators import Required, Length, Regexp, EqualTo,Email
from wtforms import ValidationError
from ..modles import User,Article,Role
import os, random, datetime

class CKEditor(object):
    def __init__(self):
        pass

    def gen_rnd_filename(self):
        """generate a random filename"""
        filename_prefix = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        return "%s%s" % (filename_prefix, str(random.randrange(1000, 10000)))

    def upload(self, endpoint=current_app):
        """img or file upload methods"""
        error = ''
        url = ''
        callback = request.args.get("CKEditorFuncNum")

        if request.method == 'POST' and 'upload' in request.files:
            # /static/upload
            fileobj = request.files['upload']
            fname, fext = os.path.splitext(fileobj.filename)
            rnd_name = '%s%s' % (self.gen_rnd_filename(), fext)

            filepath = os.path.join(endpoint.static_folder, 'upload', rnd_name)

            dirname = os.path.dirname(filepath)
            if not os.path.exists(dirname):
                try:
                    os.makedirs(dirname)
                except:
                    error = 'ERROR_CREATE_DIR'
            elif not os.access(dirname, os.W_OK):
                    error = 'ERROR_DIR_NOT_WRITEABLE'
            if not error:
                fileobj.save(filepath)
                url = url_for('main.static', filename='%s/%s' % ('upload', rnd_name))
        else:
            error = 'post error'

        res = """
                <script type="text/javascript">
                window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
                </script>
             """ % (callback, url, error)

        response = make_response(res)
        response.headers["Content-Type"] = "text/html"
	return response

class EditForm(Form, CKEditor):
	classify = SelectField('Classify',coerce=int)
	title = StringField('Title',validators=[Required(),Length(1,128)])
	ckeditor = TextAreaField()
	submit = SubmitField('Submit')
	def __init__(self,user,*args,**kwargs):
		super(EditForm,self).__init__(*args,**kwargs)
		self.classify.choices = [(classify.id,classify.name)for classify in Article.query.order_by(Article.name).all()]
		self.user = user

class NameForm(Form):
	submit = SubmitField('Submit')

class EditProfileAdminForm(Form):
	email = StringField('Email',validators=[Required(),Length(1,64),Email()])
	username = StringField('Username',validators=[Required(),Length(1,64)])
	confirmed = BooleanField('Confirmed')
	role = SelectField('Role',coerce=int)
	name = StringField('Real name',validators=[Length(0,64)])
	location = StringField('Location',validators=[Length(0,64)])
	about_me = TextAreaField('About me')
	submit = SubmitField('Submit')
	
	def __init__(self,user,*args,**kwargs):
		super(EditProfileAdminForm,self).__init__(*args,**kwargs)
		self.role.choices = [(role.id,role.name)for role in Role.query.order_by(Role.name).all()]
		self.user = user

	def validate_email(self,field):	
		if field.data != self.user.email and User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')

	def validate_username(self,field):
		if field.data != self.user.username and user.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in use.')
