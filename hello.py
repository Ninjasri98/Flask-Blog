from flask import Flask,render_template
app = Flask(__name__)
@app.route('/')
def index():
    fname = "John"
    st = "This is <strong> Bold </strong> text"
    fp = [2,34,56,67,90]
    return render_template("index.html",fname=fname,st=st,fp=fp)
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", uname = name)
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

