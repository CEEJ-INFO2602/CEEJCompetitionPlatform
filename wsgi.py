import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup
import os
import csv
from datetime import datetime
from App.database import db
from App.models import Competition, Team, Member

UPLOAD_FOLDER = 'App/uploads'

from App.database import db, get_migrate
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, create_admin )

# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

app.config['UPLOAD_FOLDER'] = 'App/uploads'

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def initialize():
    db.drop_all()
    db.create_all()
    create_admin('bob', 'bobpass')
    create_user('pam', 'pampass')
    print('database intialized')

    comp_name = 'Animal competition'
    start_date = datetime.strptime('23/04/2023', '%d/%m/%Y').date()
    end_date = datetime.strptime('23/05/2023', '%d/%m/%Y').date()

    csv_file_path = os.path.join(UPLOAD_FOLDER, 'Animal competition.csv')
    if  os.path.exists(csv_file_path):
        process_csv_file(csv_file_path, comp_name, start_date, end_date)


def process_csv_file(file_path, comp_name, start_date, end_date):
    admin_id = 1  
    competition = Competition(admin_id, comp_name, start_date, end_date)
    db.session.add(competition)
    db.session.flush()

    competition.id = 1
    with open(file_path) as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            team_name = row['Team']
            score = row['Score']
            team = Team(competition.id, admin_id, team_name, score)
            db.session.add(team)
            db.session.flush()

            participants = row['Participants'].split(", ")
            for participant in participants:
                member = Member(team.id, admin_id, participant)
                db.session.add(member)

    db.session.commit()

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)