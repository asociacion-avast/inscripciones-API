import os
from . import create_app

environment = os.getenv('FLASK_ENV', 'production')
app = create_app(environment)

if __name__ == '__main__':
    app.run(debug=True)
