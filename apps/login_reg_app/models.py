from __future__ import unicode_literals

from django.db import models
import bcrypt
import re
from datetime import date
PASSWORD_REGEX = re.compile(r'\d.*[A-Z]|[A-Z].*\d')
# Create your models here.
class UserManage(models.Manager):
    def user_register(self, postData):
        isvalid = True
        error_messages = []
        if len(postData['first_name']) < 3 or len(postData['last_name']) < 3 or len(postData['username']) < 3:
            isvalid = False
            error_messages.append('Names and username must be at least 3 characters')
        if User.objects.filter(username=postData['username']).first():
            isvalid = False
            error_messages.append('This username already exists. Please login with your account.')
        if len(postData['password']) < 8 or not PASSWORD_REGEX.match(postData['password']):
            isvalid = False
            error_messages.append('Password must be at least 8 characters and must contain at least 1 capital letter and 1 number')
        if postData['password'] != postData['confirm_password']:
            isvalid = False
            error_messages.append('Password and Confirm Password must match!')
        if isvalid == True:
            password = postData['password'].encode()
            pw_hash = bcrypt.hashpw(password, bcrypt.gensalt())
            user = self.create(first_name=postData['first_name'], last_name=postData['last_name'], username=postData['username'], pw_hash=pw_hash)
            return user, True
        else:
            return error_messages, False

    def user_login(self, postData):
        error_messages = ['You must enter a valid username and password to login']
        if postData['username'] > 1 and postData['password'] > 7 and self.filter(username = postData['username']).first():
            user = self.get(username=postData['username'])
            password = postData['password'].encode()
            if bcrypt.hashpw(password, user.pw_hash.encode()) == user.pw_hash:
                return user, True
        return error_messages, False

    def password_update(self, postData):
        isvalid = True
        error_messages = []
        if len(postData['password']) < 8 or not PASSWORD_REGEX.match(postData['password']):
            isvalid = False
            error_messages.append('Password must be at least 8 characters and must contain at least 1 capital letter and 1 number')
        if postData['password'] != postData['confirm']:
            isvalid = False
            error_messages.append('Password and Confirm Password must match!')
        if isvalid == True:
            password = postData['password'].encode()
            pw_hash = bcrypt.hashpw(password, bcrypt.gensalt())
            print pw_hash
            return pw_hash, True
        else:
            return error_messages, False

    def update_user(self, postData, user):
        isvalid = True
        error_messages = []
        if len(postData['first_name']) < 3 or len(postData['last_name']) < 3 or len(postData['username']) < 3:
            isvalid = False
            error_messages.append('Names and username must be at least 3 characters')
        if user.username != postData['username'] and User.objects.filter(username=postData['username']).first():
            isvalid = False
            error_messages.append('This username already exists. Please login with your account.')
        if isvalid == True:
            user.first_name = postData['first_name']
            user.last_name = postData['last_name']
            user.username = postData['username']
            user.save()
            print user.username
            return user, True
        else: return error_messages, False

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    username = models.CharField(max_length=45)
    pw_hash = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManage()
