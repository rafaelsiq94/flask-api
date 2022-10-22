from src import db


class Pai(db.Model):  # type: ignore
    __tablename__ = "pai"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    filhos = db.relationship("Filho")

    def update(self, data):
        for k, v in data.items():
            setattr(self, k, v)
        return self


class Filho(db.Model):  # type: ignore
    __tablename__ = "filho"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    pai_id = db.Column(db.ForeignKey("pai.id", ondelete="CASCADE"))
    professores = db.relationship("Professor", secondary="filho_professor")
    pai = db.relationship("Pai")


class FilhoProfessor(db.Model):  # type: ignore
    __tablename__ = "filho_professor"

    professor_id = db.Column(
        db.ForeignKey("professor.id", ondelete="CASCADE"), primary_key=True
    )
    filho_id = db.Column(
        db.ForeignKey("filho.id", ondelete="CASCADE"), primary_key=True
    )

    professor = db.relationship("Professor")
    filho = db.relationship("Filho")


class Professor(db.Model):  # type: ignore
    __tablename__ = "professor"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
