"""
Main module.

This is the main module where all the fun stuff happens.

Coding utf-8

Runtime: 
You have to have the file ".env" and put system-variables in terminal -
with commando: source .env
doublecheck you posess them: printenv
will make api-keys being placed in list with sys-var

Projectbased specifics : 
Coding-conventions - doubleline inbetween methods  
It is okay to use hanging indent + 1 blankline before method 
Even if not seen consistently as for now-
Future developers should declare variablenames with CamelCase

"""

import stripe #For stripe-payment and environment-variables
import os 
import datetime
import json
from flask import Flask, jsonify, abort, request, Response
from flask import Flask, render_template, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import (MetaData)
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_jwt_extended import (JWTManager, create_access_token, 
                                jwt_required, get_jwt_identity)
from forms import * #Imports everything from forms
from flask_login import (LoginManager, UserMixin, 
                        login_user, current_user,
                        logout_user, login_required)
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Mail, Message

metadata = MetaData()
app = Flask(__name__, static_folder='static', static_url_path='/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Declaration below is Very Dangerous - 
# future developers shoud look into masking "******"
app.config['SECRET_KEY'] = 'FHSGAJH48242T58GRTJ853FBIQVJ4B5IQU5H9G58G' 
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'lithemobler@gmail.com'
app.config['MAIL_PASSWORD'] = 'LITHEmobler2020'
mail = Mail(app)

stripe_keys = {
            'publishable_key': os.environ['STRIPE_PUBLISHABLE_KEY'].rstrip(),
            'secret_key': os.environ['STRIPE_SECRET_KEY'].rstrip()
            }
stripe.api_key= stripe_keys["secret_key"]

@login_manager.user_loader
def load_user(user_id):
    """Loading user based on passed on id
       
       Parameters:
       user_id (int) : 

       Returns:
       User(object)
    """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """ Used for maintaining users - cart_objects have a 1-2-many relationship
        
        Parameters: 
        db.Model - as for inheritance - necessity for database modelling
        UserMixin - as for inheritance - necessity for sessionbased handling
        
    """
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    email = db.Column(db.String, unique = True, nullable = False)
    password_hash = db.Column(db.String, nullable = False)
    address = db.Column(db.String, nullable = False)
    postalCode = db.Column(db.Integer, nullable = False)
    cart_objects =  db.relationship('Furniture', backref = 'user')
    requests =   db.relationship('Request', backref = 'user')

    def get_reset_token(self, expires_sec=1800):
        """ Reseting token with expiration for the calling object
            
            Parameters: 
            expires_sec(int) - set to 1800 seconds

            Returns:
            token(str)
            """
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8') #returns a token
    
    @staticmethod
    def verify_reset_token(token):
        """Verifying token and returning user based on token passed

        Parameters:
        token(int) - used to load id of user

        Returns:
        User(obj) based on id based on token

        Exceptions:
        InvalidTokenError(jwt.exception) - 
        Might raise InvalidTokenError when theapp cant load proper token
        """
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except jwt.InvalidTokenError:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return '<Användare {}: {} {}>'.format(self.id, self.name, self.email)

    def serialize(self):
        return dict(id = self.id, name = self.name, 
                    email = self.email, address = self.address, 
                    postalCode = self.postalCode)




class Furniture(db.Model):
    """Used for maintaining Furniture-objects in our db, 
    attribute user_id have a 1-2-many relationship

    Parameters: 
    db.Model(db) - as for inheritance - necessity for database modelling

    """
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    ldec = db.Column(db.Text, nullable = False)
    sdec = db.Column(db.Text, nullable = False)
    image = db.Column(db.String(20), nullable = False, default = 'default.jpg')
    category = db.Column(db.String, nullable = False)
    state = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Integer, nullable = False)
    colour = db.Column(db.String, nullable = False)
    width = db.Column(db.Integer, nullable = False)
    length = db.Column(db.Integer, nullable = False)
    height = db.Column(db.Integer, nullable = False)
    weight = db.Column(db.Integer, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Möbel {}: {} {} kr>'.format(self.id, self.name, 
                                            self.price, self.colour)
    
    def serialize(self): 
        return dict(id = self.id, name = self.name, 
                    ldec = self.ldec, sdec = self.sdec,
                    image = self.image, category = self.category, 
                    state = self.state, price = self.price, 
                    colour = self.colour, width = self.width,
                    length = self.length, height = self.height, 
                    weight = self.weight)


