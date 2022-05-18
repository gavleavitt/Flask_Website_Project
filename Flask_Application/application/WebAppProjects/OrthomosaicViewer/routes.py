from flask import render_template, Blueprint

orthoviewer_BP = Blueprint('orthoviewer_BP', __name__,
                        template_folder='templates',
                        static_folder='static')


@orthoviewer_BP.route("/orthoviewermainopenlayers")
def orthoviewermainol():
    tilesJSON = ""
    return render_template("OrthomosaicViewer/OrthomosaicViewerMainMapOpenLayers.html", title="Orthomosaic Viewer", s3Tiles = tilesJSON)

@orthoviewer_BP.route("/orthoviewermainmapbox")
def orthoviewermainmb():
    tilesJSON = ""
    return render_template("OrthomosaicViewer/OrthomosaicViewerMainMapMapBox.html", title="Orthomosaic Viewer", s3Tiles = tilesJSON)

@orthoviewer_BP.route("/orthoviewer/<int:id>", methods=['GET'])
def orthoviewersingle():
    tilesJSON = ""
    return render_template("OrthomosaicViewer/OrthomosaicViewerMainMap.html", title="Orthomosaic Viewer", s3Tiles = tilesJSON)