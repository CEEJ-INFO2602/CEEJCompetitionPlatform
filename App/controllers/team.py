from App.database import db
from App.models.team import Team
from datetime import datetime, timedelta

def create_team(competitionId, adminId, teamName, score):
    team = Team(competitionId = competitionId, adminId = adminId, teamName = teamName, score = score)
    db.session.add(team)
    db.session.commit()
    return team

def get_team_by_id(id):
    return Team.query.get(id)

def get_team_by_name(teamName):
    return Team.query.filter_by(teamName = teamName).first()

def get_team_by_name_json(teamName):
    return get_team_by_name(teamName).to_json()

def get_teams_by_alphabet():
    return Team.query.order_by(Team.teamName).all()

def get_teams_by_alphabet_json():
    return [team.to_json() for team in get_teams()]

def get_teams_by_score():
    return Team.query.order_by(-Team.score).all()

def get_teams_by_score_json():
    return [team.to_json() for team in get_teams_by_score()]

def update_team(id, teamName, score): 
    team = get_team_by_id(id)
    if team:
        if teamName:
            team.teamName = teamName
        if score:
            team.score = score
        db.session.add(team)
        db.session.commit()
        return team
    return None

def delete_team(id): 
    team = get_team_by_id(id)
    if team:
        db.session.delete(team)
        db.session.commit()
        return True
    return False

def get_team_by_id_json(id):
    return get_team_by_id(id).to_json()

