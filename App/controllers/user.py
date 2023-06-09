from App.models import User
from App.database import db

def get_active_user():
    allUsers = User.query.all()
    for u in allUsers:
        if (u.is_active == True):
            return u
    return "no hehe"

def create_user(username, password, access ="user"):
    user = get_user_by_username(username)
    if user:
        return None
    new_user = User(username = username, password = password, access = access)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def create_admin(username, password, access ="admin"):
    user = get_user_by_username(username)
    if user:
        return None
    new_user = User(username = username, password = password, access = access)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def update_access(id, access):
    user = get_user_by_id(id)
    if user:
        user.access = access
        db.session.add(user)
        db.session.commit()
        return user
    return None

def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user
    return None

def get_user_by_id(id):
    return User.query.get(id)

def get_all_users():
    return User.query.all()

def get_all_users_json():
    return [user.to_json() for user in get_all_users()]

def get_all_admins():
    return User.query.filter_by(access="admin").all()

def get_all_admins_json():
    return [admin.to_json() for admin in get_all_admins()]
  
def update_user(id, username="",password=""):
    user = get_user_by_id(id)
    if user:
        if username:
            user.username = username
        if password:
            user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
    return None

def is_admin(user):
    return user.get_access() == "admin"

def check_password(user, password):
    return user.check_password(password)


def delete_user(id):
    user = get_user_by_id(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False

def create_su():
    user = get_user_by_username("admin123")
    if not user:
        user = create_admin("admin123","admin123")
        print("admin created")
        db.session.add(user)
        return db.session.commit()
    return None
    