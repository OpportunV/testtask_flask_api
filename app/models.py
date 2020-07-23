from app.app import db


class Task(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(30), nullable=False, default='in progress')
    filename = db.Column(db.String(50))
    
    @property
    def completed(self):
        if self.status.lower() in ['completed', 'done', 'finished']:
            return True
        return False
    
    def __repr__(self):
        return f'Task<{self.id_=}, {self.url=}, {self.status=}, {self.filename=}>'
