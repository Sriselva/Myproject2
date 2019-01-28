import os
from flask import Flask,render_template,request,redirect,url_for,flash,jsonify
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine
from flask_mysqldb import MySQL
from sqlalchemy.sql import select
from sqlalchemy.engine import reflection
from werkzeug.utils import secure_filename

from sqlalchemy import Table, Column,String, MetaData
UPLOAD_FOLDER = 'static/documents/'
ALLOWED_EXTENSIONS = set([ 'png','docx'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
Bootstrap(app)
app.secret_key = 'random string'

engine = create_engine('mysql://root@localhost/sql')
connection=engine.connect()
metadata = MetaData()
metadata.reflect(bind=engine)
selva = metadata.tables['selva']
#selva = Table('selva', metadata,Column('username', String),Column('password', String))
#metadata.create_all(engine)


@app.route("/")
def index():
		return render_template('index.html')

@app.route("/ddl",methods=['POST'])
def ddl():
	ide=request.form['id']
	print(ide)
	name=request.form['name']
	print(name)
	desgn=request.form['designation']
	print(desgn)
	phone=request.form['phone']
	print(phone)
	
	insert(name,desgn,phone)
	
	
		
	
#def allowed_file(filename):
	#return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
		
def insert(name,desgn,phone):
	ins = selva.insert().values(Name=name,Design=desgn,Phone=phone)
	insrt=connection.execute(ins)
	print(insrt)
	return render_template('index.html')
		
		



@app.route("/view")
def viewall():
	selt=select([selva])
	selctall=connection.execute(selt)
	return render_template('view.html', result = selctall)
	return jsonify({result:selctall})
		
@app.route("/viewone",methods=['post'])				
def view():
	id=request.args.get('id')
	selt=select([selva.c.Id,selva.c.Name,selva.c.Design,selva.c.Phone]).where(selva.c.Id==ide)
	res=connection.execute(selt)
	selct=res.fetchall()
	print(selct)
	return selct
	


@app.route("/edit")
def edit():
	id=request.args.get('id')
	up=select([selva.c.Id,selva.c.Name,selva.c.Design,selva.c.Phone]).where(selva.c.Id==id)
	res=connection.execute(up)
	"""for(dict) as row in res:
		print(row)
		return jsonify(res)"""
	return render_template('update.html',result=res)

@app.route("/delete")
def delete():
	id=request.args.get('id')
	connection.execute(selva.delete().where(selva.c.Id== id))
	return render_template('index.html')

@app.route("/update",methods=["post"])
def update():
	ide=request.form['id']
	name=request.form['name']
	desgn=request.form['designation']
	phone=request.form['phone']
	upt = selva.update().values(Name=name,Design=desgn,Phone=phone).where(selva.c.Id == ide )
	reslt=connection.execute(upt)
	return render_template("index.html")
	



if __name__ == "__main__":
	app.run(debug=True)