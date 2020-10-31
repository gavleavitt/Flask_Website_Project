from sqlalchemy import create_engine, or_
from sqlalchemy.orm import sessionmaker
# from settings import dbcon
from application.models_WaterQual import beaches, waterQualityMD5, stateStandards, waterQuality
import os
from datetime import datetime
from application import application
from sqlalchemy import func as sqlfunc

def createSession():
    engine = create_engine(os.environ.get("DBCON"))
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def checkmd5(hash, pdfDate):
    """
    Checks if the downloaded PDF's MD5 hash is already in Postgres and returns result.

    :param hash: String
        New MD5 hash
    :param pdfDate: String
        New PDF Date
    :return: String
        "Exists" - Hash is already in Postgres
        "New" - Hash is not in Postgres and no other hashes exist for the PDF result week
        "Update" - Hash is not in Postgres but other hashes exist for th PDF result week
    """
    # Query Postgres with pdfDate of newly downloaded PDF
    session = createSession()
    application.logger.debug(f"Querying water quality MD5 hashes with the date {pdfDate}")
    query = session.query(waterQualityMD5).filter(waterQualityMD5.pdfdate == pdfDate).all()
    hashList = []
    application.logger.debug(f"Iterating ")
    for i in query:
        hashList.append(i.md5)
    session.close()
    if hash in hashList:
        return "Exists"
    elif len(hashList) == 0:
        return "New"
    else:
        return "Update"

# See: https://stackoverflow.com/questions/16589208/attributeerror-while-querying-neither-instrumentedattribute-object-nor-compa
def getNullBeaches(pdfDate):
    """
    Returns list of beaches with null values for the given PDF test week. Only called when a update/re-sample PDF is
    downloaded.

    :param pdfDate: String
        Date of new weekly PDF results
    :return: List[Strings,]
        Names of beaches with null test results
    """
    session = createSession()
    query = session.query(waterQuality) \
        .join(waterQualityMD5) \
        .join(beaches) \
        .filter(waterQualityMD5.pdfdate == pdfDate) \
        .filter(or_(waterQuality.FecColi == None, waterQuality.Entero == None, waterQuality.TotColi == None)) \
        .all()
    nullbeaches = []
    for i in query:
        nullbeaches.append(i.beach_rel.BeachName)
    return nullbeaches
    session.close()

def insmd5(MD5, pdfDate, pdfName):
    """
    Add water quality md5 and other information to postgres database. After committing, call on the primary key, id,
    to get the persisted, auto-incremented, id. The record must be committed before this value is assigned.
    :param MD5:
    :param pdfDate:
    :param pdfName:
    :param insDate:
    :return:
    """
    session = createSession()
    application.logger.debug(f"Inserting new md5 hash using the following details: md5:{MD5}, pdfdate:{pdfDate}",
                             f" pdfname:{pdfName}, insdate:{datetime.now()}")
    newrec = waterQualityMD5(md5=MD5, pdfdate=pdfDate, pdfName=pdfName, insdate=datetime.now())
    session.add(newrec)
    session.commit()
    newId = newrec.id
    session.close()
    print("Data added to MD5 table!")
    print(f"New water quality md5 hash id is {newrec.id}")
    return newId


def insertWaterQual(beachDict, md5_fk):
    """
    Inserts water quality results into water quality database table with md5 foreign key relationship.

    Parameters
    ----------
    beachDict: Dictionary. Dictionary containing values to be inserted into database.
    md5_fk: String. Foreign key from md5 table.

    Returns
    -------
    Print statement.
    """
    session = createSession()
    inslist = []
    for key in beachDict.keys():
        inslist.append(
            waterQuality(beach_id=beachDict[key]['fk'], TotColi=beachDict[key]['Total Coliform Results (MPN*)'],
                         FecColi=beachDict[key]["Fecal Coliform Results (MPN*)"],
                         Entero=beachDict[key]['Enterococcus Results (MPN*)'],
                         ExceedsRatio=beachDict[key]['Exceeds FC:TC ratio standard **'],
                         BeachStatus=beachDict[key]['Beach Status'], resample=beachDict[key]['resample'],
                         md5_id=int(md5_fk)))
    session.add_all(inslist)
    session.commit()
    session.close()
    print("Data added to water quality table!")


def getBeachWaterQual():
    """
    Queries Postgres AWS RDS to return the most recent water quality report data for each beach that is tested in SB
    County.

    Data are spread across tables with mapped relationships.

    This query joins the relevant tables and uses "distinct" on the waterQuality beach ID field, selecting only one
    record per beach, then "order_by" is used on the joined MD5 table to grab only the most recent record per beach.

    :return: List:
        Nested lists containing SQL Alchemy query results:
            3 query result objects:
                waterQuality, waterqualityMD5 beaches
            1 string:
                geometry type of associated beach
            2 floats:
                x and y coordinates of the associated beach
    """
    session = createSession()
    records = session.query(waterQuality, waterQualityMD5, beaches, sqlfunc.ST_GeometryType(beaches.geom),
                               sqlfunc.st_x(beaches.geom), sqlfunc.st_y(beaches.geom)) \
        .join(waterQualityMD5) \
        .join(beaches) \
        .distinct(waterQuality.beach_id) \
        .order_by(waterQuality.beach_id, waterQualityMD5.insdate.desc()).all()
    return records


def getStandards():
    """
    Get the state health standards for ocean water quality tests.

    Returns
    -------
    recDict : Dictionary
        Dict of State health standards, with the standard name as the keys and values as values.

    """
    session = createSession()
    records = session.query(stateStandards).all()
    recDict = {}
    for i in records:
        recDict[i.Name] = i.StandardMPN
    return recDict
