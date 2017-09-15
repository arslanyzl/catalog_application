from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, League, Club, User


from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)


engine = create_engine('sqlite:///soccerteam.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token


    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]


    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"



def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
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

# DISCONNECT - Revoke a current user's token and reset their login_session



# JSON APIs to view Restaurant Information
@app.route('/leagues/<int:league_id>/league/JSON')
def JSON(league_id):
    league = session.query(League).filter_by(id=league_id).one()
    items = session.query(Club).filter_by(
        league_id=league_id).all()
    return jsonify(Clubs=[i.serialize for i in items])


@app.route('/leagues/JSON')
def leaguesJSON():
    leagues = session.query(League).all()
    return jsonify(leagues=[r.serialize for r in leagues])


# show all soccer league
@app.route('/')
@app.route('/leagues/')
def showLeagues():
    leagues = session.query(League).order_by(asc(League.name))
    if 'username' not in login_session:
        return render_template('publicleagues.html', leagues=leagues)
    return render_template('leagues.html', leagues=leagues)


# create new league
@app.route('/leagues/new/', methods=['GET', 'POST'])
def newLeague():
    if 'username' not in login_session:
         return redirect('/login')
    if request.method == 'POST':
        newLeague = League(name=request.form['name'], user_id=login_session['user_id'])
        session.add(newLeague)
        session.commit()
        flash('New Soccer League %s Created' % newLeague.name)
        return redirect(url_for('showLeagues'))
    else:
        return render_template('newLeague.html')


# edit league
@app.route('/leagues/<int:league_id>/edit/', methods=['GET', 'POST'])
def editLeague(league_id):
    editedLeague = session.query(League).filter_by(id=league_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedLeague.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this soccer league. Please create your own league in order to edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedLeague.name = request.form['name']
            session.add(editedLeague)
            session.commit()
            flash('Soccer League %s has been edited' % editedLeague.name)
            return redirect(url_for('showLeagues'))
    else:
        return render_template('editedleague.html', league_id=league_id,
                               league=editedLeague)


# delete league
@app.route('/leagues/<int:league_id>/delete/', methods=['GET', 'POST'])
def deleteLeague(league_id):
    deletedLeague = session.query(League).filter_by(id=league_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if deletedLeague.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this soccer league. Please create your own league in order to delete.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(deletedLeague)
        session.commit()
        flash('Soccer League %s has been deleted' % deletedLeague.name)
        return redirect(url_for('showLeagues'))
    else:
        return render_template('deletedleague.html', league_id=league_id,
                               league=deletedLeague)


# show teams in selected league
@app.route('/leagues/<int:league_id>/league')
def soccerClub(league_id):
    league = session.query(League).filter_by(id = league_id).one()
    creator = getUserInfo(league.user_id)
    items = session.query(Club).filter_by(league_id=league.id)
    if 'username' not in login_session:
        return render_template('publicteam.html', league=league, items=items)
    else:
        return render_template('team.html', league=league, items=items)

#add new team
@app.route('/leagues/<int:league_id>/league/new/', methods=['GET', 'POST'])
def newTeam(league_id):
    if 'username' not in login_session:
        return redirect('/login')
    league = session.query(League).filter_by(id = league_id).one()
    if login_session['user_id'] != league.user_id:
        return "<script>function myFunction() {alert('You are not authorized to add menu items to this league. Please create your own league in order to add items.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        newItem = Club(name=request.form['name'], founded=request.form['founded'],
                       description=request.form['description'], league_id = league_id)
        session.add(newItem)
        session.commit()
        flash("New Soccer Team %s Created!" % (newItem.name))
        return redirect(url_for('soccerClub', league_id = league_id))
    else:
        return render_template('newteamadding.html', league_id = league_id)


# select team for edit
@app.route('/leagues/<int:league_id>/league/select-to-edit/')
def selectEdit(league_id):
    league = session.query(League).filter_by(id = league_id).one()
    items = session.query(Club).filter_by(league_id=league.id)
    return render_template('selectedit.html', league=league, items=items)


# edit team
@app.route('/leagues/<int:league_id>/league/<int:team_id>/edit/', methods=['GET', 'POST'])
def editTeam(league_id, team_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Club).filter_by(id = team_id).one()
    league = session.query(League).filter_by(id = league_id).one()
    if login_session['user_id'] != league.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit team to this league. Please create your own league in order to edit teams.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['founded']:
            editedItem.founded = request.form['founded']
        if request.form['description']:
            editedItem.description = request.form['description']
        session.add(editedItem)
        session.commit()
        flash('Soccer Team %s has been edited' % editedItem.name)
        return redirect(url_for('soccerClub', league_id = league_id))
    else:
        return render_template('editedteam.html', league_id = league_id,
                               team_id = team_id, i=editedItem)


# select team for delete
@app.route('/leagues/<int:league_id>/league/select-to-delete/')
def selectDelete(league_id):
    league = session.query(League).filter_by(id = league_id).one()
    items = session.query(Club).filter_by(league_id=league.id)
    return render_template('selectdelete.html', league=league, items=items)


# delete team    
@app.route('/leagues/<int:league_id>/league/<int:team_id>/delete', methods=['GET', 'POST'])
def deleteTeam(league_id, team_id):
    if 'username' not in login_session:
        return redirect('/login')
    deleteItem = session.query(Club).filter_by(id = team_id).one()
    league = session.query(League).filter_by(id = league_id).one()
    if login_session['user_id'] != league.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete team from this league. Please create your own league in order to delete teams.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        flash('Soccer Team %s has been deleted' % deleteItem.name)
        return redirect(url_for('soccerClub', league_id = league_id))
    else:
        return render_template('deletedteam.html', i=deleteItem)

# disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showLeagues'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showLeagues'))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
