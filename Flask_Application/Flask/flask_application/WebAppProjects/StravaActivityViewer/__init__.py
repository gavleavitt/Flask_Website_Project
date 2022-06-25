import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

stravaViewerEng = create_engine(os.environ.get("DBCON_STRAVAVIEWER"))
stravaViewerSes = sessionmaker(bind=stravaViewerEng)
