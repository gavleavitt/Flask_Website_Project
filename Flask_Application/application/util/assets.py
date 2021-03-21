from flask_assets import Bundle, Environment
from .. import app

bundles = {

    'home_js': Bundle(
        'js/mainFunctions.js',
        output='gen/home.js'),

    'home_css': Bundle(
        'css/mainStyle.css',
        output='gen/home.css'),

    'leaflet_ajax': Bundle(
        'js/lib/leaflet.ajax.min.js',
        output='gen/leaflet_ajax.js'
    ),

    'mouse_position_css': Bundle(
        'css/lib/L.Control.MousePosition.css',
        output='gen/mouse_position_css.css'
    ),

    'mouse_position_js': Bundle(
        'js/lib/L.Control.MousePosition.js',
        output='gen/mouse_position_js.js'
    ),
    #  'leafet_search_css': Bundle(
    #
    #  ),
    #   'leafet_search_js': Bundle(
    #
    # ),
    # 'admin_js': Bundle(
    #     'js/lib/jquery-1.10.2.js',
    #     'js/lib/Chart.js',
    #     'js/admin.js',
    #     output='gen/admin.js'),
    #
    # 'admin_css': Bundle(
    #     'css/lib/reset.css',
    #     'css/common.css',
    #     'css/admin.css',
    #     output='gen/admin.css')
}

assets = Environment(app)

assets.register(bundles)