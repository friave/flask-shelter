env\Scripts\activate.bat
flask run

flask db migrate
flask db upgrade

python:
from project import create_app, db
app = create_app()
app.app_context().push()
db.create_all()
exit()