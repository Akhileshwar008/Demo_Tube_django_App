from django.db import models
from pymodm import EmbeddedMongoModel, MongoModel, fields,connect
from pymongo.read_preferences import ReadPreference
from django.forms import ModelForm
from django import forms


# pymodm.connection.connect('mongodb+srv://Akhilesh:Akhil123@cluster0.sp5fc.mongodb.net/mydata?retryWrites=true&w=majority', 
#                           alias='default', **kwargs)

# # Create your models here.






# class User(MongoModel):
#     email = fields.EmailField(primary_key=True)
#     name = fields.CharField()

#     class Meta:
#         # Read from secondaries.
#         read_preference = ReadPreference.SECONDARY

# # Instantiate User using positional arguments:
# jane = User('jane@janesemailaddress.net', 'Jane')
# # Keyword arguments:
# roy = User(name='Roy', email='roy@roysemailaddress.net')


from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import connect, fields, MongoModel, EmbeddedMongoModel


# # Connect to MongoDB first. PyMODM supports all URI options supported by
# # PyMongo. Make sure also to specify a database in the connection string:
connect('mongodb://localhost:27017/newdata')


# Now let's define some Models.
class Users(MongoModel):
    # Use 'email' as the '_id' field in MongoDB.
    email = fields.CharField(primary_key=True)
    name = fields.CharField()
    password = fields.CharField()
    sex = fields.CharField()
    
    class Meta:
        final = True






