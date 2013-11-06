from moxie import create_app
from moxie.core.db import db

app = create_app()
with app.blueprint_context('notifications'):
    db.create_all()
