from App.database import db
from datetime import datetime

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    competitionId = db.Column(db.Integer, db.ForeignKey("competition.id"), nullable=False)
    adminId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    teamName = db.Column(db.String(120), nullable=False)
    score = db.Column(db.String(120), nullable = False)
    members = db.Column(db.String(200), nullable = False)
    
    def __init__(self, competitionId, adminId, teamName, score, members):
        self.competitionId = competitionId
        self.adminId = adminId
        self.teamName = teamName
        self.score = score
        self.members = members

    def to_json(self):
        return{
            "id": self.id,
            "competitionId": self.competitionId,
            "adminId": self.adminId,
            "teamName": self.teamName,
            "score": self.score,
            "members": self.members
        }