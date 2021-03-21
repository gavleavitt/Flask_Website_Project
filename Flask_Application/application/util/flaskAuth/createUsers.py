#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 16:26:42 2020

@author: user
"""
import sqlalchemy
# from sqlalchemy import create_engine
# import script_config as dbconfig
# #import models
#
# engine = create_engine((f"postgresql://{dbconfig.settings['user']}:{dbconfig.settings['password']}@{dbconfig.settings['host']}" +
#           f":{dbconfig.settings['port']}/{dbconfig.settings['dbname']}"))
#
# conn = engine.connect()
#
# def askdetails():
#     user = input("Enter username")
#     password = input("Enter password")
#     roles = input("Insert roles seperated by a comma")
#     results = {"user":user,"password":password,"roles":roles}
#     return results
#
# def insertuser(username,hashedpass):
#     ins = models.User.insert().values(user=username,hashpass=hashedpass)
#     conn.execute(ins)
#
# def insertroles(username,roles):
#     ins = models.User.insert().values(user=username,roles=roles)
#     conn.execute(ins)
#
# details = askdetails()