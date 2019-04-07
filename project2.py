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

CLIENT_ID = json.loads(
    open('client_secret.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "ignate Application"
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



@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print( "done!")
    return output


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


