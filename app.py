from backend import create_app, db, models
from flask_migrate import Migrate

from config import DevelopmentConfig

app = create_app(DevelopmentConfig)
migrate = Migrate(app, db)



