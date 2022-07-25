from flask import render_template, Blueprint, url_for
from flask_application import application
orthoviewer_BP = Blueprint('orthoviewer_BP', __name__,
                        template_folder='templates',
                        static_folder='static')
# see: https://docs.pygeoapi.io/en/latest/_modules/pygeoapi/flask_app.html
if application.config['ENV'] != "development":
    dataURLBase = "https://geo.leavittmapping.com/collections/ortho_mission_extents/items"
else:
    dataURLBase = "http://geo.leavitttesting.local:5000/collections/ortho_mission_extents/items"

@orthoviewer_BP.route("/orthoviewermainopenlayers")
def orthoviewermainol():
    mapTitle = "Orthomosaic Collection, Processing, and Web Viewer"
    tilesJSON = ""
    # TODO: Figure out how to make dynamic link, can I grab the subdomain and url from the pygeoapi blueprint?

    # f"http://{application.config['SERVER_NAME']}{url_for('pygeoapi_blueprint.handletracerequest')}"
    dataURL = dataURLBase + "?f=json"
    return render_template("OrthomosaicViewer/OrthomosaicViewerMainMapOpenLayers.html", title="Orthomosaic Viewer",
                           mapTitle=mapTitle, s3Tiles = tilesJSON, dataURL=dataURL)

@orthoviewer_BP.route("/orthoviewermainmapbox")
def orthoviewermainmb():
    tilesJSON = ""
    return render_template("OrthomosaicViewer/OrthomosaicViewerMainMapMapBox.html", title="Orthomosaic Viewer", s3Tiles = tilesJSON)

@orthoviewer_BP.route("/orthoviewermainopenlayers/<int:rid>", methods=['GET'])
def orthoviewersingle(rid):
    dataURL = dataURLBase + f"/{rid}?f=json"
    # Get ID from GET request and to pass into template
    return render_template("OrthomosaicViewer/OrthomosaicViewerMainMapSingle.html", title="Orthomosaic Viewer", dataURL=dataURL)

@orthoviewer_BP.route("/orthoviewermainopenlayers/mesh/<int:rid>", methods=['GET'])
def orthoviewermeshsingle(rid):
    # Get ID from GET request and to pass into template
    return render_template("OrthomosaicViewer/OrthomosaicViewerMainMapMesh.html", title="Orthomosaic Viewer", dataURL=rid)