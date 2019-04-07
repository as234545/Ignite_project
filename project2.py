from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from database_setup import Base, CatalogItem, User
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
import json
from flask import make_response
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
from apiclient import discovery
import httplib2
from oauth2client import client
import requests

app = Flask(__name__)


# Create session and connect to DB
# engine = create_engine('sqlite:///catalog.db')
# must delete when deploying
engine = create_engine('sqlite:///catalog.db' , connect_args={'check_same_thread': False}) #must delete at deplyment
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

#  anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)
    # "The current session state is %s" % login_session['state']



@app.route('/')
def First():
  return render_template('First.html' )

@app.route('/catalogs')
def showCatalogs():
  items = session.query(CatalogItem).all()
  return render_template('catalog.html', items=items)


@app.route('/catalogPublic')
def showCatalogsPublic():
  itemsp = session.query(CatalogItem).all()
  return render_template('publicPage.html', itemsp=itemsp)


@app.route('/catalog/new/', methods=['GET', 'POST'])
def newCatalogItem():
  if request.method == 'POST':
    newCatalog = CatalogItem(title=request.form.get('title'), content=request.form.get(
        'content'), catalog_type=request.form.get('catalog_type'))
    session.add(newCatalog)
    session.commit()
    flash("new post has been created!")
    return redirect(url_for('showCatalogs'))
  else:
    return render_template('newCatalog.html')

# Task 2: Create route for editMenuItem function here


@app.route('/catalog/<int:catalog_id>/edit/', methods=['GET', 'POST'])
def editCatalogItem(catalog_id):
  editedpost = session.query(CatalogItem).filter_by(id=catalog_id).first()
  if request.method == 'POST':
    if request.form.get('title'):
      editedpost.title = request.form.get('title')
    if request.form.get('content'):
      editedpost.content =  request.form.get('content')
    if request.form.get('catalog_type'):
      editedpost.catalog_type =  request.form.get('catalog_type')
    session.add(editedpost)
    session.commit()
    flash("post has been edited")
    return redirect(url_for('showCatalogs'))
  else:
    return render_template('editcatalogitem.html', i=editedpost)

# Task 3: Create a route for deleteMenuItem function here


@app.route('/catalog/<int:catalog_id>/delete/', methods=['GET', 'POST'])
def deleteCatalogItem(catalog_id):
    deletepost = session.query(CatalogItem).filter_by(id=catalog_id).first()
    if request.method == 'POST':
        session.delete(deletepost)
        session.commit()
        flash("post has been deleted")
        return redirect(url_for('showCatalogs'))
    else:
        return render_template('deletecatalogitem.html', catalog=deletepost)# catalog here is a cursor that is user in the html page



if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(port=5000)


