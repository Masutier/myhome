from datetime import datetime
from flask import Flask, render_template as render, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update(
    TESTING=True,
    SECRET_KEY='e26bdc3e748d7f82df50d57443ab7607bfb65fd470e058323a66bb75af4c9d36'
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myhome.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/')
def home():

    return render("home.html")


@app.route('/doit')
def doit():

    return render("doit.html")


@app.route('/createdoit')
def createdoit():

    return render("createdoit.html")


@app.route('/updatedoit')
def updatedoit():

    return render("updatedoit.html")


@app.route('/deletedoit')
def deletedoit():

    return


@app.route('/buyit')
def buyit():

    return render("buyit.html")


@app.route('/createbuyit')
def createbuyit():

    return render("createbuyit.html")


@app.route('/updatebuyit')
def updatebuyit():

    return render("updatebuyit.html")


@app.route('/deletebuyit')
def deletebuyit():

    return


@app.errorhandler(404)
def page_not_found(e):

    return render("errors/404.html"), 404

@app.errorhandler(500)
def internal_server(e):

    return render("errors/500.html"), 500