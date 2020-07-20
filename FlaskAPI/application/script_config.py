#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from werkzeug.security import generate_password_hash, check_password_hash


settings = {
    "dbname":"",
    "port":"",
    "user":"",
    "password":"",
    "host":"",
    "store":"/media/sf_OSGeoLive_Shared/MTB_Tracking/GoogleDriveAPI/storage.json",
    "scope":"https://www.googleapis.com/auth/drive.readonly",
    "flow":"/media/sf_OSGeoLive_Shared/MTB_Tracking/GoogleDriveAPI/credentials.json",
    "fileid":"1E2vteA_Kh43hGWknAm5e1OE1uM0OWBzM",
    "phone":"Moto X4",
    "POI_Outdoors":['Toro Park','Fort Ord', 'UCSC Trails', 'Soquel Demo','Kern Canyon'],
    "srid":"4326",
    "timezone":"US/Pacific",
    "fileSavePathway":"/media/sf_OSGeoLive_Shared/GPSSaveLocation"}
