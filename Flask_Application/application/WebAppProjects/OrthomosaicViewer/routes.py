from flask import render_template, Blueprint

orthoviewer_BP = Blueprint('orthoviewer_BP', __name__,
                        template_folder='templates',
                        static_folder='static')


@orthoviewer_BP.route("/orthoviewermain")
def orthoviewermain():
    tilesJSON = ""
    return render_template("OrthomosaicViewer/OrthomosaicViewerMainMap.html", title="Orthomosaic Viewer", s3Tiles = tilesJSON)
