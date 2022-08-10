from sqlalchemy.ext.hybrid import hybrid_property
from extensions import db, pwd_context


class User(db.Model):
    """Basic user model"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    is_project_manager = db.Column(db.Boolean, default=False)
    is_developer = db.Column(db.Boolean, default=True)
    projects = db.relationship("Project", back_populates="project_manager")
    tasks = db.relationship("TaskDeveloper", back_populates="assignee")

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def __repr__(self):
        return f"User::{self.username}"


class TokenBlocklist(db.Model):
    """Blocklist representation"""

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    token_type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)

    user = db.relationship("User", lazy="joined")

    def to_dict(self):
        return {
            "token_id": self.id,
            "jti": self.jti,
            "token_type": self.token_type,
            "user_identity": self.user_identity,
            "revoked": self.revoked,
            "expires": self.expires,
        }


class Project(db.Model):
    """Basic Project model"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    project_manager_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    project_manager = db.relationship("User", back_populates="projects")
    tasks = db.relationship("Task", back_populates="project")

    def __repr__(self):
        return f"Project::{self.title}"


class TaskDeveloper(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"), primary_key=True)
    task = db.relationship("Task", back_populates="assignees")
    assignee = db.relationship("User", back_populates="tasks")


class Task(db.Model):
    """Basic task model"""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    project = db.relationship("Project", back_populates="tasks")
    assignees = db.relationship("TaskDeveloper", back_populates="task")

    def __repr__(self):
        return f"Task::{self.title}"
