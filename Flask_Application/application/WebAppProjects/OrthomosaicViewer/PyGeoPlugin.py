from pygeoapi.provider.base import BaseProvider
from pygeoapi.provider.postgresql import PostgreSQLProvider
import application
from application.util import StravaAWSS3
import os
# https://stackoverflow.com/questions/805066/how-do-i-call-a-parent-classs-method-from-a-child-class-in-python
class orthoPoints(PostgreSQLProvider):
    def query(self, **kwargs):
        application.logger.debug("query request!")
        # queryRes= super().query(**kwargs)
        queryRes = PostgreSQLProvider.query(self, **kwargs)
        # application.logger.debug(queryRes)
        # media name: ['features'][5]['properties']['Media Name']
        for c,i in enumerate(queryRes['features']):
            preSignedURL = StravaAWSS3.get_presigned_url(i['properties']['Media Name'], os.getenv("orthobucket"),
                                                         expiration=600)
            queryRes['features'][c]['properties']["URL"] = preSignedURL
        # process queryRes
        application.logger.debug(queryRes)
        return queryRes
    def get(self, identifier, **kwargs):
        application.logger.debug("get request!")
        queryRes = PostgreSQLProvider.get(self, identifier, **kwargs)
        preSignedURL = StravaAWSS3.get_presigned_url(queryRes['properties']['Media Name'], os.getenv("orthobucket"),
                                                     expiration=600)
        queryRes['properties']["URL"] = preSignedURL
        return queryRes


# see https://docs.pygeoapi.io/en/latest/_modules/pygeoapi/provider/postgresql.html
# class orthoPoints(BaseProvider):
#     def __init__(self, PostgreSQLProvider):
#         """Inherit from parent class"""
#
#         super().__init__(PostgreSQLProvider)
#
#     def query(self, startindex=0, limit=10, resulttype='results',
#                             bbox=[], datetime_=None, properties=[], sortby=[],
#                             select_properties=[], skip_geometry=False, **kwargs):
#
#                       # optionally specify the output filename pygeoapi can use as part of the response (HTTP Content-Disposition header)
#                       self.filename = "my-cool-filename.dat"
#
#                       # open data file (self.data) and process, return


# class MyCoolVectorDataProvider(BaseProvider):
#     """My cool vector data provider"""
#
#     def __init__(self, provider_def):
#         """Inherit from parent class"""
#
#         super().__init__(provider_def)
#
#     def get_fields(self):
#
#         # open dat file and return fields and their datatypes
#         return {
#             'field1': 'string',
#             'field2': 'string'
#         }
#
#     def query(self,startindex=0, limit=10, resulttype='results',
#               bbox=[], datetime_=None, properties=[], sortby=[],
#               select_properties=[], skip_geometry=False, **kwargs):
#
#         # optionally specify the output filename pygeoapi can use as part
#         of the response (HTTP Content-Disposition header)
#         self.filename = "my-cool-filename.dat"
#
#         # open data file (self.data) and process, return
#         return {
#             'type': 'FeatureCollection',
#             'features': [{
#                 'type': 'Feature',
#                 'id': '371',
#                 'geometry': {
#                     'type': 'Point',
#                     'coordinates': [ -75, 45 ]
#                 },
#                 'properties': {
#                     'stn_id': '35',
#                     'datetime': '2001-10-30T14:24:55Z',
#                     'value': '89.9'
#                 }
#             }]
#         }