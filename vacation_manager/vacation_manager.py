"""Vacation Manager"""

from vacation_manager import create_app

if __name__ == '__main__':
    app = create_app()
    app.run("0.0.0.0", port=80, debug=True, threaded=True)
