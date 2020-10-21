from application import app, application, models, db, StravaWebHook, logger, DB_Queries_Strava, getStravaActivities
from application import functions as func
from application import DB_Queries as DBQ
from application.models_Strava import athletes, sub_update, strava_activities, strava_activities_masked
from application import DB_Queries_Strava as DQS
from application import objectgeneration as OBG
from application.authentication import auth
from flask import request, Response
from flask import jsonify
import sys
from application import script_config
from application import stravaAuth
from sqlalchemy.ext.declarative import declarative_base
import os
from sqlalchemy import create_engine, or_


# def createTable(tableModel):
#     engine = create_engine(os.environ.get("DBCON"))
#     Base = declarative_base()
#     tableObjects = [tableModel.__table__]
#     Base.metadata.create_all(engine, tables=tableObjects)
#
#
# @app.route("/admin/createtables")
# @auth.login_required(role='admin')
# def createtables():
#     session = DQS.createSession()
#     tablemodels = [strava_activities, strava_activities_masked]
#     for i in tablemodels:
#         createTable(i)
#     return "Success!"
#
# @app.route("/admin/populatestravatables")
# @auth.login_required(role='admin')
# def populatetables():
#     session = DQS.createSession()
#     days = 3650
#     message = getStravaActivities.processActs(days)
#     return message


# def createMaskedStravaTable():
#     engine = create_engine(os.environ.get("DBCON"))
#     Base = declarative_base()
#     tableModel = models_Strava.strava_activities_masked
#     tableObjects = [tableModel.__table__]
#     Base.metadata.create_all(engine, tables=tableObjects)


# @app.route("/admin/manuallydownact")
# @auth.login_required(role='admin')
# def manually_process_act():
#     """
#     Used to manually download and insert strava activities by inputted ID. Used during development and testing,
#     shouldn't be needed once app is fully functional.
#
#     Returns
#     -------
#
#     """
#     client = stravaAuth.gettoken()
#     # ID of activity to download and insert into Postgres tables
#     actid = 4217956841
#     activity = getStravaActivities.getFullDetails(client, actid)
#     # Insert activity details into Postgres/PostGIS
#     DQS.insertAct(activity)
#     # Calculate masked activities and insert into Postgres masked table
#     DQS.maskandInsertAct(activity["actId"])
#     # DQS.maskandInsertAct(actid)
#     return "Success!"

# @app.route(script_config.strava_create_sub_url, methods=['GET'])
# @auth.login_required(role='admin')
# def handle_Create_Strava_Sub():
#     """
#     URL to handle creation of new webhook subscription. Must visited by user who has already provided OAuth access.
#     Requires admin level access to visit.
#
#     Consider for future development:
#     Have page prompt user for OAuth access, process Oauth creds, then create new webhook subscription including new user
#     Maybe use Flask-Login to keep track of who is logged in and Oauth credentials.
#
#     Returns
#     -------
#     String. String containing new webhook subscription ID.
#     """
#     try:
#         # Get application access credentials
#         client = stravaAuth.gettoken()
#         application.logger.debug("Client loaded with tokens!")
#         # Handle webhook subscription and response
#         response = StravaWebHook.create_Strava_Webhook(client)
#         return f"Creation of new strava webhook subscription succeeded, new sub id is {response}!"
#     except Exception as e:
#         return f"Creation of new strava webhook subscription failed with the error {e}"
# @app.route(script_config.strava_list_subs_url, methods=['GET'])
# @auth.login_required(role='admin')
# def liststravasubs():
#     """
#     Lists application webhook subscriptions. Manually visited, requires admin level access.
#
#     Returns
#     -------
#     String. Message with webhook subscription IDs.
#     """
#     # Get application access credentials
#     client = stravaAuth.gettoken()
#     subIDs = StravaWebHook.listStravaSubIds(client)
#     return f"Webhook subscriptions IDs are {subIDs}"
#
# @app.route(script_config.strava_delete_subs_url, methods=['GET'])
# @auth.login_required(role='admin')
# def deletestravasubs():
#     """
#     Deletes application webhook subscriptions. Manually visited, requires admin level access.
#
#     Returns
#     -------
#     String. Message with deleted webhook subscription IDs.
#
#     """
#     # Get application access credentials
#     client = stravaAuth.gettoken()
#     subIDs = StravaWebHook.deleteStravaSubIds(client)
#     return f"Deleted webhook subscriptions with the IDs: {subIDs}"


# @app.route("/testmasking")
# @auth.login_required(role='admin')
# def testMaskandInsertActivity():
#     DB_Queries_Strava.maskandInsertAct(2872938014)
#     return "Success!"

# @app.route("/stravaprocessmasking")
# @auth.login_required(role='admin')
# def stravaProcessDat():
#     DB_Queries_Strava.simplifyandMaskAllActivities()
#     return "Success!"
#
#
# @app.route("/createmaskedtab")
# @auth.login_required(role='admin')
# def createStravaMaskedtable():
#     DB_Queries_Strava.createMaskedStravaTable()
#     return "Success!"

#
# @app.route("/downloadstravaact")
# @auth.login_required(role='admin')
# def downloadStravaAct():
#     return getStravaActivities.processActs(6)

# @app.route("/sendemail")
# @auth.login_required(role='admin')
# def email():
#     errorEmail.senderroremail()
#     return("Email sent!")
# @app.route("/uploadpdf")
# @auth.login_required(role='admin')
# def upload():
#     GoogleDrive. addtoGDrive(r"G:\My Drive\Projects\test_documents\Ocean_Water_Quality_Report_testing_20201002.pdf",
#                               "Ocean_Water_Quality_Report_testing_20201002.pdf")
#     return("uploaded!")
# @app.route("/testdownload")
# @auth.login_required(role='admin')
# def testdownload():
#     parsePDF.parsePDF()
#     return ("Ran test download!")
#
# @app.route("/auth/strava")
# @auth.login_required(role='admin')
# def authstrava():
#     client = Stravadownload.stravaAuth()
#     res = Stravadownload.getatth(client)
#     print("res")