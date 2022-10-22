from src import db


class Updatable:
    def update(self, data):
        for attr, value in data.items():
            setattr(self, attr, value)


class Pai(db.Model, Updatable):
    __tablename__ = "pai"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    filhos = db.relationship("Filho", overlaps="filhos")


class Filho(db.Model, Updatable):
    __tablename__ = "filho"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    pai_id = db.Column(db.ForeignKey("pai.id", ondelete="CASCADE"))
    professores = db.relationship("Professor", secondary="filho_professor")
    pai = db.relationship("Pai")


class FilhoProfessor(db.Model):
    __tablename__ = "filho_professor"

    professor_id = db.Column(
        db.ForeignKey("professor.id", ondelete="CASCADE"), primary_key=True
    )
    filho_id = db.Column(
        db.ForeignKey("filho.id", ondelete="CASCADE"), primary_key=True
    )

    professor = db.relationship("Professor", overlaps="professores")
    filho = db.relationship("Filho", overlaps="professores")


class Professor(db.Model):
    __tablename__ = "professor"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
