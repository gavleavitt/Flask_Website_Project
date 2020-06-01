#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 29 13:32:44 2020

@author: user
"""
from application import app, db, models
from application import script_config as dbconfig
from werkzeug.security import generate_password_hash, check_password_hash
from application import DB_Queries as DBQ
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()


@auth.get_user_roles
def get_user_roles(username):
    """
    

    Parameters
    ----------
    username : TYPE
        DESCRIPTION.

    Returns
    -------
    roles : TYPE
        DESCRIPTION.

    """
    roles = DBQ.getroles(username)
    if roles != None:
        return roles

@auth.verify_password
def verify_password(username, password):
    """
    

    Parameters
    ----------
    username : TYPE
        DESCRIPTION.
    password : TYPE
        DESCRIPTION.

    Returns
    -------
    username : TYPE
        DESCRIPTION.

    """
    hashpass = DBQ.gethashpass(username)
    if (hashpass != None):
        if username in hashpass.keys() and check_password_hash(
                hashpass[username], password):
            return username
