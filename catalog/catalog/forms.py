# --------- forms.py: define WTF form classes -------------
from wtforms import Form, StringField, TextField, SelectField, IntegerField, RadioField, TextAreaField, FileField, validators
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired
from flask.ext.wtf.html5 import URLField

class NewBook(Form):
    """ Class to create a new book """
    title = StringField('Title', validators = [DataRequired()])
    isbn = StringField('ISBN')
    datepub = StringField('Year Published')
    language = SelectField('Language',
                           choices = ['Arabic', 'English', 'French', 'German', 'Spanish'])
    edition = SelectField('Edition', choices = ['1st', '2nd', '3rd', '4th', '5th'])
    condition = SelectField('Condition', choices = ['Acceptable', 'Excellent', 'Good', 'Poor'])
    binding = SelectField('Binding', choices = ['Hardback', 'Paperback', 'Video'])
    available = RadioField('Available', choices = ['Yes', 'No'])
    category = StringField('Category', validators = [DataRequired()])
    author = StringField('Author', validators = [DataRequired()])
    publisher = StringField('Publisher', validators = [DataRequired()])
    coverURL = FileField('Cover Image')
    summary = TextAreaField('Summary')

class NewCategory(Form):
    """ Class to create a new category """
    name = StringField('Name', validators = [DataRequired])

class EditCategory(Form):
    """ Class to edit a category """
    name = StringField('Name', validators = [DataRequired])

class NewAuthor(Form):
    """ Class to create a new author """
    name = StringField('Name', validators = [DataRequired])
    active = RadioField('Active', choices = [(1, "Yes"), (0, "No")], default = 1 )
    imageURL = StringField('Image URL')

class EditAuthor(Form):
    """ Class to edit an author """
    name = StringField('Name', validators = [DataRequired])
    active = RadioField('Active', choices = [(1, "Yes"), (0, "No")])
    imageURL = StringField('Image URL')
#
class NewPublisher(Form):
    """ Clas to create a new publisher """
    name = StringField('Name', validators = [DataRequired()])
    address = StringField('Address')

class EditPublisher(Form):
    """ Clas to edit a publisher """
    name = StringField('Name', validators = [DataRequired()])
    address = StringField('Address')

class NewReview(Form):
    """ Class to create a review """
    review = TextAreaField('Your Review', validators = [DataRequired])

class BookByIsbn(Form):
    """ Class to isbn submit form """
    isbn_google_api = StringField('Book ISBN',validators = [DataRequired])

#print 'all good'
