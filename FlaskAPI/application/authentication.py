#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 13:32:44 2020

@author: user
"""
from application import script_config as dbconfig
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()
@auth.get_user_roles
def get_user_roles(username):
    return dbconfig.roles.get(username)

@auth.verify_password
def verify_password(username, password):
    if username in dbconfig.users and check_password_hash(
            dbconfig.users.get(username), password):
        return username