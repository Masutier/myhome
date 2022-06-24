from datetime import datetime
from flask import Flask, render_template as render, request, url_for, flash, redirect

from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config.update(
    TESTING=True,
    SECRET_KEY='e26bdc3e748d7f82df50d57443ab7607bfb65fd470e058323a66bb75af4c9d36'
)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myhome.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# models
class Buy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    toBuy = db.Column(db.String(150), nullable=False)
    status = db.Column(db.Boolean, default=True)
    dateStart = db.Column(db.DateTime, default=datetime.utcnow)
    dateEnd = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __repr__(self):
        return self.toBuy


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    todo = db.Column(db.String(180), nullable=False)
    dateStart = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    dateEnd = db.Column(db.DateTime, nullable=True, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return self.todo


class Receta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video = db.Column(db.string(100), nullable=False)

    def __repr__(self):
        return self.todo


# Home
@app.route('/')
def home():

    objBuy = Buy.query.filter_by(status='1')
    objBuycount = 0
    for obj in objBuy:
        objBuycount += 1

    objHist = Buy.query.filter_by(status='0')
    objHistcount = 0
    for obj in objHist:
        objHistcount += 1

    objDoit = Todo.query.all()
    objDoitount = 0
    for obj in objDoit:
        objDoitount += 1

    return render("home.html", objBuycount=objBuycount, objDoitount=objDoitount, objHistcount=objHistcount)


# Buy It
@app.route('/buyit')
def buyit():
    objBuy = Buy.query.filter_by(status='1')

    return render("buyit.html", objBuy=objBuy)


@app.route('/createbuyit', methods=["GET", "POST"])
def createbuyit():
    action = None
    form = InputForm()
    # Validate form
    if form.validate_on_submit():
        toBuying = Buy(toBuy=form.action.data)
        db.session.add(toBuying)
        db.session.commit()
        form.action.data = ''
        flash("El Articulo Fue Agregado Correctamente")
        return redirect(url_for('buyit'))

    return render("createbuyit.html", action=action, form=form)


@app.route('/updatebuyit/<int:id>', methods=['GET', 'POST'])
def updatebuyit(id):
    form = InputForm()
    buyObj = Buy.query.get_or_404(id)
    if request.method == "POST":
        buyObj.toBuy = request.form["action"]
        db.session.commit()
        form.action.data = ''
        flash("El Articulo Fue Modificado")
        return redirect(url_for('buyit'))
    else:
        return render("updatebuyit.html", form=form, buyObj=buyObj)


@app.route('/deletebuyit/<int:id>', methods=['GET', 'POST'])
def deletebuyit(id):
    buyObj = Buy.query.get_or_404(id)
    try:
        db.session.delete(buyObj)
        db.session.commit()
        flash("El Articulo Fue Eliminado Del Todo")
        return redirect(url_for('buyit'))
    except:
        flash("Ups!!! Algo salio mal, Intentalo otra vez")
        return redirect(url_for('buyit'))

    return redirect('home')


# Do It
@app.route('/doit')
def doit():
    objDoit = Todo.query.all()

    return render("doit.html", objDoit=objDoit)


@app.route('/createdoit', methods=["GET", "POST"])
def createdoit():
    action = None
    form = InputForm()
    # Validate form
    if form.validate_on_submit():
        toDoing = Todo(todo=form.action.data)
        db.session.add(toDoing)
        db.session.commit()
        form.action.data = ''
        flash("La Tarea Fue Agregada Correctamente")
        return redirect(url_for('doit'))

    return render("createdoit.html", action=action, form=form)


@app.route('/updatedoit/<int:id>', methods=['GET', 'POST'])
def updatedoit(id):
    form = InputForm()
    objDoit = Todo.query.get_or_404(id)
    if request.method == "POST":
        objDoit.todo = request.form["action"]
        db.session.commit()
        form.action.data = ''
        flash("La Tarea Se Modifico")
        return redirect(url_for('doit'))
    else:
        return render("updatedoit.html", form=form, objDoit=objDoit)


@app.route('/deletedoit/<int:id>', methods=['GET', 'POST'])
def deletedoit(id):
    objDoit = Todo.query.get_or_404(id)
    try:
        db.session.delete(objDoit)
        db.session.commit()
        flash("La Tarea Fue Eliminada Del Todo")
        return redirect(url_for('doit'))
    except:
        flash("Ups!!! Algo salio mal, Intentalo otra vez")
        return redirect(url_for('doit'))

    return redirect('home')


@app.route("/historyBuy")
def historyBuy():
    history = Buy.query.filter_by(status='0')

    return render('historyBuy.html', history=history)


@app.route("/closeBuy")
def closeBuy():
    buyObj = Buy.query.filter_by(status='1')
    if not buyObj:
        flash("No Items en la lista!")
        return redirect(url_for('buyit'))
    else:
        for item in buyObj:
            item.status = 0
            item.dateEnd = datetime.now()
            db.session.commit()
        flash("Items en lista de Historia!")

        #email
        # subject = 'Lista de compras', currentdate
        # template = render_to_string('mail/buyList.html', context={'buyObj':buyObj})
        # template_message = strip_tags(template)
        # from_email = settings.EMAIL_HOST_USER
        # to = [settings.EMAIL_TO]
        # mail.send_mail(subject, template_message, from_email, to, html_message=template)
        # flash("Email was sent!")

        return render("historyBuy.html", buyObj=buyObj)


app.route('/recetas')
def recetas():

    return


app.route('\createreceta')
def createreceta():

    return

# Forms
class InputForm(FlaskForm):
    action = StringField("Tu Entrada", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UpdateBuyForm(FlaskForm):
    action = StringField("Tu Entrada", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Errors
@app.errorhandler(404)
def page_not_found(e):

    return render("errors/404.html"), 404

@app.errorhandler(500)
def internal_server(e):

    return render("errors/500.html"), 500
