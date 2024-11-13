from flask import jsonify

def api_error(message, status_code):
    response = jsonify({
        "success": False,
        "message": message
    })
    response.status_code = status_code
    return response


def page_not_found(e):
    return api_error("Not found", 404)

def forbidden(e):
    return api_error("Forbidden", 403)

def bad_request(e):
    return api_error("Bad request", 400)

def internal_server_error(e):
    return api_error("Internal server error", 500)

def register_errors(app):
    app.register_error_handler(400, bad_request)
    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

