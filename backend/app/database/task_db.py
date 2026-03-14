from app.database.base import SessionLocal, TaskDB, TaskAssigneeDB, User


class TaskCRUD:

    @staticmethod
    def get_all(db=None):
        if db is None:
            with SessionLocal() as db:
                return db.query(TaskDB).order_by(TaskDB.created_at.desc()).all()
        return db.query(TaskDB).order_by(TaskDB.created_at.desc()).all()

    @staticmethod
    def get_by_user(user_id: int, db=None):
        if db is None:
            with SessionLocal() as db:
                return db.query(TaskDB).filter(TaskDB.user_id == user_id).order_by(TaskDB.created_at.desc()).all()
        return db.query(TaskDB).filter(TaskDB.user_id == user_id).order_by(TaskDB.created_at.desc()).all()

    @staticmethod
    def _with_assignees(task, db):
        rows = db.query(TaskAssigneeDB).filter(TaskAssigneeDB.task_id == task.id).all()
        task.assignee_ids = [r.user_id for r in rows]
        return task

    @staticmethod
    def create(data, db=None):
        own_db = db is None
        if own_db:
            db = SessionLocal()
        try:
            task = TaskDB(
                title=data.title,
                due_date=data.due_date,
                due_time=data.due_time,
                project_id=data.project_id,
                user_id=data.user_id,
                project_type=data.project_type
            )
            db.add(task)
            db.commit()
            db.refresh(task)
            if hasattr(data, 'assignee_ids') and data.assignee_ids:
                for uid in data.assignee_ids:
                    db.add(TaskAssigneeDB(task_id=task.id, user_id=uid))
                db.commit()
            return TaskCRUD._with_assignees(task, db)
        finally:
            if own_db:
                db.close()

    @staticmethod
    def toggle_complete(task_id: int, db=None):
        own_db = db is None
        if own_db:
            db = SessionLocal()
        try:
            task = db.query(TaskDB).get(task_id)
            if not task:
                return None
            task.is_completed = not task.is_completed
            db.commit()
            db.refresh(task)
            return TaskCRUD._with_assignees(task, db)
        finally:
            if own_db:
                db.close()

    @staticmethod
    def update(task_id: int, data, db=None):
        own_db = db is None
        if own_db:
            db = SessionLocal()
        try:
            task = db.query(TaskDB).get(task_id)
            if not task:
                return None
            if data.title        is not None: task.title        = data.title
            if data.due_date     is not None: task.due_date     = data.due_date
            if data.status       is not None: task.status       = data.status
            if data.description  is not None: task.description  = data.description
            if data.project_id   is not None: task.project_id   = data.project_id
            if data.due_time     is not None: task.due_time     = data.due_time
            if data.project_type is not None: task.project_type = data.project_type

            if hasattr(data, 'assignee_ids') and data.assignee_ids is not None:
                db.query(TaskAssigneeDB).filter(TaskAssigneeDB.task_id == task_id).delete()
                for uid in data.assignee_ids:
                    db.add(TaskAssigneeDB(task_id=task_id, user_id=uid))

            db.commit()
            db.refresh(task)
            return TaskCRUD._with_assignees(task, db)
        finally:
            if own_db:
                db.close()

    @staticmethod
    def delete(task_id: int, db=None):
        own_db = db is None
        if own_db:
            db = SessionLocal()
        try:
            task = db.query(TaskDB).get(task_id)
            if not task:
                return None
            db.query(TaskAssigneeDB).filter(TaskAssigneeDB.task_id == task_id).delete()
            db.delete(task)
            db.commit()
            return True
        finally:
            if own_db:
                db.close()