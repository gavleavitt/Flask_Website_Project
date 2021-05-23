from application import db
from sqlalchemy import Column, String, Integer, DateTime, TIMESTAMP, text
from sqlalchemy.sql import func
# from application.util.flaskLogin.models import User
from datetime import datetime
from sqlalchemy.sql import expression

# flask-sqlalchemy server default: https://stackoverflow.com/a/44787117
#https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime

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
    assets_rel = db.relationship("Asset", backref="Owner")

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
    # create relationship
    ownerfk = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner_rel = db.relationship(Owner,
        backref=db.backref('assets', lazy=True),supports_json = True)

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
    created_on = db.Column(db.DateTime(timezone=True), default=datetime.utcnow())
    updated_on = db.Column(db.DateTime(timezone=True),  default=datetime.utcnow(), onupdate=datetime.utcnow())

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
    created_on = db.Column(db.DateTime(timezone=True), default=datetime.utcnow())
    updated_on = db.Column(db.DateTime(timezone=True),  default=datetime.utcnow(), onupdate=datetime.utcnow())

