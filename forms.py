"""
Forms module.

This is where all the forms used in main are created.

Classes:
QuestionForm - used for users to publish questions to us
LoginForm - used for logging in users
UpdateProfileForm - for a user to update Profile information
SellRequestForm - for users to send us sellrequests
RequestResetForm - 
ChangePasswordForm - For a user to change their password
FilterForm - For filtering the explore-page

"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, PasswordField, 
                    SubmitField, BooleanField, 
                    IntegerField, SelectField)
from wtforms.validators import (DataRequired, Length,
                                Email, EqualTo, ValidationError)
from main import * #should be able to just import User, but it raises an error.
from flask_login import current_user



class RegistrationForm(FlaskForm):
    """Used for users data-input in registering process"""
    name = StringField('Namn', 
                        validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', 
                        validators=[DataRequired(), Email()])
    password = PasswordField('Lösenord', 
                            validators=[DataRequired()])
    confirm_password = PasswordField('Lösenord konfirmation', 
                                    validators=[DataRequired(), 
                                    EqualTo('password')]
                                    )
    address = StringField('Adress', validators=[DataRequired()])
    postalCode = StringField('Postkod', validators=[DataRequired()])
    submit = SubmitField('Registrera dig')

    def validate_email(self, email):
        """ 
        ValidationError raised if email doesnt match any user in db
        """
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError('Den mail adressen är redan registrerad')


class QuestionForm(FlaskForm):
    """ Used for users to publish questions to us """
    name = StringField('Namn', validators=[Length(min=2, max=25)])
    email = StringField('Email', validators=[Email()])
    message = StringField('Meddelande', validators=[Length(min=2, max=100)])
    submit = SubmitField('Skicka')


class LoginForm(FlaskForm):
    """ Used for logging in users """
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Lösenord', validators=[DataRequired()])
    remember = BooleanField('Kom ihåg mig') 
    submit = SubmitField('Logga in')


class UpdateProfileForm(FlaskForm): 
    """
    You should be able to send in empty fields 
    for the information you dont want to change
    hence this route
    """
    name = StringField('Namn', 
                        validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Adress', validators=[DataRequired()])
    postalCode = StringField('Postkod', validators=[DataRequired()])
    submit = SubmitField('Uppdatera uppgifter')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()         
            if user is not None:
                raise ValidationError('Den mail adressen är redan registrerad')


class SellRequestForm(FlaskForm):
    """For users to send us sellrequests"""
    category = SelectField('Välj kategori', 
                            choices = [('Stol', 'Stol'), ('Bord', 'Bord'),
                            ('Säng', 'Säng'), ('Fåtölj', 'Fåtölj'), 
                            ('Soffa', 'Soffa'), ('Förvaring', 'Förvaring')])
    transportHelp = BooleanField('Jag vill att min möbel hämtas av LITHEmöbler')
    donation = BooleanField('Detta är en donation')
    skicka = SubmitField('Skicka säljförfrågning')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    submit = SubmitField('Skicka begäran om att återställa lösenord')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is None: 
            raise ValidationError('Det finns inget konto \
                                    kopplat till den email addressen')


class ChangePasswordForm(FlaskForm):
    """For a user to change their password"""                                     
    password = PasswordField('Lösenord', validators=[DataRequired()])
    confirm_password = PasswordField('Lösenord konfirmation',
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Återställ lösenord')


class FilterForm(FlaskForm):
    """For filtering the explore-page"""
    category1 = BooleanField('Stolar', description = "Stol") 
    category2 = BooleanField('Soffor', description = "Soffa") 
    category3 = BooleanField('Sängar', description = "Säng") 
    category4 = BooleanField('Bord', description = "Bord") 
    category5 = BooleanField('Fåtöljer', description = "Fåtölj") 
    category6 = BooleanField('Förvaring', description = "Förvaring") 
    color1 = BooleanField('Svart', description = 'Svart')    
    color2 = BooleanField('Vit', description = "Vit")    
    color3 = BooleanField('Brun', description = "Brun")    
    color4 = BooleanField('Grön', description = "Grön")
    color5 = BooleanField('Gul', description = "Gul")    
    color6 = BooleanField('Blå', description = "Blå")    
    color7 = BooleanField('Röd', description = "Röd")    
    color8 = BooleanField('Beige', description = "Beige")
    color9 = BooleanField('Grå', description = "Grå")
    condition1 = BooleanField('Nyskick', description = 1)
    condition2 = BooleanField('Bra skick', description = 2)
    condition3 = BooleanField('Helt ok', description = 3)
    condition4 = BooleanField('Lite sliten', description = 4)
    condition5 = BooleanField('Mycket sliten', description = 5)
    maxprice = IntegerField('Max pris')
    minprice = IntegerField('Min pris')
    filtrera = SubmitField('Filtrera')
    sortera_billigast = SubmitField('Billigast först')
    sortera_dyrast = SubmitField('Dyrast först')

