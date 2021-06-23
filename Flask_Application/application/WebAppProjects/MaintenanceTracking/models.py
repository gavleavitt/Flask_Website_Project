from application import db
from sqlalchemy import Column, String, Integer, DateTime, TIMESTAMP, text
from sqlalchemy.sql import func
# from application.util.flaskLogin.models import User
from datetime import datetime
from sqlalchemy.sql import expression
from flask_login import current_user
from application import logger
# flask-sqlalchemy server default: https://stackoverflow.com/a/44787117
#https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime

# def setUserID():
#     # logger.debug(current_user.id)
#     logger.debug("inside deserial!")
#     # return int(current_user.id)
#     pass
class Owner(db.Model):

    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    username = db.Column(String(100), unique=True)
    hashpass = db.Column(String(255))
    fullname = db.Column(String(100))
    role = db.Column(String(255))
    created_on = db.Column(db.DateTime(timezone=True), default=datetime.utcnow())
    updated_on = db.Column(db.DateTime(timezone=True),  default=datetime.utcnow(), onupdate=datetime.utcnow())
    assets_rel = db.relationship("Asset", backref="users")
    athlete_rel = db.relationship("athletes", backref="users")

class Asset(db.Model):
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key=True, supports_json = True, supports_dict= True)
    name = db.Column(db.String(100), default="", supports_json = True,supports_dict= True)
    modelyear = db.Column(db.String(100), default="", supports_json = True, supports_dict= True)
    make = db.Column(db.String(100), default="", supports_json = True, supports_dict= True)
    model = db.Column(db.String(100), default="", supports_json = True, supports_dict= True)
    notes = db.Column(db.String(500), default="", supports_json = True, supports_dict= True)
    suspension = db.Column(db.String(50), default="", supports_json = True, supports_dict= True)
    framesize = db.Column(db.String(50), default="", supports_json = True, supports_dict= True)
    wheelsize = db.Column(db.String(50), default="", supports_json = True, supports_dict= True)
    type = db.Column(db.String(50), default="", supports_json = True, supports_dict= True)
    retailprice = db.Column(db.Integer(), default=0, supports_json = True, supports_dict= True)
    purchaseprice = db.Column(db.Integer(), default=0, supports_json = True, supports_dict= True)
    purchasetype = db.Column(db.String(20), default="", supports_json = True, supports_dict= True)
    purchasesource = db.Column(db.String(100), default="", supports_json = True, supports_dict= True)
    serial = db.Column(db.String(100), default="", supports_json = True, supports_dict= True)
    created_on = db.Column(db.DateTime(timezone=True), default=datetime.utcnow(),
                           supports_json = True, supports_dict= True)
    updated_on = db.Column(db.DateTime(timezone=True),  default=datetime.utcnow(), onupdate=datetime.utcnow(),
                           supports_json = True, supports_dict= True)
    stravaid = db.Column(db.Integer())
    # create relationship
    ownerfk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # owner_rel = db.relationship(Owner,
    #     backref=db.backref('assets', lazy=True),supports_json = False)

class maintRecord(db.Model):
    __tablename__= "maintenance_records"

    id = db.Column(db.Integer, primary_key=True, supports_json = True, supports_dict= True)
    worktype = db.Column(db.String(100), default="", supports_json = True, supports_dict= True)
    mainttime = db.Column(db.DateTime(timezone=True), supports_json = True, supports_dict= True)
    worknotes = db.Column(db.String(100), default="", supports_json = True, supports_dict= True)
    workcost = db.Column(db.Integer(), default=0, supports_json = True, supports_dict= True)
    shop = db.Column(db.String(100), default="", supports_json = True, supports_dict= True)
    workduration = db.Column(db.Float(), default=0.0, supports_json = True, supports_dict= True)
    assetfk = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False,
                        supports_json = True, supports_dict= True)
    partfk = db.Column(db.Integer, db.ForeignKey('partinstalls.id'), nullable=False,
                       supports_json = True, supports_dict= True)
    created_on = db.Column(db.DateTime(timezone=True), default=datetime.utcnow(),
                           supports_json = True, supports_dict= True)
    updated_on = db.Column(db.DateTime(timezone=True),  default=datetime.utcnow(), onupdate=datetime.utcnow(),
                           supports_json = True, supports_dict= True)
    ownerfk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # create relationships
    asset_rel = db.relationship(Asset,
        backref=db.backref('maintenance_records', lazy=True),supports_json = True)

    # owner_rel = db.relationship(Owner,
    #     backref=db.backref('assets', lazy=True),supports_json = False)


class installs(db.Model):
    __tablename__= 'partinstalls'

    id = db.Column(db.Integer, primary_key=True)
    partnum = db.Column(db.String(100), default="")
    partserial = db.Column(db.String(100), default="")
    partcost = db.Column(db.Integer(), default=0)
    currentlyinstalled = db.Column(db.Boolean(), default=True)
    partnotes = db.Column(db.String(100), default="")
    assetfk = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    maintfk = db.Column(db.Integer, db.ForeignKey('maintenance_records.id'), nullable=False)
    vendor = db.Column(db.String(100), default="")
    postinglink = db.Column(db.String(100), default="")
    s3objid = db.Column(db.String(100), default="")
    manuallink = db.Column(db.String(100), default="")
    parttype = db.Column(db.String(100), default="")
    partname = db.Column(db.String(100), default="")
    created_on = db.Column(db.DateTime(timezone=True), default=datetime.utcnow())
    updated_on = db.Column(db.DateTime(timezone=True),  default=datetime.utcnow(), onupdate=datetime.utcnow())
    ownerfk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # create relationship
    # owner_rel = db.relationship(Owner,
    #     backref=db.backref('assets', lazy=True),supports_json = False)
    # maintRec_rel = db.relationship(maintRecord,
    #     backref=db.backref('partinstalls', lazy=True), supports_json = True)

class webhook_subs(db.Model):
    __tablename__ = 'strava_webhook_subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    sub_id = db.Column(db.BigInteger)
    activesub = db.Column(db.String(10))
    verify_token = db.Column(db.String(15))

class athletes(db.Model):
    __tablename__ = 'strava_athletes'

    id = db.Column(db.Integer, primary_key=True)
    athlete_id = db.Column(db.Integer)
    scopes = db.Column(db.String)
    sub_id = db.Column(Integer, db.ForeignKey("strava_webhook_subscriptions.id"))
    refresh_token = db.Column(db.String)
    access_token_exp = db.Column(db.DateTime)
    athlete_name = db.Column(db.String)
    access_token = db.Column(db.BigInteger)
    userfk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # Relationship with webhook subscriptions table
    sub_rel = db.relationship(webhook_subs, backref="strava_athletes")
    # Relationship with owner/users
    user_rel = db.relationship('Owner', backref=db.backref('strava_athletes', lazy=True))


