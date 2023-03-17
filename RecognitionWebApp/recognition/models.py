from recognition import db, login_manager

from flask_login import UserMixin

@login_manager.user_loader
def load_user(user):
    return Recognition.query.get(int(user))

class Recognition(db.Model, UserMixin):
    picture_id = db.Column(db.Integer, primary_key=True)
    picture_name = db.Column(db.String(20), nullable=False)
    picture_prediction = db.Column(db.Integer)

    def get_id(self):
        return self.picture_id
