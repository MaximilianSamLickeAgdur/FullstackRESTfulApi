
from flask import Flask, jsonify, abort, request, Response
from flask import Flask, render_template, redirect, flash, url_for
from flask_login import login_user, logout_user, current_user, login_required
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField, TextField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'


@app.route('/')
def layout():
   
    form = FilterForm()
    return render_template("explore.html", form = form, furniture = furniture)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template("login.html", form = form)

@app.route('/request')
def request():
    return render_template("request.html")

@app.route('/konto')
def konto():
    form = UpdateForm()
    return render_template("konto.html", form = form)

@app.route('/contact')
def contact():
    return render_template("contact.html")

class LoginForm(FlaskForm):
       username = StringField('Emailaddress', validators=[DataRequired(), Email()])
       password = PasswordField('Lösenord', validators=[DataRequired()])
       submit = SubmitField('Logga in')
       remember = BooleanField('Kom ihåg mig')

class FilterForm(FlaskForm):

        category1 = BooleanField('Stolar') 
        category2 = BooleanField('Soffor') 
        category3 = BooleanField('Sängar') 
        category4 = BooleanField('Bord') 
        category5 = BooleanField('Fotöljer') 
        category4 = BooleanField('Bord') 
        category5 = BooleanField('Fåtöljer') 
        category6 = BooleanField('Förvaring') 
        color1 = BooleanField('Svart')    
        color2 = BooleanField('Vit')    
        color3 = BooleanField('Brun')    
        color4 = BooleanField('Grön')
        color5 = BooleanField('Gul')    
        color6 = BooleanField('Blå')    
        color7 = BooleanField('Röd')    
        color8 = BooleanField('Beige')   
        condition1 = BooleanField('Nyskick')
        condition2 = BooleanField('Bra skick')
        condition3 = BooleanField('Helt ok')
        condition4 = BooleanField('Lite sliten')
        condition5 = BooleanField('Mycket sliten')
        maxprice = IntegerField('Max pris')
        minprice = IntegerField('Min pris')
        filtrera = SubmitField('Filtrera')


class UpdateForm(FlaskForm):

    name = StringField('Förnamn')
    surname = StringField('Efternamn')
    email = StringField('Email')
    adress = StringField('Adress')
    ort = StringField('Ort')
    code = StringField('Postnummer')
    submit = SubmitField('Uppdatera personuppgifter')


# class Furn(db.model):
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String, nullable = False)
#     condition = db.Column(db.String, nullable = False)
#     material = db.Column(db.String, nullable = False)
#     image = db.Column(db.String, nullable = False)

if  __name__ == "__main__":
    app.run(debug = True)
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
=======
    
=======
=======
>>>>>>> Sebellen
=======
=======
>>>>>>> Sam
from flask import Flask, jsonify, abort, request, Response
from flask import Flask, render_template, redirect, flash, url_for
from flask_login import login_user, logout_user, current_user, login_required
from wtforms import StringField, SubmitField, PasswordField, BooleanField, IntegerField, TextField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'


@app.route('/')
def layout():
   
    form = FilterForm()
    return render_template("explore.html", form = form, furniture = furniture)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template("login.html", form = form)

@app.route('/request')
def request():
    return render_template("request.html")

@app.route('/konto')
def konto():
    form = UpdateForm()
    return render_template("konto.html", form = form)

@app.route('/contact')
def contact():
    return render_template("contact.html")

class LoginForm(FlaskForm):
       username = StringField('Emailaddress', validators=[DataRequired(), Email()])
       password = PasswordField('Lösenord', validators=[DataRequired()])
       submit = SubmitField('Logga in')
       remember = BooleanField('Kom ihåg mig')

class FilterForm(FlaskForm):

        category1 = BooleanField('Stolar') 
        category2 = BooleanField('Soffor') 
        category3 = BooleanField('Sängar') 
        category4 = BooleanField('Bord') 
        category5 = BooleanField('Fotöljer') 
        category4 = BooleanField('Bord') 
        category5 = BooleanField('Fåtöljer') 
        category6 = BooleanField('Förvaring') 
        color1 = BooleanField('Svart')    
        color2 = BooleanField('Vit')    
        color3 = BooleanField('Brun')    
        color4 = BooleanField('Grön')
        color5 = BooleanField('Gul')    
        color6 = BooleanField('Blå')    
        color7 = BooleanField('Röd')    
        color8 = BooleanField('Beige')   
        condition1 = BooleanField('Nyskick')
        condition2 = BooleanField('Bra skick')
        condition3 = BooleanField('Helt ok')
        condition4 = BooleanField('Lite sliten')
        condition5 = BooleanField('Mycket sliten')
        maxprice = IntegerField('Max pris')
        minprice = IntegerField('Min pris')
        filtrera = SubmitField('Filtrera')


class UpdateForm(FlaskForm):

    name = StringField('Förnamn')
    surname = StringField('Efternamn')
    email = StringField('Email')
    adress = StringField('Adress')
    ort = StringField('Ort')
    code = StringField('Postnummer')
    submit = SubmitField('Uppdatera personuppgifter')


# class Furn(db.model):
#     id = db.Column(db.Integer, primary_key = True)
#     name = db.Column(db.String, nullable = False)
#     condition = db.Column(db.String, nullable = False)
#     material = db.Column(db.String, nullable = False)
#     image = db.Column(db.String, nullable = False)

if  __name__ == "__main__":
    app.run(debug = True)
<<<<<<< HEAD
=======
>>>>>>> Jonte
    
>>>>>>> Sam
