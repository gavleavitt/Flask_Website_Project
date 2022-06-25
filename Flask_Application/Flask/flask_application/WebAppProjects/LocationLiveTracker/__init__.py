import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

gpsTrackEng = create_engine(os.environ.get("DBCON_GPSTRACKING"))
gpsTrackSes = sessionmaker(bind=gpsTrackEng)
