from app.database.base import SessionLocal, CorporateMemberDB, ProjectDB


class CorporateMemberCRUD:

    @staticmethod
    def get_by_project(project_id: int, db=None):
        own_db = db is None
        if own_db:
            db = SessionLocal()
        try:
            project = db.query(ProjectDB).get(project_id)
            if not project:
                return None
            return db.query(CorporateMemberDB).filter(
                CorporateMemberDB.project_id == project_id
            ).order_by(CorporateMemberDB.added_at.desc()).all()
        finally:
            if own_db:
                db.close()

    @staticmethod
    def add_member(data, db=None):
        own_db = db is None
        if own_db:
            db = SessionLocal()
        try:
            existing = db.query(CorporateMemberDB).filter(
                CorporateMemberDB.project_id == data.project_id,
                CorporateMemberDB.email == data.email
            ).first()
            if existing:
                return None

            member = CorporateMemberDB(
                project_id=data.project_id,
                email=data.email,
                name=data.name,
                role=data.role or "Member"
            )
            db.add(member)
            db.commit()
            db.refresh(member)
            return member
        finally:
            if own_db:
                db.close()

    @staticmethod
    def update_member(member_id: int, data, db=None):
        own_db = db is None
        if own_db:
            db = SessionLocal()
        try:
            member = db.query(CorporateMemberDB).get(member_id)
            if not member:
                return None
            if data.name is not None:
                member.name = data.name
            if data.role is not None:
                member.role = data.role
            if data.email is not None:
                member.email = data.email
            db.commit()
            db.refresh(member)
            return member
        finally:
            if own_db:
                db.close()

    @staticmethod
    def remove_member(member_id: int, db=None):
        own_db = db is None
        if own_db:
            db = SessionLocal()
        try:
            member = db.query(CorporateMemberDB).get(member_id)
            if not member:
                return None
            db.delete(member)
            db.commit()
            return True
        finally:
            if own_db:
                db.close()
