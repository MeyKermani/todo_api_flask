from functools import wraps
from flask_jwt_extended import get_jwt_identity
from models import Task, User


def can_edit_task():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            task_id = kwargs.get("task_id")
            task = Task.query.get_or_404(task_id)
            current_user = User.query.filter_by(id=get_jwt_identity()).first()
            if current_user.is_project_manager and task.project.project_manager == current_user:
                return fn(*args, **kwargs)
            elif current_user.is_developer and current_user in task.assignees:
                return fn(*args, **kwargs)
            else:
                return {'message': 'You are not authorized to access this data.'}, 403
        return wrapper
    return decorator
