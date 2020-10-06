#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module handles authentication checks by calling on database query functions with the credentials provided by the user.  

Created on Fri May 29 13:32:44 2020

@author: Gavin Leavitt
"""
from werkzeug.security import generate_password_hash, check_password_hash
from application import DB_Queries as DBQ
from flask_httpauth import HTTPBasicAuth

# Sets up auth object, is modified by decorators further down the script and called when a 
# user attempts to authenticate when visiting a route.
auth = HTTPBasicAuth()


@auth.get_user_roles
def get_user_roles(username):
    """
    Calls on the DB_Queries getroles function to get the roles of the provided username.
    This function is separated to keep all authentication and role checks separate from the queries. 

    Parameters
    ----------
    username : String
        Username provided by user.

    Returns
    -------
    roles : List
        List of strings containing the roles of the provided username, if any.

    """
    roles = DBQ.getroles(username)
    # If roles contains values return it, otherwise return nothing, which will cause the role check to fail,
    # blocking access to the resource
    if roles != None:
        return roles

@auth.verify_password
def verify_password(username, password):
    """
    Verifies if the provided username and password are valid.
    
    The provided username is used to query the DB, if the username is in the DB then the
    username and stored hashed password (hashed in pbkdf2:sha512) are returned to this function. 
  
    The user provided password is then hashed and checked against the stored hash, if they match then the
    username is returned from this function, allowing access to the resource. 

    Parameters
    ----------
    username : String
        Username provided by user.
    password : String
        Password provided by user.

    Returns
    -------
    username : String
        Provided username if the username and password combo are valid, allowing access to the resource.
    None
        If the username, or username and password combo, are invalid then nothing is returned and auth fails, 
        denying access to the resource. 

    """
    hashpass = DBQ.gethashpass(username)
    # The != None expression may not be needed, the second if statement will not be entered
    # unless the username and password combo are right, a user will not be given any info if just
    # the username is correct and password is incorrect
    if (hashpass != None):
        if username in hashpass.keys() and check_password_hash(
                hashpass[username], password):
            return username
