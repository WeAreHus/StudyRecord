class User(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer,primary_key=True)
    adminname = db.Column(db.String(10),unique=True)
    password = db.Column(db.String(16))

    def __init__(self,username,password):
        self.username  = username
        self.password = password
    def __repr__(self):
        return '<User %r>' % self.username
        