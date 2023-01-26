#! /usr/bin/env python3
from flask import Flask, render_template, url_for, request
from data import *


# Global variable for database
db = []

# A dictionary that contains translations for sortable fields
sort_by_items = {"project_name":"Projektnamn", "start_date":"Startdatum", "end_date":"Slutdatum", "project_id":"Projekt-id", "group_size":"Gruppstorlek"}



# Loads JSON file into db
def load_db():
    global db
    db = load("data.json")





app = Flask (__name__)

@app.route ("/")

# Returns an html file for start page
def index():
    global db
    load_db()
    found_projects = search(db, "end_date", sort_order="desc")
    recent_projects = found_projects[:3]

    #Creates an dynamic page containing the last tre projects
    return render_template("index.html", projects = recent_projects)

@app.route ("/list")

# Returns an html page containing search option to a list of projects
def project_list():
    global db, sort_by_items
    load_db()
    found = []
    db_techniques = get_techniques(db)
    search_for = request.args.get("search", "")
    techniques = request.args.getlist("technique")
    search_fields = request.args.getlist("search_field", None)
    if search_fields == []:
        search_fields = None
    sort_by = request.args.get("sort", "project_name")
    order = request.args.get("order", "desc")
    found = search(db, sort_by = sort_by, sort_order = order, techniques = techniques, search = search_for, search_fields = search_fields)
                          
    return render_template("project_list.html", projects = found , search = search_for, sort = sort_by, sort_by_items = sort_by_items , order = order, tech_check = techniques, search_check = search_fields, techniques = db_techniques)

@app.route("/project/<int:id>")

# Creates an html page based on given id corresponding to project id
def project (id):
    global db
    load_db()
    project = get_project(db, id)
    return render_template("project.html", project = project)
    
@app.route("/techniques")
# Creates an html page containing a list of projects using selected techniqeus
def techniques():
    global db
    load_db()
    techniques = request.args.getlist("techniques")
    
    found = search(db, techniques = techniques)
    print(found)
    return render_template("techniques.html", projects = found, tech_check = techniques)



@app.errorhandler(404)
def handle_bad_request(e):
    return render_template("404.html")

if __name__ == "__main__":
    app.run(debug=True)

