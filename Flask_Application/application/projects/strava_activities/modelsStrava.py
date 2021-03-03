from sqlalchemy import Column, String, Integer, ForeignKey, Float, Interval, BigInteger, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()

class strava_gear(Base):
    __tablename__ = "strava_gear"
    id = Column(Integer, primary_key=True)
    gear_name = Column(String(50))
    gearid = Column(String(50), unique=True)
    gear_desc = Column(String(100))

class athletes(Base):
    __tablename__ = 'strava_athletes'

    id = Column(Integer, primary_key=True)
    athlete_id = Column(Integer)
    scopes = Column(String)
    sub_id = Column(Integer)
    refresh_token = Column(String)
    athlete_name = Column(String)

class sub_update(Base):
    __tablename__ = 'strava_webhook_updates'

    id = Column(Integer, primary_key=True)
    aspect = Column(String)
    event_time = Column(DateTime)
    object_id = Column(BigInteger)
    object_type = Column(String)
    owner_id = Column(Integer)
    subscription_id = Column(Integer)
    update_title = Column(String)

class strava_activities(Base):
    __tablename__ = "strava_activities"

    id = Column(Integer, primary_key=True)
    actID = Column(BigInteger, unique=True)
    athlete_id = Column(Integer, ForeignKey("strava_athletes.athlete_id"))
    upload_id = Column(String(50))
    name = Column(String(255))
    distance = Column(Float)
    type_extended = Column(String(50))
    moving_time = Column(Interval)
    elapsed_time = Column(Interval)
    manual = Column(String(50))
    total_elevation_gain = Column(Float)
    elev_high = Column(Float)
    elev_low = Column(Float)
    type = Column(String(50))
    start_date = Column(DateTime)
    start_date_local = Column(DateTime)
    timezone = Column(String(50))
    utc_offset = Column(Float)
    start_latlng = Column(String(100))
    end_latlng = Column(String(100))
    start_latitude = Column(Float)
    start_longitude = Column(Float)
    device_name = Column(String(100))
    achievement_count = Column(Integer)
    pr_count = Column(Integer)
    private = Column(String(50))
    gear_id = Column(String(50), ForeignKey("strava_gear.gearid"))
    average_speed = Column(Float)
    max_speed = Column(Float)
    average_watts = Column(Float)
    kilojoules = Column(Float)
    description = Column(String(255))
    workout_type = Column(String(100))
    calories = Column(Float)
    ## Wahoo data and sensor data
    avgtemp = Column(Integer)
    has_heartrate = Column(String(100))
    max_heartrate = Column(Float)
    average_heartrate = Column(Float)
    average_cadence = Column(Float)

    ##
    geom = Column(Geometry(geometry_type='LINESTRINGM', srid=4326, from_text = 'ST_GeomFromEWKT',  name='geometry',
                           dimension=3))
    gear_rel = relationship(strava_gear, backref="strava_gear")
    ath_rel = relationship(athletes, backref="strava_athletes")

    def builddict(self):
        """
        Formats data in a GeoJSON friendly format, removes troublesome columns and formats datetime fields using
        .isoformat(). Interval, timedelta, values are converted to Int (seconds).

        :return: Dictionary with attribute data
        """
        removedictlist = ['_sa_instance_state', 'geom']
        dateCol = ["start_date", "start_date_local"]
        durCol = ["moving_time", "elapsed_time"]
        res_dict = self.__dict__
        for i in removedictlist:
            res_dict.pop(i, None)
        for v in dateCol:
            if not isinstance(res_dict[v], str):
                res_dict[v] = res_dict[v].isoformat()
        for h in durCol:
            if not isinstance(res_dict[h], int):
                res_dict[h] = res_dict[h].seconds
        return res_dict


class strava_activities_masked(Base):
    __tablename__ = "strava_activities_masked"

    id = Column(Integer, primary_key=True)
    actID = Column(BigInteger, ForeignKey("strava_activities.actID"))
    # geom = Column(Geometry(geometry_type='MULTILINESTRING', srid=4326,  from_text = 'ST_GeomFromEWKT', name='geometry'))
    geom = Column(Geometry(geometry_type='MULTILINESTRING', srid=4326,  from_text='ST_GeomFromEWKB', name='geometry'))
    # geom = Column(Geometry(geometry_type='MULTILINESTRING', srid=4326, from_text='ST_GeomFromWKB', name='geometry'))
    act_rel = relationship(strava_activities, backref="strava_activities_masked")


class privacy_clip_poly(Base):
    __tablename__ = "privacy_clip"

    id = Column(Integer, primary_key=True)
    geom = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326, from_text='ST_GeomFromEWKB', name='geometry'))

class AOI(Base):
    __tablename__ = 'AOI'

    id = Column(Integer, primary_key=True)
    geom = Column(Geometry('MULTIPOLYGON', 4326), index=True)
    location = Column(String(80))
    desc = Column(String(80))
    privacy = Column(String(50))

