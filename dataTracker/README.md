pip3 install flask
pip3 install flask-wtf
pip3 install flask-sqlalchemy
pip3 install flask-brcypt
pip3 install Pillow
pip3 install WTForms-Components
pip install paginate-sqlalchemy


initializing database
	$python3
	$from datatracker import create_app
	$app = create_app()
	$app.app_context().push()
	$db.create_all()