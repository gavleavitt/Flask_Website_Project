from sqlalchemy import Column, String, Integer, Date, Boolean, ForeignKey, Float, Interval, BigInteger
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from geoalchemy2 import Geometry

Base = declarative_base()

class athletes(Base):
    __tablename__ = 'strava_athletes'

    id = Column(Integer, primary_key=True)
    athlete_id = Column(Integer)
    scopes = Column(String)
    sub_id = Column(Integer)
    refresh_token = Column(String)
    athlete_name = Column(String)

class sub_update(Base):
    __tablename__ = 'webhook_updates'

    id = Column(Integer, primary_key=True)
    aspect = Column(String)
    event_time = Column(Date)
    object_id = Column(Integer)
    object_type = Column(String)
    owner_id = Column(Integer)
    subscription_id = Column(Integer)
    update_title = Column(String)

class strava_activities(Base):
    __tablename__ = "strava_activities"

    id = Column(Integer, primary_key=True)
    actID = Column(BigInteger)
    upload_id = Column(String(50))
    name = Column(String(255))
    distance = Column(Float)
    moving_time = Column(Interval)
    elapsed_time = Column(Interval)
    total_elevation_gain = Column(Float)
    elev_high = Column(Float)
    elev_low = Column(Float)
    type = Column(String(50))
    start_date = Column(Date)
    start_date_local = Column(Date)
    timezone = Column(String(50))
    utc_offset = Column(Float)
    start_latlng = Column(String(100))
    end_latlng = Column(String(100))
    start_latitude = Column(Float)
    start_longitude = Column(Float)
    achievement_count = Column(Integer)
    pr_count = Column(Integer)
    private = Column(String(50))
    gear_id = Column(String(50))
    average_speed = Column(Float)
    max_speed = Column(Float)
    average_watts = Column(Float)
    kilojoules = Column(Float)
    description = Column(String(255))
    workout_type = Column(String(100))
    calories = Column(Float)
    geom = Column(Geometry(geometry_type='LINESTRINGM', srid=4326, from_text = 'ST_GeomFromEWKT',  name='geometry',
                           dimension=3))
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
    # geom = Column(Geometry(geometry_type='MULTILINESTRING', srid=4326, from_text = 'ST_GeomFromWKB', name='geometry'))
    geom = Column(Geometry(geometry_type='MULTILINESTRING', srid=4326,  from_text = 'ST_GeomFromEWKT', name='geometry'), index=True)
    beach_rel = relationship(strava_activities, backref="strava_activities_masked")