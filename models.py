from DogAgeReminder import db, app


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # login will be the username
    login = db.Column(db.String(20))
    pw_hash = db.Column(db.String(64))
    email = db.Column(db.String(50), unique=True)


class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text())
    date_of_birth = db.Column(db.DateTime(timezone=False))
    weeks = db.Column(db.Integer)
    age = db.Column(db.DateTime(timezone=False))

    # references the id of the user who owns that pet
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # each user now has an attribute called 'pets'
    owner = db.relationship('User', backref='pets')


db.create_all(app=app)
