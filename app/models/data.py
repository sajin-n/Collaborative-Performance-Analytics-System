from app import db
from datetime import datetime


class Team(db.Model):
    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    team_code = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    project_name = db.Column(db.String(200))
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    students = db.relationship("Student", backref="team", cascade="all, delete-orphan")
    submissions = db.relationship(
        "Submission", backref="team", cascade="all, delete-orphan"
    )
    metrics = db.relationship(
        "TeamMetric", backref="team", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Team {self.team_code}>"


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)
    enrollment_year = db.Column(db.Integer)
    major = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    submissions = db.relationship(
        "Submission", backref="student", cascade="all, delete-orphan"
    )
    metrics = db.relationship(
        "StudentMetric", backref="student", cascade="all, delete-orphan"
    )
    peer_reviews = db.relationship(
        "PeerReview", backref="reviewer", foreign_keys="PeerReview.reviewer_id"
    )
    reviewed = db.relationship(
        "PeerReview", backref="reviewee", foreign_keys="PeerReview.reviewee_id"
    )

    def __repr__(self):
        return f"<Student {self.student_id}>"


class Submission(db.Model):
    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)
    submission_type = db.Column(
        db.String(50)
    )  # 'code', 'documentation', 'report', etc.
    commit_hash = db.Column(db.String(100))
    lines_changed = db.Column(db.Integer, default=0)
    files_modified = db.Column(db.Integer, default=0)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Submission {self.id}>"


class StudentMetric(db.Model):
    __tablename__ = "student_metrics"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer, db.ForeignKey("students.id"), nullable=False, index=True
    )
    metric_name = db.Column(
        db.String(100), nullable=False
    )  # 'contribution', 'attendance', 'commits', etc.
    metric_value = db.Column(db.Float)
    calculated_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("student_id", "metric_name", name="uq_student_metric"),
    )

    def __repr__(self):
        return f"<StudentMetric {self.metric_name}={self.metric_value}>"


class TeamMetric(db.Model):
    __tablename__ = "team_metrics"

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(
        db.Integer, db.ForeignKey("teams.id"), nullable=False, index=True
    )
    metric_name = db.Column(
        db.String(100), nullable=False
    )  # 'balance', 'performance', 'progress', etc.
    metric_value = db.Column(db.Float)
    calculated_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("team_id", "metric_name", name="uq_team_metric"),
    )

    def __repr__(self):
        return f"<TeamMetric {self.metric_name}={self.metric_value}>"


class PeerReview(db.Model):
    __tablename__ = "peer_reviews"

    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    reviewee_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable=False)
    rating = db.Column(db.Integer)  # 1-5 scale
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<PeerReview {self.reviewer_id}->{self.reviewee_id}>"


class Attendance(db.Model):
    __tablename__ = "attendance"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default="present")  # 'present', 'absent', 'late'
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint("student_id", "date", name="uq_attendance"),)

    def __repr__(self):
        return f"<Attendance {self.student_id}-{self.date}>"
