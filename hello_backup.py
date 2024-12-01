from flask import Flask,render_template,flash,request,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,ValidationError
from wtforms.validators import DataRequired,EqualTo,Length
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, create_engine,DateTime,Text
from datetime import datetime,timezone,date
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash,check_password_hash
from wtforms.widgets import TextArea
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Mysql6969%40@localhost/usersdb'
app.config['SECRET_KEY'] = "password"
db = SQLAlchemy(app)
migrate = Migrate(app,db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

class users(db.Model,UserMixin):
    id = Column(Integer,primary_key=True)
    username = Column(String(20),nullable=False,unique=True)
    name = Column(String(200),nullable=False)
    email =  Column(String(120),nullable=False,unique=True)
    favourite_color = Column(String(120),nullable=True)
    date_added = Column(DateTime,default=lambda: datetime.now(timezone.utc))
    password_hash = Column(String(128))
    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute ")
    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
    def __repr__(self):
        return '<Name %r>' % self.name
"""if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Successful")
        """
class posts(db.Model):
    id = Column(Integer,primary_key=True)
    title = Column(String(255))
    content = Column(Text)
    author = Column(String(255))
    date_posted = Column(DateTime,default=datetime.now(timezone.utc))
    slug = Column(String(255))
class PostForm(FlaskForm):
    title = StringField("Title",validators=[DataRequired()])
    author = StringField("Author",validators=[DataRequired()])
    content = StringField("Content",validators=[DataRequired()],widget=TextArea())
    slug = StringField("Slug",validators=[DataRequired()])
    submit = SubmitField("Submit")
    
class UserForm(FlaskForm):
    name = StringField("Name ",validators=[DataRequired()])
    username = StringField("User Name ",validators=[DataRequired()])
    email = StringField("Email ",validators=[DataRequired()])
    favourite_color = StringField("Favourite Color")
    password_hash = PasswordField("Password",validators=[DataRequired(),EqualTo("password_hash2",message="Passwords must match")])
    password_hash2 = PasswordField("Confirm Password",validators=[DataRequired()])
    submit = SubmitField("Submit")
class NamerForm(FlaskForm):
    name = StringField("What is your name? ",validators=[DataRequired()])
    submit = SubmitField("Submit")
class PasswordForm(FlaskForm):
    email = StringField("What is your Email? ",validators=[DataRequired()])
    password_hash = PasswordField("What is your password? ",validators=[DataRequired()])
    submit = SubmitField("Submit")
class LoginForm(FlaskForm):
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    submit = SubmitField("Submit")
@app.route('/add_post',methods=['GET','POST'])
@login_required
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        post = posts(title=form.title.data,author=form.author.data,slug=form.slug.data,content=form.content.data)
        form.title.data = ''
        form.author.data = ''
        form.slug.data = ''
        form.content.data = ''
        db.session.add(post)
        db.session.commit()
        flash("Blog Post Added Successfully")
    return render_template("add_post.html",form=form)
@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        
        user = users.query.filter_by(username=form.username.data).first()
        
        if user:
            if check_password_hash(user.password_hash,form.password.data):
                
                login_user(user)
                flash("Login Successful")
                return redirect(url_for('dashboard'))
            else:
               
                flash("Wrong Password. Please Try Again")
        else:
           
            flash("Username does not exist. Try Again")
   
    return render_template("login.html",form=form)
@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out")
    return redirect(url_for('login'))
@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    name_to_update = users.query.get_or_404(id)
    if request.method == 'POST' :
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favourite_color = request.form['favourite_color']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("User updated successfully ")
            return render_template("dashboard.html",form=form,name_to_update=name_to_update)
        except:
            flash("Error!! Please Try again ")
            return render_template("dashboard.html",form=form,name_to_update=name_to_update)
    else:
        return render_template("dashboard.html",form=form,name_to_update=name_to_update,id=id)

    
    
@app.route('/posts')
def post():
    post = posts.query.order_by(posts.date_posted)
    return render_template("posts.html",post = post)
@app.route('/posts/<int:id>')
def ind_post(id):
    post = posts.query.get_or_404(id)
    return render_template("post.html",post = post)
@app.route('/post/edit/<int:id>',methods=['GET','POST'])
@login_required
def edit_post(id):
    post = posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        db.session.add(post)
        db.session.commit()
        flash("Post Updated Successfully")
        return redirect(url_for('post',id=post.id))
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content
    return render_template("edit_post.html",form=form)
@app.route('/post/delete/<int:id>')
def delete_post(id):
    post_to_delete = posts.query.get_or_404(id)
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Post Deleted Successfully")
        post = posts.query.order_by(posts.date_posted)
        return render_template("posts.html",post = post)
    except:
        flash("There was an error in deleting the post..Try Again")
        post = posts.query.order_by(posts.date_posted)
        return render_template("posts.html",post = post)


@app.route('/date')
def get_curr():
    return{"Date": date.today()}
@app.route('/delete/<int:id>')
def delete(id):
    name = None
    form = UserForm()
    name_to_delete = users.query.get_or_404(id)
    try:
        db.session.delete(name_to_delete)
        db.session.commit()
        flash("User Deleted Successfully ")
        our_users = users.query.order_by(users.date_added)    
        return render_template("add_user.html",form=form,name= name,our_users=our_users)

        
    except:
        flash("There was an error in deleting the user. Please Try again")
        our_users = users.query.order_by(users.date_added)    
        return render_template("add_user.html",form=form,name= name,our_users=our_users)


@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    form = UserForm()
    name_to_update = users.query.get_or_404(id)
    if request.method == 'POST' :
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favourite_color = request.form['favourite_color']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("User updated successfully ")
            return render_template("update.html",form=form,name_to_update=name_to_update)
        except:
            flash("Error!! Please Try again ")
            return render_template("update.html",form=form,name_to_update=name_to_update)
    else:
        return render_template("update.html",form=form,name_to_update=name_to_update,id=id)

@app.route('/')
def index():
    fname = "John"
    st = "This is <strong> Bold </strong> text"
    fp = [2,34,56,67,90]
    return render_template("index.html",fname=fname,st=st,fp=fp)
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name = name)
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500
@app.route('/name',methods=['GET','POST'])
def name():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
        flash("Form Submitted Successfully ")
    return render_template("name.html",name = name,form = form)
@app.route('/test_pw',methods=['GET','POST'])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        form.email.data = ""
        form.password_hash.data = ""
        pw_to_check = users.query.filter_by(email=email).first()
        passed = check_password_hash(pw_to_check.password_hash,password)
    return render_template("test_pw.html",email = email,password=password,pw_to_check=pw_to_check,passed=passed,form = form)
@app.route('/user/add',methods=['GET','POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data, method='pbkdf2:sha256')
            user = users(name=form.name.data,username=form.username.data,email=form.email.data,favourite_color=form.favourite_color.data,password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ""
        form.username.data = ""
        form.email.data = ""
        form.favourite_color.data = ""
        form.password_hash.data = ""
        flash("User Added Successfully")
    our_users = users.query.order_by(users.date_added)    
    return render_template("add_user.html",form=form,name= name,our_users=our_users)


