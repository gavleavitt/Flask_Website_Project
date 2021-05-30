from application import app
# from application.util.ErrorHandling import exception_handler

def register_api(view, endpoint, url, pk='id', pk_type='int', dateRange=None):
    """
    Taken from https://flask.palletsprojects.com/en/2.0.x/views/
    @param view:
    @param endpoint:
    @param url:
    @param pk:
    @param pk_type:
    @return:
    """

    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},
                     view_func=view_func, methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST',])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])
    # if dateRange:
    #     pass
    #     app.add_url_rule(f"{url}<startdatetime><enddatetime>", view_func=view_func,
    #                      methods=['GET'])
        # app.add_url_rule(f"{url}<startdatetime><enddatetime>", view_func=view_func,
        #                  methods=['GET'])