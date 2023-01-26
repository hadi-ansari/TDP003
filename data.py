#! /usr/bin/env python3
import json


#Load JSON file containing project data
def load(file_name):
    try:
        with open(file_name, "r", encoding = "utf-8") as f:
            projects = json.load(f)
            projects.sort(key = lambda i: i["project_id"])
            return projects
    except:
        return None

# Return number of projects in a database
def get_project_count(db):
    if db != None:
        return len(db)
    return 0

# Returns project matching given id
def get_project(db, id):
    if db != None:
        for i in db:
            if i["project_id"] == id:
                return i

    return None


# Fetches and sorts projects matching criteria from the specified list
def search(db, sort_by="project_name", sort_order="desc", techniques = None, search=None, search_fields=None):
    found = []
#---------------------------------------- search ----------------------------------------
    print(techniques)
    if search == None:
        search = ""
    if db == None:
        return []
    if search_fields == []:
        return []
    
    if search_fields == None:
        for p in db:
            for field in p:
                if search.upper() in str(p[field]).upper():
                    found.append(p)
                    break
                    
    elif search_fields != None:
        for p in db:
            for field in search_fields:
                if search.upper() in str(p[field]).upper():
                    found.append(p)
                    break
    
    
    if techniques != None and techniques != []:
        found2 = found.copy()
        for p in found2:
            result =  all(elem in p["techniques_used"]  for elem in techniques )
            if not result:
                found.remove(p)
            
#---------------------------------------- sort ----------------------------------------
# key = lambda i: i[sort_by] => decide in which field projects in database should be sorted in
    if sort_order == "asc":
        found.sort(key = lambda i: i[sort_by])
    elif sort_order == "desc":
        found.sort(reverse = True, key = lambda i: i[sort_by])
    
    return found

# Returns all techniques used by projects in database
def get_techniques(db):
    techniques = []
    if db != None:
        for project in db:
            for technique in project["techniques_used"]:
                techniques.append(technique)

        # Remove any duplicates from a List
        techniques = list(dict.fromkeys(techniques))
        # Sort a technique list alphabetically
        techniques.sort()
    
    return techniques


# Collects and returns statistics for all techniques in the specified project list.
def get_technique_stats(db):
    technique_stats = {}
    techniques = get_techniques(db)
    for technique in techniques:
        technique_stats[technique] = []
        for project in db:
            if technique in project["techniques_used"]:
                dic ={}
                dic["id"] = project["project_id"]
                dic["name"] = project["project_name"]
                technique_stats[technique].append(dic)
    return technique_stats

def main():
    pass
    
    
# ----------------- Main program --------------- #
if __name__ == "__main__":
    main()

