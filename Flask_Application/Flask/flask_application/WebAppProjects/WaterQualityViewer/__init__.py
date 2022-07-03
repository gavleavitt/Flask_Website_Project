import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

waterQualityEng = create_engine(os.environ.get("DBCON_WATERQUALITY"))
waterQualitySes = sessionmaker(bind=waterQualityEng)
