from models import Task, Project, TaskDeveloper
from extensions import ma, db


class ProjectSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)

    class Meta:
        model = Project
        sqla_session = db.session
        load_instance = True


class TaskDeveloperSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = TaskDeveloper
        exclude = ['task_id']


class TaskSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)

    class Meta:
        model = Task
        sqla_session = db.session
        project = ma.Nested("ProjectSchema")
        assignees = ma.Nested("TaskDeveloperSchema")
        include_relationships = True
        load_instance = True
