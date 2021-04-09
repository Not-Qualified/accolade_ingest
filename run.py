from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy as sa
from sqlalchemy import create_engine
import sqlalchemy as dba
import pymysql

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///elisa.sqlite"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123123123@localhost/elisa?charset=utf8mb4"

db = sa(app)

# engine = create_engine("mysql+pymysql://root:123123123@localhost/elisa?charset=utf8mb4")
engine = create_engine("sqlite:///elisa.sqlite")

connection = engine.connect()
# print(connection.dialect.has_table(connection, "p_adfwe_1233_url"))
# print(dir(connection))
# print(connection.engine)

@app.route('/', methods=["POST", "PUT"])
def hello_world():
	if request.method == "POST":
		context = {
			"url": request.args.get("url", ""),
			"project_id": request.args.get("project_id", ""),
			"cache_ttl": request.args.get("cache_ttl", False),
			"cache_grace": request.args.get("cache_grace", False),
			"status": request.args.get("status", False),
			"response_time": request.args.get("response_time", False),
			"cache_state": request.args.get("cache_state", True),
			"sitemap": request.args.get("sitemap", ""),
		}

		model = f'p_{context["project_id"]}_urls'
		if not connection.dialect.has_table(connection, model):
			print("New Table Creation Condition")
			def custom_table(model):
				data_dictionary = {
					"url": db.Column(db.String(500), unique=True, nullable=False, primary_key=True, ), 
					"cache_ttl": db.Column(db.Integer, nullable=False, ), 
					"cache_grace": db.Column(db.Integer, nullable=False, ), 
					"status": db.Column(db.Integer,  nullable=False, ), 
					"response_time": db.Column(db.Float,  nullable=False, ), 
					"cache_state": db.Column(db.String(10), default="True", ), 
					"sitemap": db.Column(db.String(1000), nullable=True, ), 
				}
				class_name = type(model, (db.Model, ), data_dictionary)
				return class_name
			table = custom_table(model)
			db.session.commit()
			db.create_all()
			table = table(
					url=request.args.get("url", ""),
					cache_ttl=request.args.get("cache_ttl", False),
					cache_grace=request.args.get("cache_grace", False),
					status=request.args.get("status", False),
					response_time=request.args.get("response_time", False),
					cache_state=request.args.get("cache_state", "True"),
					sitemap=request.args.get("sitemap", ""),
				)
			db.session.add(table)
		else:
			table_object = dba.Table(model, dba.MetaData(), autoload=True, autoload_with=engine, )
			qurey = dba.select([table_object]).where(table_object.columns.url == request.args.get("url", ""))
			if connection.execute(qurey).fetchall():
				print("Same")
				statement = dba.update(table_object)
				statement = statement.where(table_object.columns.url == request.args.get("url"))
				statement = statement.values(
						cache_ttl=request.args.get("cache_ttl", False),
						cache_grace=request.args.get("cache_grace", False),
						status=request.args.get("status", False),
						response_time=request.args.get("response_time", False),
						cache_state=request.args.get("cache_state", "True"),
						sitemap=request.args.get("sitemap", ""),
					)
				result = connection.execute(statement)
				print(result)
			else:
				print("New")
				statement = dba.insert(table_object).values(
						url=request.args.get("url", ""),
						cache_ttl=request.args.get("cache_ttl", False),
						cache_grace=request.args.get("cache_grace", False),
						status=request.args.get("status", False),
						response_time=request.args.get("response_time", False),
						cache_state=request.args.get("cache_state", "True"),
						sitemap=request.args.get("sitemap", ""),
					)
				result = connection.execute(statement)
			print(table_object)


			
		# db.session.add(Elisa(
		# 	url = context["url"],
		# ))

		db.session.commit()
		db.create_all()
		db.metadata.clear()
		return context
