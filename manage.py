from app import create_app
from flask_cors import CORS
app = create_app(config_name='default')
CORS(app, supports_credentials=True)
app.run()
