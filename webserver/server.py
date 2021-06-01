#!/usr/bin/env python

"""
Columbia's COMS W4111.003 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
import json
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, url_for, flash
from forms import PaitientRegistrationForm
from flask_caching import Cache
import logging
from flask import request


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@104.196.152.219/proj1part2
#
# For example, if you had username biliris and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://biliris:foobar@104.196.152.219/proj1part2"
#
DATABASEURI = "postgresql://im2594:4005@35.227.37.35/proj1part2"

#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
# engine.execute(
# """CREATE TABLE IF NOT EXISTS test (
# id serial,
#  name text
# );""")
# engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print ("uh oh, problem connecting to database")
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
def index():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  #  print (request.args)
  #
  # example of a database query
  #
  #  cursor = g.conn.execute("SELECT name FROM test")
  #  names = []
  #  for result in cursor:
  #    names.append(result['name'])  # can also be accessed using result[0]
  #  cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  #  context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html")

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#


# a general search for the pages
# @app.route('/general_search')
# def general_search():

#     results_paitients = []
#     results_office_location = []
#     results_provides_service = []
    
#     return render_template("general_search.html", Paitients=results_paitients, office_location=results_office_location, provides_service=results_provides_service)


# @app.route('/specialty_search', methods=['GET'])
# def specialty_search():
#   query=request.args.get('query')
    
#   print ('searching facility name')
#   print (query)
    
#   cursor = g.conn.execute("SELECT distinct specality FROM provides_service", query)
#   rows=cursor.fetchall()

#   print(rows)
#   print("TESTSSS")
    
#   cursor.close()

#   return render_template("specialty_search.html", Specialty=rows)

@app.route('/general_search', methods=['GET'])
def general_search():

    query=request.args.get('query')
    
    print ('searching facility name')
    
    cursor = g.conn.execute("SELECT distinct facility_name FROM provides_service LIMIT 100", query)
    rows=cursor.fetchall()
    
    cursor.close()
    
    #updating rows by addingfacility_data=rows
    return render_template("general_search.html", Medicaid_Provider=rows)


#search by facility name
@app.route('/search_facility_name', methods=['GET'])
def search_facility_name():

    query=request.args.get('query')
    
    print ('searching facility name')
    
    cursor = g.conn.execute("SELECT distinct * FROM provides_service p JOIN office_location k ON k.provider_id=p.provider_id WHERE facility_name= %s", query)
    rows=cursor.fetchall()

    cursor.close()
    
    #updating rows by addingfacility_data=rows
    return render_template("search_results.html", facility_data=rows)


@app.route('/search_speciality_name', methods=['GET'])
def search_speciality_name():

    query=request.args.get('query')
    
    cursor = g.conn.execute("SELECT distinct * FROM provides_service p JOIN office_location k ON k.provider_id=p.provider_id WHERE speciality= %s LIMIT 100", query)
    rows=cursor.fetchall()
    
    print(rows)

    cursor.close()
    
    #updating rows by addingfacility_data=rows
    return render_template("search_results_speciality.html", speciality_data=rows)




@app.route('/specialty_search', methods=['GET'])
def search_specialty():

    query=request.args.get('query')
    
    cursor = g.conn.execute("SELECT distinct speciality from provides_service", query)
    rows=cursor.fetchall()

    cursor.close()
    
    #updating rows by addingfacility_data=rows
    return render_template("speciality_search.html", specialty_data=rows)



@app.route('/custom_search', methods=['GET'])
def custom_search():

    query=request.args.get('query')
    
    cursor = g.conn.execute("SELECT distinct speciality from provides_service", query)
    rows=cursor.fetchall()

    cursor.close()
    
    #updating rows by addingfacility_data=rows
    return render_template("custom_search.html", specialty_data=rows)



  
@app.route('/custom_search_result', methods=['GET', 'POST'])
def custom_search_result():

    query=request.args.get('query')
    county=request.args.get('county')
    
    cursor = g.conn.execute("SELECT distinct * FROM office_location NATURAL JOIN provides_service WHERE speciality =%s and county =%s limit 100", query, county)
    rows=cursor.fetchall()

    cursor.close()

    cursor2 = g.conn.execute("SELECT distinct * FROM office_location NATURAL JOIN provides_service WHERE speciality =%s and county =%s limit 100", query, county)
    rows2=cursor2.fetchall()

    cursor2.close()

    
    
    #updating rows by addingfacility_data=rows
    return render_template("custom_search_results.html", specialty_data=rows, data=rows2)


#search by the most occuring data
@app.route('/search_most_ouccurinig', methods=['GET'])
def search_most_ouccurinig():

  query = request.args.get('query')
  print ('most ouccring')
  
  cursor = g.conn.execute("select distinct facility_name, count(facility_name)AS most_occuring from provides_service natural join office_location group by facility_name order by most_occuring desc limit 1", query)
  rows = cursor.fetchall()

  cursor.close()
  
  return render_template("search_most_ouccurinig.html",  data= rows)



@app.route('/paitient_registration', methods=['GET', 'POST'])
def register():
    form = PaitientRegistrationForm()
    if form.validate_on_submit():
        flash(f'Success')
        return redirect(url_for('index'))
    return render_template('paitient_registration.html', form=form)
    

# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
  return redirect('/')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print ("running on %s:%d" % (HOST, PORT))
    app.run(host=HOST, port=PORT, debug=True, threaded=threaded)

  run()
