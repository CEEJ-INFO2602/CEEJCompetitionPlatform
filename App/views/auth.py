from flask import Flask
from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user
from flask_login import login_required, login_user, current_user, logout_user
from App.models import User
import csv
from datetime import datetime
from App.database import db
from App.models import Competition, Team, Member
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'App/uploads'

from.index import index_views

from App.controllers import (
    create_user,
    jwt_authenticate,
    login, 
    get_active_user,
    set_active_true,
    set_active_false,
    get_all_competitions,
    is_admin,
    get_all_competitions_by_alphabet,
    get_all_competitions_by_start_date,
    get_teams_by_alphabet,
    get_teams_by_score,
    delete_competition
)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')

'''
Page/Action Routes
'''

@auth_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)


@auth_views.route('/identify', methods=['GET'])
@login_required
def identify_page():
    return jsonify({'message': f"username: {current_user.username}, id : {current_user.id}"})


@auth_views.route('/render_login', methods=['GET'])
def render_login():
    return render_template('loginPage.html')

@auth_views.route('/login_action', methods=['GET', 'POST'])
def login_action():
    data = request.form
    user = login(data['username'], data['password'])
    if user:
        login_user(user)
        set_active_true(user)

        if is_admin(user):
            return redirect('/render_adminPage'), 200

        return redirect('/render_competitionsPage'), 200
    
    flash('bad username or password given')
    return render_template('loginPage.html'), 401

@auth_views.route('/logout_action')
def logout_action():
    logout_user()
    return render_template('index.html')

@auth_views.route('/render_signUp', methods=['GET'])
def render_signUp():
    return render_template('signUpPage.html')

@auth_views.route('/signUp_action', methods=['GET', 'POST'])
def signUp_action():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')

        if (password != confirmPassword):
            flash('Passwords do not match')
            return render_template('signUpPage.html'), 401


        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username Already Taken !!!')
            return render_template('signUpPage.html'), 401

        # Create a new user & Save the new user to the database
        create_user(username, password, access ="user")

        # Log in the user
        user=login(username, password)

        login_user(user)
        set_active_true(user)

        if is_admin(user):
            return redirect('/render_adminPage'), 200

        return redirect('/render_competitionsPage'), 200

    flask('ERROR SIGNING UP!')
    return render_template('signUpPage.html'), 401

@auth_views.route('/active_user', methods=['GET', 'POST'])
def active_user():
    username = get_active_user()
    return username


@auth_views.route('/render_competitionsPage', methods=['GET', 'POST'])
def render_competitionsPage():
    competitions = get_all_competitions()
    return render_template('competitionsPage.html', competitions=competitions)


@auth_views.route('/render_adminPage', methods=['GET', 'POST'])
def render_adminPage():
    competitions = get_all_competitions()
    return render_template('adminPage.html', competitions=competitions)

@auth_views.route('/sort_competitions_by_name_action_admin', methods=['GET', 'POST'])
def sort_competitions_by_name_action_admin():
    competitions = get_all_competitions_by_alphabet()
    return render_template('adminPage.html', competitions=competitions)

@auth_views.route('/sort_competitions_by_date_action_admin', methods=['GET', 'POST'])
def sort_competitions_by_date_action_admin():
    competitions = get_all_competitions_by_start_date()
    return render_template('adminPage.html', competitions=competitions)  

@auth_views.route('/sort_competitions_by_name_action', methods=['GET', 'POST'])
def sort_competitions_by_name_action():
    competitions = get_all_competitions_by_alphabet()
    return render_template('competitionsPage.html', competitions=competitions)

@auth_views.route('/sort_competitions_by_date_action', methods=['GET', 'POST'])
def sort_competitions_by_date_action():
    competitions = get_all_competitions_by_start_date()
    return render_template('competitionsPage.html', competitions=competitions) 
   
@auth_views.route('/render_createCompetitionsPage', methods=['GET'])
def render_createCompetitionsPage():
    return render_template('createCompetitionsPage.html') 



@auth_views.route('/upload', methods=['POST'])
def upload():
    comp_name = request.form['compName']
    start_date = datetime.strptime(request.form['startDate'], '%Y-%m-%d').date()
    end_date = datetime.strptime(request.form['endDate'], '%Y-%m-%d').date()

    csv_file = request.files['csvFile']
    if csv_file and allowed_file(csv_file.filename):
        filename = csv_file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        csv_file.save(file_path)
        process_csv_file(file_path, comp_name, start_date, end_date)
        return "File uploaded successfully"
    else:
        return "Error uploading file"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] == 'csv'

def process_csv_file(file_path, comp_name, start_date, end_date):
    admin_id = 1  
    competition = Competition(admin_id, comp_name, start_date, end_date)
    db.session.add(competition)
    db.session.flush()

    with open(file_path) as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            team_name = row['Team']
            score = row['Score']
            members = members['Participants']
            team = Team(competition.id, admin_id, team_name, score, members)
            db.session.add(team)
            db.session.flush()

    db.session.commit()

@auth_views.route('/delete_competition/<int:competition_id>', methods=['GET', 'POST'])
def delete_competition(competition_id):
    competition = Competition.query.filter_by(id=competition_id).first()
    if competition:
        db.session.delete(competition)
        db.session.commit()
        return redirect(url_for('auth_views.render_adminPage'))
    return redirect(url_for('auth_views.render_adminPage'))

    competition = Competition.query.filter_by(id=comp_id).first()
    if competition:
        db.session.delete(competition)
        db.session.commit()

        # Delete the CSV file for the competition
        csv_file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{comp_id}.csv")
        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)

        return f"Competition with ID {comp_id} deleted successfully"
    else:
        return f"Competition with ID {comp_id} not found"

@auth_views.route('/teamViewPage/<int:competition_id>')
def teamViewPage(competition_id):
    competition = Competition.query.filter_by(id=competition_id).first()
    teams = competition.teams
    return render_template('teamViewPage.html', teams=teams)

@auth_views.route('/teamViewPageAdmin/<int:competition_id>')
def teamViewPageAdmin(competition_id):
    competition = Competition.query.filter_by(id=competition_id).first()
    teams = competition.teams
    return render_template('teamViewPageAdmin.html', teams=teams)

@auth_views.route('/sort_teams_by_name_action', methods=['GET', 'POST'])
def sort_teams_by_name_action():
    teams = get_teams_by_alphabet()
    return render_template('teamViewPage.html', teams=teams)

@auth_views.route('/sort_teams_by_score_action', methods=['GET', 'POST'])
def sort_teams_by_date_action():
    teams = get_teams_by_score()
    return render_template('teamViewPage.html', teams=teams) 

@auth_views.route('/participantViewPage/<int:team_id>')
def participantViewPage(team_id):
    team = Team.query.filter_by(id=team_id).first()
    return render_template('participantViewPage.html', team=team)

@auth_views.route('/participantViewPageAdmin/<int:team_id>')
def participantViewPageAdmin(team_id):
    team = Team.query.filter_by(id=team_id).first()
    return render_template('participantViewPageAdmin.html', team=team)

'''
API Routes
'''

@auth_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@auth_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    create_user(data['username'], data['password'])
    return jsonify({'message': f"user {data['username']} created"})

@auth_views.route('/api/login', methods=['POST'])
def user_login_api():
  data = request.json
  token = jwt_authenticate(data['username'], data['password'])
  if not token:
    return jsonify(message='bad username or password given'), 401
  return jsonify(access_token=token)

@auth_views.route('/api/identify', methods=['GET'])
@jwt_required()
def identify_user_action():
    return jsonify({'message': f"username: {jwt_current_user.username}, id : {jwt_current_user.id}"})