from application import db
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from application.util.flaskLogin.models import User
from sqlalchemy.sql import expression

# flask-sqlalchemy server default: https://stackoverflow.com/a/44787117
#https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime

class Asset(db.Model):
    __tablename__ = 'assets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default="")
    modelyear = db.Column(db.String(100), default="")
    make = db.Column(db.String(100), default="")
    model = db.Column(db.String(100), default="")
    notes = db.Column(db.String(500), default="")
    suspension = db.Column(db.String(50), default="")
    framesize = db.Column(db.String(50), default="")
    wheelsize = db.Column(db.String(50), default="")
    type = db.Column(db.String(50), default="")
    retailprice = db.Column(db.Integer(), default=0)
    purchasetype = db.Column(db.String(20), default="")
    purchasesource = db.Column(db.String(100), default="")
    serial = db.Column(db.String(100), default="")
    ownerfk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_on = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_on = db.Column(DateTime(timezone=True), onupdate=func.now())

class maintRecord(db.Model):
    __tablename__= "maintenance_records"

    id = db.Column(db.Integer, primary_key=True)
    worktype = db.Column(db.String(100), default="")
    mainttime = db.Column(db.DateTime(timezone=True))
    worknotes = db.Column(db.String(100), default="")
    workcost = db.Column(db.Integer(), default=0)
    shop = db.Column(db.String(100), default="")
    workduration = db.Column(db.Float(), default=0.0)
    assetfk = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    partfk = db.Column(db.Integer, db.ForeignKey('partinstalls.id'), nullable=False)
    created_on = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_on = db.Column(DateTime(timezone=True), onupdate=func.now())

class installs(db.Model):
    __tablename__= 'partinstalls'

    id = db.Column(db.Integer, primary_key=True)
    partnum = db.Column(db.String(100), default="")
    partserial = db.Column(db.String(100), default="")
    partcost = db.Column(db.Integer(), default=0)
    currentlyinstalled = db.Column(db.Boolean(), default=True)
    partnotes = db.Column(db.String(100), default="")
    assetfk = db.Column(db.Integer, db.ForeignKey('assets.id'), nullable=False)
    vendor = db.Column(db.String(100), default="")
    postinglink = db.Column(db.String(100), default="")
    s3objid = db.Column(db.String(100), default="")
    manuallink = db.Column(db.String(100), default="")
    parttype = db.Column(db.String(100), default="")
    partname = db.Column(db.String(100), default="")
    created_on = db.Column(DateTime(timezone=True), server_default=func.now())
    updated_on = db.Column(DateTime(timezone=True), onupdate=func.now())