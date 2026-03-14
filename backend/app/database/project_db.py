from app.database.base import SessionLocal, ProjectDB, TaskDB, ProjectMemberDB, User


class ProjectCRUD:

    @staticmethod
    def get_all(user_id: int = None, db=None):
        own_db = db is None
        if own_db:
            db = SessionLocal()
        try:
            if user_id is None:
                return db.query(ProjectDB).order_by(ProjectDB.created_at.desc()).all()

            # projects ที่ own + projects ที่เป็น member
            owned = db.query(ProjectDB).filter(
                ProjectDB.user_id == user_id
            ).all()

            member_project_ids = db.query(ProjectMemberDB.project_id).filter(
                ProjectMemberDB.user_id == user_id
            ).all()
            member_project_ids = [r[0] for r in member_project_ids]

            member_projects = db.query(ProjectDB).filter(
                ProjectDB.id.in_(member_project_ids),
                ProjectDB.user_id != user_id
            ).all()

            seen = {p.id for p in owned}
            result = list(owned)
            for p in member_projects:
                if p.id not in seen:
                    result.append(p)

            return sorted(result, key=lambda p: p.created_at, reverse=True)
        finally:
            if own_db:
                db.close()

    @staticmethod
    def create(data, user_id: int = None, db=None):
        own_db = db is None
        if own_db:
            db = SessionLocal()
        try:
            project = ProjectDB(
                name=data.name, emoji=data.emoji, type=data.type,
                color=data.color, description=data.description,
                user_id=user_id
            )
            db.add(project)
            db.commit()
            db.refresh(project)
            return project
        finally:
            if own_db:
                db.close()

    @staticmethod
    def update(project_id: int, data, db=None):
        own_db = db is None
        if own_db:
            db = SessionLocal()
        try:
            project = db.query(ProjectDB).get(project_id)
            if not project:
                return None
            if data.name is not None:
                project.name = data.name
            if data.emoji is not None:
                project.emoji = data.emoji
            if data.type is not None:
                project.type = data.type
            if data.color is not None:
                project.color = data.color
            if data.description is not None:
                project.description = data.description
            db.commit()
            db.refresh(project)
            return project
        finally:
            if own_db:
                db.close()

    @staticmethod
    def delete(project_id: int, db=None):
        own_db = db is None
        if own_db:
            db = SessionLocal()
        try:
            project = db.query(ProjectDB).get(project_id)
            if not project:
                return None
            db.delete(project)
            db.commit()
            return True
        finally:
            if own_db:
                db.close()

    @staticmethod
    def get_tasks(project_id: int, db=None):
        own_db = db is None
        if own_db:
            db = SessionLocal()
        try:
            from app.database.base import TaskAssigneeDB
            project = db.query(ProjectDB).get(project_id)
            if not project:
                return None
            tasks = db.query(TaskDB).filter(
                TaskDB.project_id == project_id
            ).order_by(TaskDB.created_at.desc()).all()
            
            for task in tasks:
                rows = db.query(TaskAssigneeDB).filter(TaskAssigneeDB.task_id == task.id).all()
                task.assignee_ids = [r.user_id for r in rows]
            
            return tasks
        finally:
            if own_db:
                db.close()

    # ── Member CRUD ──

    @staticmethod
    def get_members(project_id: int, db=None):
        own_db = db is None
        if own_db:
            db = SessionLocal()
        try:
            members = db.query(ProjectMemberDB).filter(
                ProjectMemberDB.project_id == project_id
            ).all()
            result = []
            for m in members:
                user = db.query(User).get(m.user_id)
                if user:
                    result.append({
                        "user_id": m.user_id,
                        "role":    m.role,
                        "email":   user.email,
                        "name":    user.name or "",
                        "avatar_url": user.avatar_url or ""
                    })
            return result
        finally:
            if own_db:
                db.close()

    @staticmethod
    def add_member(project_id: int, email: str, role: str = "Member", db=None):
        own_db = db is None
        if own_db:
            db = SessionLocal()
        try:
            # หา user จาก email
            user = db.query(User).filter(User.email == email).first()
            if not user:
                return None, "User not found"

            # เช็คว่าเป็น member แล้วหรือยัง
            existing = db.query(ProjectMemberDB).filter(
                ProjectMemberDB.project_id == project_id,
                ProjectMemberDB.user_id    == user.id
            ).first()
            if existing:
                return None, "User is already a member"

            member = ProjectMemberDB(
                project_id=project_id,
                user_id=user.id,
                role=role
            )
            db.add(member)
            db.commit()
            return {
                "user_id": user.id,
                "role":    role,
                "email":   user.email,
                "name":    user.name or "",
                "avatar_url": user.avatar_url or ""
            }, None
        finally:
            if own_db:
                db.close()

    @staticmethod
    def remove_member(project_id: int, user_id: int, db=None):
        own_db = db is None
        if own_db:
            db = SessionLocal()
        try:
            member = db.query(ProjectMemberDB).filter(
                ProjectMemberDB.project_id == project_id,
                ProjectMemberDB.user_id    == user_id
            ).first()
            if not member:
                return False
            db.delete(member)
            db.commit()
            return True
        finally:
            if own_db:
                db.close()