class Request(db.Model):
    """ For maintaining requests
        
        Parameters: 
        db.Model(db) - as for inheritance - necessity for database modelling

    """ 
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String, nullable = False)
    donation = db.Column(db.Boolean, nullable = False)
    transport = db.Column(db.Boolean, nullable = False)
    approved = db.Column(db.Boolean, default = False, nullable = False)
    year = db.Column(db.String, nullable = False)
    month = db.Column(db.String, nullable = False)
    day = db.Column(db.String, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
   
def get_Furniture(id): 
    """Helpfunction for functions removeObject,addToCart, exploreid
       
       Parameters:
       id(int) - used to check if furnitures attribute id is equal

       Returns:
       furniture(obj)
    """ 
    urnitures = Furniture.query.all()
    furniture = next(furniture for furniture in urnitures if furniture.id==id)
    return furniture

@app.route('/', methods =['GET'])
def home():
    return render_template("home.html")


@app.route('/checkout')
def checkout():
    """Calculates bought furnitures total price in 1/10 kr and renders checkout

       Parameters: None

       Returns:
       Checkout template with parameters stripe-key stated before imports 
       and calculated amount in 1/10 kr

    """
    furnitures = current_user.cart_objects
    amount= 100*sum(furniture.price for furniture in furnitures) # Amount in 1/10 kr
    return render_template('checkout.html', 
                            key = stripe_keys["publishable_key"], 
                            amount = amount , cart_objects = furnitures)


@app.route('/charge', methods=['POST'])
def charge():
    """Charging customer in 1/10 kr for all products put in customers cart
    
    Parameters: None

    Returns:
    Charge-template with parameters representing
     calculated amount and customers objects put in cart

    Exceptions:
    StripeError - might be raised due to previous inadecuate cookie-handling
    """
    try:
        amount= 100*sum(furniture.price for furniture in current_user.cart_objects) # amount i antal ören, därav ggr 100
        customer = stripe.Customer.create(email='spelaringenroll@mail.com', 
                                            source=request.form['stripeToken'])
        res = stripe.Charge.create(customer=customer.id, 
                                    amount=amount, currency='SEK', 
                                    receipt_email="felixelvjung1@gmail.com")
    except stripe.error.StripeError:
        return render_template("payment-error.html")

    if res.paid: #res.paid has type boolean hence this syntax
        boughtFurns = []
        ids = []
        for x in current_user.cart_objects:
            boughtFurns.append(x)
            ids.append(x.id)
        furns = Furniture.query.all()
        for x in furns:
            if x.id in ids:
                x.user=None
                db.session.delete(x)
        db.session.commit()
    return render_template('charge.html', amount=amount, furniture = boughtFurns)


@app.route('/explore', methods=['GET', 'POST']) 
def explore():
    """Rendering Explore-route with or without filter
    As for future developers: filtering method can easily be improved-
    future improvements could be utilizing Django´s filtering methods
    or direct SQL filtering - with the requirement of changing db-system
      
    Parameters: None

    Returns : 
    Explore-template with passed on filtered list in case of form being True
    Explore-template consisting of the whole db in case of form being False
    """
    form = FilterForm()
    filt_lista = []
    furnitures = Furniture.query.all()
    if form.filtrera.data:
        listan = ["Same"] * 20
        for (idx,val) in enumerate(form): #Converting form to list
            if idx==20:break
            if val.data: # val.data is a boolean field hence this syntax
                listan[idx] = val.description
        
        def all_same(listan):  # Helperfunction checking if all list elements are the same
            return all(checker == listan[0] for checker in listan)
        
        if form.maxprice.data is not None:
            maxprice = form.maxprice.data
        else:
            maxprice = 999_999_999

        if form.minprice.data is not None:
            minprice = form.minprice.data
        else:
            minprice = 0      
 
        for furniture in furnitures:
            if ((furniture.category in listan[:6] or all_same(listan[:6])) and
                (furniture.colour in listan[6:15] or all_same(listan[6:15])) and
                (furniture.state in listan[15:] or all_same(listan[15:])) and
                (minprice<furniture.price<maxprice)): 
                #If list-attributes(in case of not equal) exists for furniture object
                #and price within filtered range
                    filt_lista.append(furniture) 
        return render_template("explore.html", 
                                form = form,
                                furniture = filt_lista, user=current_user)
    return render_template("explore.html", 
                            form=form,
                            furniture = Furniture.query.all(),user=current_user)





@app.route('/removeFromObject/<int:id>', methods=['GET', 'POST'])
@login_required
def removeObject(id): 
    """Sets furniture's attribute user to None based on user-id
    
    Parameters: 
    id(int) - used for calling on helpermethod

    Returns:
    Redirecting to cart-route
    """
    get_Furniture(id).user = None
    db.session.commit()
    return redirect(url_for('cart'))


@app.route('/addToCart/<int:id>' , methods = ['POST'])
@login_required
def addToCart(id):
    """Setting given furniture´s attribute "user" as the current user
    Parameters: 
    id(int) - used for calling helpermethod

    Returns:
    Redirecting to explore-route
    """
    get_Furniture(id).user = current_user
    db.session.commit()
    return redirect(url_for('explore'))


@app.route('/explore/<int:id>', methods=['GET'])
def exploreid(id):
    """Rendering exploreid for furniture requested with id
    
    Parameters:
    id(int) - used for calling on helpermethod

    Returns:
    exploresid template with passed on QuestionForm, furniture based on par
    and current user (based on session)
    """
    form = QuestionForm()
    furniture = get_Furniture(id)
    return render_template("exploresid.html" , 
                            form = form, furniture = furniture,
                            user=current_user)


@app.route('/cart') 
@login_required
def cart():
    """Rendering the current users cart 
    
    Parameters: None

    Returns:
    cart-template with passed on cart for the session-based current_user
    """
    cart_objects = current_user.cart_objects
    return render_template("cart.html" , cart_objects = cart_objects)


@app.route('/contact', methods=['GET'])
def contact():
    """Rendering contact-template with questionform
    
    Parameters: None

    Returns:
    Contact-template with passed on QuestionForm
    """
    form = QuestionForm()
    if form.validate_on_submit():
        flash(f'Tack för din fråga, vi återkommer så fort vi vi kan!', 'success')
    return render_template("contact.html", form=form)
 

@app.route('/register', methods=['GET','POST'])
def register():
    """Registering user if not already authenticated
    
    Parameters: None
    
    Returns:
    Redirects to explore-template in case of user being authenticated
    Redirects to login-tempalte in case of  form-submit-button pressed
    Redirect to register-template in case of above statements -
    not being triggered

    """
    if current_user.is_authenticated:
        return redirect(url_for('explore'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data).decode('utf-8')
        newuser = User(
                       name = form.name.data, email = form.email.data,
                       password_hash = hashed_pw, address = form.address.data, 
                       postalCode = form.postalCode.data
                       )
        db.session.add(newuser)
        db.session.commit()
        flash(f'Konto skapat för {form.name.data}! \
                Du kan nu logga in.', 'success')
        return redirect(url_for('login'))

    return render_template("register.html", 
                            title = 'Registrera dig', form = form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logging in user if not authenticated
    
    Parameters: None

    Returns:
    Redirects to explore-route if user is authenticated
    or form submit button have been pressed on -
    the latter case is only triggered if first one is not
    
    Redirects to login-template in case of none of the above triggered 
    """
    if current_user.is_authenticated:
        return redirect(url_for('explore'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first() 
        if ((user is not None) and 
           (check_password_hash(user.password_hash, form.password.data))):
                login_user(user, remember = form.remember.data)
                return redirect(url_for('explore'))
        else:
            flash('Kunde inte logga in.', 'danger')
    
    return render_template("login.html", title = 'Logga in', form = form)


@app.route('/logout')
def logout():
    """Calling on logout function for user and rendering explore
    
    Parameters: None

    Returns:
    Redirecting to explore-route
    """
    logout_user()
    return redirect(url_for('explore'))


@app.route('/about')
def about():
    """Rendering about"""
    return render_template("about.html")


@app.route('/profile')
@login_required
def profile(): 
    """Rendering profile sending current user object
    
    Parameters: None

    Returns: 
    Profile-template with passed UpdateProfileForm and sess-based user
    """
    form = UpdateProfileForm()
    return render_template("profile.html", form = form, user = current_user)


@app.route('/profile/update', methods=['GET', 'POST'])
@login_required
def updateprofile(): 
    """Updating profile info with form if submitted
    
    Parameters: None

    Returns:
    Redirecting to explore route in case of form-submit-button pressed
    Redirecting to updateprofileinfo route if sub-button not pressed
    """
    form = UpdateProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.address = form.address.data
        current_user.postalCode = form.postalCode.data
        db.session.commit()
        flash('Dina uppgifter har uppdaterats', 'success')
        return redirect(url_for('profile'))
    else:
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.postalCode.data = current_user.postalCode
    return render_template("updateprofile.html", form=form)


@app.route('/profile/sell', methods = ['GET', 'POST'])
@login_required
def sellrequest(): 
    """This is where the user can send in their sell request
    
    Parameters: None

    Returns:
    Redirecting to profile-route if form has filled-in fields
    Redirecting to sell-route if the above is not triggered
    """
    form = SellRequestForm()
    if form.skicka.data: # form.skicka.data is boolean type hence this syntax
        time = datetime.datetime.now()
        request = Request(
                        category = form.category.data, 
                        donation = form.donation.data, 
                        transport = form.transportHelp.data, 
                        year = time.year, 
                        month = time.month, 
                        day = time.day 
                        )
        db.session.add(request)
        request.user = current_user
        db.session.commit()
        return redirect(url_for('profile'))
    return render_template("sell.html", form=form)


def send_reset_email(user):
    """Emailing reset-link for password to user as for testing
    
    Parameters:
    user(obj) - used to retrieve token

    Returns: None
    """
    token = user.get_reset_token()
    msg = Message(
                'Begäran att återställa lösenord', 
                sender='lithemobler@gmail.com', recipients=[user.email]
                )
    msg.body = f'''För att återställa ditt lösenord, följ bifogad länk:
            {url_for('reset_token', token=token, _external=True)}
            Om du inte vill byta lösenord, ignorera detta meddelande.'''
    mail.send(msg)



@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    """Reseting password
    
    Parameters: None

    Returns:
    Redirecting to explore route if user is authenticated
    Redirecting to login if above not triggered and form filled
    Redirecting to reset-request template if above ! triggered
    """
    if current_user.is_authenticated:
        return redirect(url_for('explore'))

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(
        'Ett email har skickats till dig angående återställning av lösenord')
        return redirect(url_for('login'))

    return render_template('reset_request.html',
                            title= 'Återställ lösenord', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    """Reseting password for user if correct token and form submitted
    
    Parameters:
    token(str) - used for retrieving userobject

    Returns:
    Redirecting to explore route if sessbased user is authenticated
    Redirecting to reset_request-route if no user found for token
    Redirecting to login-route if none above triggered an form filled
    Redirecting to reset-token template if none triggered
    """

    if current_user.is_authenticated:
        return redirect(url_for('explore'))
    user = User.verify_reset_token(token)
    if user is None: 
        flash('Ditt token är felaktigt eller gammalt', 'warning')
        return redirect(url_for('reset_request')) 
    form = ChangePasswordForm()
    if form.validate_on_submit():
        hashed_pw = generate_password_hash(form.password.data).decode('utf-8')
        user.password_hash = hashed_pw
        db.session.commit()
        flash('Ditt lösenord har ändrats! Du kan nu logga in.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', 
                            title= 'Återställ Lösenord', form=form)


@app.route('/registration')
def registration():
    """Rendering registration for users to register
    
    Parameters: None

    Returns: 
    Registration-template with passed on RegistrationForm
    """
    form = RegistrationForm()
    return render_template("registration.html", form = form)


@app.cli.command('resetDB')
def resetDB():
    """Reseting database method
    This method and methos below:
    are for resetting and creating database-  
    in gitbash: 
    $ export FLASK_APP=main.py
    $ python -i
    >>> import main
    >>> from main import resetDB
    >>> from main import createDB
    >>> exit()
    $ FLASK resetDB
    $ FLASK createDB
    """
    db.drop_all()
    db.create_all()
    print("Reset database successfully.")

@app.cli.command('createDB')
def createDB():
    """Creating database
    27 furnitures and 1 user are added
    """
    furn1 = Furniture(name = 'Svart matbord', ldec='Matbord med plats för 4 stolar', sdec='Matbord', image = 'matbord.jpg', category='Bord', state=5, price=500, colour="Svart", width=60, height=70, length=100, weight = 20)
    furn2 = Furniture(name = 'Beige säng', ldec='Queen-sized säng med huvudgavel från JYSK', sdec='Ställbar Kontinentalsäng', image = 'beige säng.jpeg', category='Säng', state=3, price=700, colour='Beige', width=160, height=50, length=200, weight = 50)
    furn3 = Furniture(name = 'Rosa fåtölj', ldec='Högkvalitativ fåtölj från danska designers Preben Sorenssen', sdec='Ergonomisk designfåtölj', image = 'röd fåtölj.jpg', category='Fåtölj', state=3, price=900, colour='Röd', width=55, height=70, length=50, weight = 25)
    furn4 = Furniture(name = 'Blå stol', ldec='Blå sammetsstol med svarta ben', sdec='Stol i sammet', image = 'blå stol.jpg', category='Stol', state=3, price=199, colour='Blå', width=45, height=45, length=80, weight = 7)
    furn5 = Furniture(name = 'Vit bokhylla', ldec='Stor bokhylla med mycket utrymme', sdec='Bokhylla i ek', image = 'bokhylla rik.jpg', category='Förvaring', state=5, price=3499, colour='Vit', width=120, height=220, length=30, weight = 60)
    furn6 = Furniture(name = 'Brun fåtölj', ldec='Retro fåtölj i äkta läder och stålfot', sdec='Fåtölj i läder', image = 'brun fåtölj.jpg', category='Fåtölj', state=1, price=499, colour='Brun', width=50, height=110, length=50, weight = 18)
    furn7 = Furniture(name = 'Byrå', ldec='Byrå i trä med stor förvaringskapacitet', sdec='Byrå i trä', image = 'byrålåda.jpeg', category='Förvaring', state=3, price=500, colour='Brun', width=90, height=120, length=60, weight = 30)
    furn8 = Furniture(name = 'Grå säng', ldec='Högkvalitativ säng med höj- och sänkfunktion från Mio', sdec='Ställbar kontinentalsäng', image = 'Fin säng.jpg', category='Säng', state=2, price=1199, colour='Grå', width=180, height=55, length=210, weight = 60)
    furn9 = Furniture(name = 'Grå fåtölj', ldec='Fåtölj i fint skick i mysigt material', sdec='Fåtölj i ullimitation', image = 'fluffig fotölj.jpg', category='Fåtölj', state=4, price=500, colour='Grå', width=70, height=100, length=60, weight = 14)
    furn10 = Furniture(name = 'Fåtölj med pall', ldec='Fåtölj från IKEA med matchande fotpall', sdec='Fåtölj-set', image = 'fotöljpall.jpg', category='Fåtölj', state=3, price=299, colour='Grå', width=60, height=90, length=100, weight = 20)
    furn11 = Furniture(name = 'Grå soffa', ldec='Soffa i mycket bra skick. Perfekt storlek för en mindre lägenhet/korridorsrum', sdec='2,5-sits med svarta stålben', image = 'grå soffa.jpg', category='Soffa', state=5, price=699, colour='Grå', width=150, height=70, length=60, weight = 30)
    furn12 = Furniture(name = 'Grön soffa', ldec='Större soffa i sammet. Litet tecken på slitage på vänster armstöd', sdec='3-sits i sammet', image = 'grön soffa.jpeg', category='Soffa', state=3, price=799, colour='Grön', width=180, height=80, length=70, weight = 40)
    furn13 = Furniture(name = 'Låg bokhylla', ldec='Bokhylla som även kan fungera som tv-möbel med smart förvaring', sdec='Vitlackerad bokhylla i trä', image = 'liten bokhylla.jpg', category='Förvaring', state=4, price=300, colour='Vit', width=130, height=70, length=40, weight = 25)
    furn14 = Furniture(name = 'Liten soffa', ldec='Soffa med plats för 2 personer', sdec='Soffa modell mindre', image = 'liten soffa.jpg', category='Soffa', state=1, price=500, colour='Svart', width=80, height=70, length=50, weight = 12)
    furn15 = Furniture(name = 'Byrå', ldec='Moderiktig byrå med liten skada på 2a lådan från botten', sdec='Cremefärgad byrå', image = 'möbelbyrå.jpeg', category='Förvaring', state=2, price=899, colour='Beige', width=80, height=100, length=50, weight = 30)
    furn16 = Furniture(name = 'Nattduksbord', ldec='Fint vitt nattduksbord i helt nytt skick', sdec='Nattduksbord i nyskick', image = 'nattduksbord.jpg', category='Förvaring', state=5, price=200, colour='Vit', width=40, height=30, length=30, weight = 4)
    furn17 = Furniture(name = 'Grå soffa', ldec='Mindre soffa med tecken på användning. Bra budgetval!', sdec='2-sits med träben', image = 'grå soffa2.jpg', category='Soffa', state=2, price=200, colour='Grå', width=100, height=60, length=50, weight = 19)
    furn18 = Furniture(name = 'Runt bord', ldec='Mindre matbord med plats för 4. Rödvinsfläck 20x20 cm mitt på bordet', sdec='Matbord i bok', image = 'runtbord.jpg', category='Bord', state=1, price=99, colour='Brun', width=70, height=65, length=70, weight = 15)
    furn19 = Furniture(name = 'Blå fåtölj', ldec='Blå sammetsfåtölj med mässingsben', sdec='Fåtölj i sammet', image = 'blå fåtölj.jpg', category='Fåtölj', state=4, price=500, colour='Blå', width=60, height=100, length=60 , weight = 15)
    furn20 = Furniture(name = 'Grå Säng', ldec='Säng i använt skick. Fläckig madrass', sdec='Säng med huvudgavel', image = 'grå säng.jpg', category='Säng', state=1, price=59, colour='Grå', width=140, height=60, length=200, weight = 25)
    furn21 = Furniture(name = 'Hylla i stål', ldec='Hylla med flera användningsområden. Kryddor, böcker, växter, bara fantasin sätter gränserna!', sdec='Hylla med svarta hyllplan', image = 'stålbokhylla.jpg', category='Förvaring', state=4, price=199, colour='Grå', width=3, height=10, length=10, weight = 50)
    furn22 = Furniture(name = 'Grå vardagsstol', ldec='En stol som passar perfekt som komplement till soffan i vardagsrummet!', sdec='Mindre stol i bra skick', image = 'grå stol.jpeg', category='Stol', state=5, price=299, colour='Grå', width=1, height=1, length=1.5, weight = 3)
    furn23 = Furniture(name = 'Svart fåtölj', ldec='En fin svart fåtölj i mocka som passar perfekt för ditt vardagsrum. Endast använd ett halvår och därmed i bra skick.', sdec='Fåtölj i mocka', image = 'svart fåtölj.jpg', category='Fåtölj', state=5, price=589, colour='Svart', width=150, height=150, length=150, weight = 50)
    furn24 = Furniture(name = 'Träbord', ldec='4-mannabord i ek för en billig peng.', sdec='Enkelt bord i ek', image = 'träbord.jpg', category='Bord', state=2, price=169, colour='Brun', width=150, height=150, length=200, weight = 50)
    furn25 = Furniture(name = 'Enkelsäng', ldec='En grå 90-säng perfekt för dig som vill slippa studentbostäders korridorssäng.', sdec='Justerbar grå säng', image = 'grå säng2.jpg', category='Säng', state=5, price=499, colour='Grå', width=0.9, height=90, length=200, weight = 20)
    furn26 = Furniture(name = 'Träbord', ldec='Ett stilrent bord i fint skick. Endast använd ett litet tag. Ett bord som passar perfekt till vardagsrummet.', sdec='Matbord i ek', image = 'träbord2.jpg', category='Bord', state=4, price=300, colour='Brun', width=150, height=120, length=250, weight = 10)
    furn27 = Furniture(name = 'Trästol', ldec='En stol perfekt för din balkong! Har använts i cirka ett år och har ytterst lite slitage.', sdec='Beige trästol med tillbehör', image = 'trästol.jpg', category='Stol', state=4, price=199, colour='Brun', width=1.5, height=1.5, length=1.5, weight = 10)

    hashed_pw = bcrypt.generate_password_hash("123123").decode('utf-8')
    newuser = User(name = "Test", email = "test@test.com", password_hash = hashed_pw, address = "Liu", postalCode = "58246")


    db.session.add_all([newuser,
                        furn1, furn2, furn3, 
                        furn4, furn5, furn6, 
                        furn7, furn8, furn9, 
                        furn10, furn11, furn12, 
                        furn13, furn14, furn15, 
                        furn16, furn17, furn18, 
                        furn19, furn20, furn21,
                        furn22, furn23, furn24, 
                        furn25, furn26, furn27]) 
    db.session.commit()

    print("created database sucsessfully.")


if  __name__ == "__main__":
    app.run(debug = True)
    
