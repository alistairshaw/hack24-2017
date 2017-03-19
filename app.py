from flask import Flask, render_template, jsonify
from sqlalchemy import text
from flask_sqlalchemy import SQLAlchemy
import database
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# View Routes
@app.route("/")
def index():
	return render_template('index.html')

@app.route("/project/<int:projectid>")
def project(projectid):
	return render_template('project.html')

@app.route("/project/commits/<int:projectid>")
def projectCommits(projectid):
    return render_template('project-commits.html')

@app.route("/project/<int:projectid>/<int:eventid>")
def projectEvent(projectid, eventid):
	return render_template('event.html')

@app.route("/profile/<int:userid>", defaults={'userid': None})
def profile(userid):
    return render_template('profile.html')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

@app.route("/new")
def new():
    return render_template('new.html')

# API Routes
@app.route("/api/user/<int:userid>")
def apiUser(userid):
	user = database.users.query.filter_by(id=userid).first()
	userJson = {
		"id" : user.id,
		"name" : user.name,
		"email" : user.email,
		"name" : user.name,
		"institution" : user.institution,
		"position" : user.position,
		"avatar" : user.avatar,
		"twitter" : user.twitter
	}
	return jsonify(userJson)

@app.route("/api/project/<int:projectid>")
def apiProject(projectid):
	project = database.projects.query.filter_by(id=projectid).first()
	projectJson = {
		"id" : project.id,
		"project_name" : project.project_name,
		"start_date" : project.start_date,
		"end_date" : project.end_date,
		"description" : project.description,
		"is_public" : project.isPublic
	}
	return jsonify(projectJson)

@app.route("/api/project/events/<int:projectid>")
def apiProjectEvent(projectid):
	documents = database.documents
	events = database.events
	users = database.users
	sql_text = "SELECT e.id, e.filename, e.created, u.name, u.avatar, d.id AS document_id, d.document_title FROM events AS e LEFT JOIN documents AS d ON e.document_id = d.id LEFT JOIN users AS u ON e.user_id = u.id"
	sql = text(sql_text)
	results = db.engine.execute(sql)
	eventsJson = {}
	for i in results:
		json = {
			"id" : i.id,
			"document_id" : i.document_id,
			"filename" : i.filename,
			"created" : i.created,
			"document_title" : i.document_title,
			"name" : i.name,
			"avatar" : i.avatar
		}
		eventsJson[i.id] = json

	final = {
		"total" : 7,
		"data" : eventsJson
	}
	return jsonify(final)

@app.route("/api/projects/getprojectsbyuser/<int:userid>")
def apiProjectByUser(userid):
	projects = database.projects
	#projectsData = database.projects_users.query.join(projects).add_columns(projects_users.id, projects.id, projects.project_name, projects.start_date, projects.end_date, projects.description, projects.isPublic).filter_by(user_id=userid)
	projectJson = {}
	for i in projects:
		json = {
			"id" : i.id,
			"project_name" : i.project_name,
			"start_date" : i.start_date,
			"end_date" : i.end_date,
			"description" : i.description,
			"is_public" : i.isPublic
		}
		projectJson[i.id] = json
	return jsonify(projectJson) 

@app.route("/api/comments/<int:documentid>")
def apiEventComments(documentid):
	comments = database.comments.query.filter_by(document_id=documentid)
	commentsJson = {}
	for i in comments:
		logging.info('xx')
		json = {
			"id" : i.id,
			"user_id" : i.user_id,
			"document_id" : i.document_id,
			"comment" : i.comment,
			"created" : i.created
		}
		commentsJson[i.id] = json
	return jsonify(commentsJson)

@app.route("/api/documents/getdocumentsbyuser/<int:userid>")
def apiGetDocumentsByUser(userid):
	#documents = database.documents
	return None

if __name__ == "__main__":
	app.run()
