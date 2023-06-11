env\Scripts\activate.bat
set FLASK_APP=project
set FLASK_ENV=development

flask run



flask db migrate
flask db upgrade

python:
from project import create_app, db
app = create_app()
app.app_context().push()
db.create_all()
exit()