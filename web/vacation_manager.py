"""Vacation Manager"""

from web.app import app

if __name__ == '__main__':
    app.run("0.0.0.0", port=80, debug=True, threaded=True)
