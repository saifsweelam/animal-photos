from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, abort


from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Species, Photo, User

from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

# Connection with Database
engine = create_engine('sqlite:///animalphotos.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Setting Constants
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Animal Photos"

# Initializing Flask app
app = Flask(__name__)

# Main Species are displayed in homepage
@app.route('/')
@app.route('/home/')
@app.route('/species/')
def showSpecies():
    species = session.query(Species).all()
    if 'username' not in login_session:
        return render_template('publichome.html', species=species)
    return render_template('home.html', species=species)

# A webpage to display photos in a species
@app.route('/species/<int:species_id>/')
def showPhotos(species_id):
    species = session.query(Species).filter_by(id=species_id).one()
    photos = session.query(Photo).filter_by(species_id=species_id).all()
    if 'username' not in login_session:
        return render_template('publicphotos.html', photos=photos, species=species)
    return render_template('photos.html', photos=photos, species=species)


# Show a specific Photo
@app.route('/species/<int:species_id>/<int:photo_id>/')
def showAPhoto(species_id, photo_id):
    species = session.query(Species).filter_by(id=species_id).one()
    photo = session.query(Photo).filter_by(id=photo_id).one()
    creator = session.query(User).filter_by(id=photo.user_id).one()
    if 'username' not in login_session:
        return render_template('publicphotoview.html', species=species, creator=creator, photo=photo)
    if login_session['username'] != creator.username:
        return render_template('photoview.html', species=species, creator=creator, photo=photo)
    return render_template('userphotoview.html', species=species, creator=creator, photo=photo)


# View User's photos
@app.route('/profile/photos/')
def showUploads():
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    user = session.query(User).filter_by(
        username=login_session['username']).one()
    photos = session.query(Photo).filter_by(user_id=user.id).all()
    return render_template('uploads.html', user=user, photos=photos)


# Add a new Species
@app.route('/species/new/', methods=['GET', 'POST'])
def newSpecies():
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    if request.method == 'GET':
        return render_template('addspecies.html')
    if request.method == 'POST':
        name = request.form['name']
        species = Species(name=name)
        session.add(species)
        session.commit()
        flash('Successfully created a new species "{}"'.format(species.name))
        return redirect(url_for('showSpecies'))

# Add a new Photo
@app.route('/species/new/photo/', methods=['GET', 'POST'])
def newPhoto():
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    species = session.query(Species).all()
    if request.method == 'GET':
        return render_template('addphoto.html', species=species)
    if request.method == 'POST':
        title = request.form['title']
        url = request.form['url']
        description = request.form['description']
        species_name = request.form['species']
        species = session.query(Species).filter_by(name=species_name).one()
        user = session.query(User).filter_by(
            username=login_session['username']).one()
        photo = Photo(title=title, url=url,
                      description=description, species=species, user=user)
        session.add(photo)
        session.commit()
        flash('Successfully created a new photo')
        return redirect(url_for('showPhotos', species_id=species.id))

# Edit an existing Photo
@app.route('/species/<int:species_id>/<int:photo_id>/edit/', methods=['GET', 'POST'])
def editPhoto(species_id, photo_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    photo = session.query(Photo).filter_by(id=photo_id).one()
    creator = session.query(User).filter_by(id=photo.user_id).one()
    all_species = session.query(Species).all()
    if creator.username != login_session['username']:
        return render_template('unauthorized.html')
    if request.method == 'GET':
        return render_template('editphoto.html', photo=photo, species=all_species)
    if request.method == 'POST':
        if request.form['title'] != photo.title:
            photo.title = request.form['title']
        if request.form['url'] != photo.url:
            photo.url = request.form['url']
        if request.form['description'] != photo.description:
            photo.description = request.form['description']
        if request.form['species'] != photo.species.name:
            species_name = request.form['species']
            photo.species = session.query(Species).filter_by(name=species_name).one()
        session.add(photo)
        session.commit()
        flash('Successfully modified photo')
        return redirect(url_for('showAPhoto', species_id=photo.species_id, photo_id=photo.id))


# Delete a Photo
@app.route('/species/<int:species_id>/<int:photo_id>/delete/', methods=['POST', 'GET'])
def deletePhoto(species_id, photo_id):
    if 'username' not in login_session:
        return redirect(url_for('showLogin'))
    photo = session.query(Photo).filter_by(id=photo_id).one()
    creator = session.query(User).filter_by(id=photo.user_id).one()
    if creator.username != login_session['username']:
        return render_template('unauthorized.html')
    if request.method == 'GET':
        return render_template('deletephoto.html', photo=photo)
    if request.method == 'POST':
        session.delete(photo)
        session.commit()
        flash('Successfully deleted photo')
        return redirect(url_for('showPhotos', species_id=species_id))

# Route for Login Page
@app.route('/login/', methods=['GET','POST'])
def showLogin():
    if request.method == 'GET':
        if 'username' in login_session:
            flash('You\'re already logged in')
            return redirect(url_for('showSpecies'))
        state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                        for x in range(32))
        login_session['state'] = state
        return render_template('login.html', STATE=state)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = session.query(User).filter_by(email=email).one()
        if not user or not user.verify_password(password):
            return "<script>alert('Check that you enter correct data for E-mail & password'); location.href='/login';</script>"
        login_session['username'] = user.username
        login_session['email'] = user.email
        if user.picture:
            login_session['picture'] = user.picture
        flash('Successfully logged in as {}'.format(login_session['username']))
        return redirect(url_for('showSpecies'))


# Route for Registering a new User
@app.route('/register/', methods=['GET', 'POST'])
def showRegister():
    if request.method == 'GET':
        if 'username' in login_session:
            flash('You\'re already logged in')
            return redirect(url_for('showSpecies'))
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        picture = request.form['picture']
        if username is None or email is None or password is None:
            return "<script>alert('Please enter your Name, E-mail & Password'); location.href='/register';</script>"
        if session.query(User).filter_by(email = email).first() is not None:
            return "<script>alert('User already exists'); location.href='/login';</script>"
        newUser = User(username=username, email=email)
        if picture:
            newUser.picture = picture
        newUser.hash_password(password)
        session.add(newUser)
        session.commit()
        flash('User was created Successfully. You can login now.')
        return redirect(url_for('showLogin'))


# Method to connect to Google and Login
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
        print("Token's client ID does not match app's.")
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

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session['email'])
    login_session['user_id'] = user_id

    # See if a user exists, if it doesn't make a new one

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print('done!')
    return output

# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/disconnect/')
def disconnect():
    if 'gplus_id' in login_session:
        # Only disconnect a connected user.
        access_token = login_session.get('access_token')
        if access_token is None:
            response = make_response(
                json.dumps('Current user not connected.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
        url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
        h = httplib2.Http()
        h.request(url, 'GET')

        # Reset the user's sesson.
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash('Successfully Disconnected')

        return redirect(url_for('showSpecies'))
    else:
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        
        flash('Successfully Disconnected')

        return redirect(url_for('showSpecies'))



# API Endpoints

# Get All Species
@app.route('/API/species/')
def showSpeciesJSON():
    species = session.query(Species).all()
    return jsonify(species=[i.serialize for i in species])

# Get All Photos
@app.route('/API/photos/')
def showAllPhotosJSON():
    photos = session.query(Photo).all()
    return jsonify(photos=[i.serialize for i in photos])

# Get Photos of certain species
@app.route('/API/species/<int:species_id>')
def showPhotosJSON(species_id):
    photos = session.query(Photo).filter_by(species_id=species_id).all()
    return jsonify(photos=[i.serialize for i in photos])

# Get a certain photo
@app.route('/API/species/<int:species_id>/<int:photo_id>')
def showAPhotoJSON(species_id, photo_id):
    photo = session.query(Photo).filter_by(species_id=species_id, id=photo_id).one()
    return jsonify(photo_data=photo.serialize)


# Functions related to users


def createUser(email):
    newUser = User(username=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded=False)
