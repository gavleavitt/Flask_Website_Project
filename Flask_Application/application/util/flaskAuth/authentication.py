#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module handles authentication checks by calling on database query functions with the credentials provided by the user.

Created on Fri May 29 13:32:44 2020

@author: Gavin Leavitt
"""
from werkzeug.security import generate_password_hash, check_password_hash
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

import application
from application.util.flaskAuth.modelsAuth import Roles, User
from application import Session
# Sets up auth object, is modified by decorators further down the script and called when a
# user attempts to authenticate when visiting a route.
auth = HTTPBasicAuth()

# def createSession():
#     engine = create_engine(os.environ.get("DBCON"))
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     return session

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
    roles = getroles(username)
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
    hashPass = getHashPass(username)
    # The != None expression may not be needed, the second if statement will not be entered
    # unless the username and password combo are right, a user will not be given any info if just
    # the username is correct and password is incorrect
    if (hashPass != None):
        if username in hashPass.keys() and check_password_hash(
                hashPass[username], password):
            return username

def getroles(username):
    """
    Queries PostgreSQL database for user roles using username supplied by Flask HTTP Basic Auth.

    Parses roles into a list.

    Parameters
    ----------
    username : String
        Username as provided by user in the auth prompt.

    Returns
    -------
    res : List
        List of strings containing user roles.
        All roles need to be returned.
    None if empty results, user not in database.
    """
    session = Session()
    query = session.query(Roles.roles).filter(Roles.user == username).all()
    #     res += row
    res = query[0]
    if len(res) == 0:
        res = None
    # Roles are stored as comma seperated strings
    # Convert result tuple into a list of strings split by commas
    else:
        res = res[0].split(",")
    session.close()
    return res


def getHashPass(username):
    """
    Get the hashed password from PostgreSQL database using the username supplied by HTTP Basic Auth.

    Parameters
    ----------
    username : String
        Username as provided by user in the auth prompt.

    Returns
    -------
    res_dict : dictionary
        keys:
            username (string, parameter)
         value:
            hashed password (string)
            None (if no matching user in table)

    A dictionary is returned to maintain connection between username supplied and password.
    """
    session = Session()
    query = session.query(User.hashpass).filter(User.user == username).all()
    res_dict = {}
    for row in query:
        res_dict[username] = row.hashpass
    session.close()
    if len(res_dict) == 0:
        return None
    else:
        return res_dict
