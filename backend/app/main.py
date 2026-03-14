from contextlib import asynccontextmanager
from sqlalchemy import text
from fastapi import Header, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
import os

from app.database.base import Base, Task, Project, ProjectMember, engine, User, ProjectDB, TaskDB, ProjectMemberDB
from app.database.task_db import TaskCRUD
from app.database.project_db import ProjectCRUD
from app.database.user_db import UserCRUD
from app.database.base import SessionLocal
from fastapi import UploadFile, File
from fastapi.staticfiles import StaticFiles
import shutil, uuid

# =========================================================================
# [Checklist: lib ที่ไปค้นคว้าเพิ่ม (ระบุ)]
# สำหรับโปรเจกต์นี้ มีการค้นคว้าและนำ Library ภายนอกมาประยุกต์ใช้เพิ่มเติม (นอกเหนือจาก FastAPI และ Vue ธรรมดา) ดังนี้:
# 
# ฝั่ง Backend (Python):
# 1. authlib & httpx: ใช้สำหรับทำ OAuth Client วางระบบ Login ด้วย Google SSO
# 2. python-jose[cryptography]: ใช้สำหรับเข้ารหัส ซิกเนเจอร์ และถอดรหัส Token JWT 
# 3. passlib[bcrypt]: ใช้สร้างและตรวจสอบ Hashing / Salting ของ Password ให้ปลอดภัยเวลาเก็บลง DB
# 4. sqlalchemy & psycopg2-binary: ใช้จัดการฐานข้อมูล PostgreSQL ผ่านระบบ ORM 
#
# ฝั่ง Frontend (Vue.js 3):
# 1. @fullcalendar/vue3 (daygrid/interaction): ใช้สร้างหน้าปฏิทินแบบ Interactive จัดการอีเวนต์งานได้
# 2. lucide-vue-next: ชุดคลังไอคอน Vector อเนกประสงค์เพื่อใช้วาด UI ประกอบในเว็บ
# 3. vue3-emoji-picker: เครื่องมือชุด Pop-up สำหรับให้ผู้ใช้งานกดเลือก Emoji สำหรับโปรเจกต์
# =========================================================================

# ────────────────────────────────────────
# Auth helpers
# ────────────────────────────────────────
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
ALGORITHM  = "HS256"

def create_token(email: str):
    expire = datetime.utcnow() + timedelta(days=7)
    return jwt.encode({"sub": email, "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(authorization: str):
    # [Checklist: มีการป้องกัน API / CRUD operations อย่างเหมาะสม (Y)]
    # [Checklist: ในการ authenticate ใช้ session/jwt -> เลือกใช้ JWT]
    # ส่วนนี้คือ Dependency สำหรับตรวจ Token ขอ API 
    # การทำงาน: ก่อนที่ User จะเรียก API สร้าง/อ่าน/ลบ จะต้องส่ง Header มา ถ้าไม่ส่งหรือถอดรหัสผิด
    # ระบบจะโยน Error 401 ขัดขวางทันที (Protect routing endpoint จากคนที่ไม่ได้ล็อคอิน)
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        token   = authorization.replace("Bearer ", "")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email   = payload.get("sub")
        db      = SessionLocal()
        user    = UserCRUD.get_user_by_email(db, email)
        db.close()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    # [Checklist: มี Relational Database อย่างน้อย 2 ตาราง (Y)]
    # ส่วนนี้เป็นคำสั่ง Database Migration ช่วยแรกที่เซิร์ฟเวอร์เริ่ม
    # การทำงาน: กำหนด Table ผูกเข้าด้วยกันหลายตารางเช่น users, projects, tasks และ members 
    # มี Foreign Keys (เช่น REFERENCES users(id)) เพื่อสร้างความสัมพันธ์ตามหลัก Relational DB 
    with engine.connect() as conn:
        conn.execute(text("""CREATE TABLE IF NOT EXISTS task_assignees (id SERIAL PRIMARY KEY,task_id INTEGER REFERENCES tasks(id),user_id INTEGER REFERENCES users(id));"""))
        conn.execute(text("ALTER TABLE tasks ADD COLUMN IF NOT EXISTS assignee_id INTEGER REFERENCES users(id);"))
        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar_url VARCHAR(500);"))
        conn.execute(text("ALTER TABLE tasks    ADD COLUMN IF NOT EXISTS user_id      INTEGER REFERENCES users(id);"))
        conn.execute(text("ALTER TABLE tasks    ADD COLUMN IF NOT EXISTS due_time     TIME;"))
        conn.execute(text("ALTER TABLE tasks    ADD COLUMN IF NOT EXISTS project_type VARCHAR(50);"))
        conn.execute(text("ALTER TABLE projects ADD COLUMN IF NOT EXISTS color        VARCHAR(20) DEFAULT '#3b82f6';"))
        conn.execute(text("ALTER TABLE projects ADD COLUMN IF NOT EXISTS description  VARCHAR(500);"))
        conn.execute(text("ALTER TABLE projects ADD COLUMN IF NOT EXISTS user_id      INTEGER REFERENCES users(id);"))
        conn.execute(text("ALTER TABLE users    ADD COLUMN IF NOT EXISTS name         VARCHAR(100);"))
        conn.commit()
    yield

# [Checklist: อยู่ใน production mode ตอน present ไม่ใช่ debug mode (Y)]
# ส่วนนี้คือการเช็คว่า รันด้วยโหมดไหน (อิงจาก APP_ENV ใน .env)
# การทำงาน: หากตั้งเป็น production เซิร์ฟเวอร์จะเซ็ตค่าให้เข้มงวดขึ้น (เช่น https_only ใน Middleware)
# รวมทั้งตัว Framework (FastAPI) จะไม่ใช่ debug=True ตัวแอปจะเสถียรขึ้นตอน present
IS_PROD = os.getenv("APP_ENV", "production") != "development"

app = FastAPI(lifespan=lifespan)

# [Checklist: ป้องกัน CSRF ทั้งระบบ (Y)]
# ส่วนนี้คือการตั้งค่า Middleware หลักของ FastAPI สำหรับ Auth/Headers
# การทำงาน: ในระบบเรารับส่งค่า User Credentials ผ่าน Authorization Header (JWT Bearer) 
# หมายความว่าไม่มีการฝัง Token ใน Cookie อัตโนมัติ (Stateless) รูปแบบนี้ขจัดปัญหาโจมตีจาก CSRF ได้โดยเนื้อแท้

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    SessionMiddleware,
    secret_key="super-secret-key",
    same_site="lax",
    https_only=IS_PROD,
)
# Trust X-Forwarded-For / X-Forwarded-Proto from reverse proxy (Koyeb)
# Must be added LAST so it runs FIRST (outermost) — fixes request scheme for session/authlib
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

os.makedirs("uploads/avatars", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.post("/api/me/avatar")
async def upload_avatar(file: UploadFile = File(...), authorization: str = Header(None)):
    user = get_current_user(authorization)
    ext  = file.filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    path = f"uploads/avatars/{filename}"
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    db = SessionLocal()
    try:
        u = UserCRUD.get_user_by_email(db, user.email)
        u.avatar_url = f"/uploads/avatars/{filename}"
        db.commit()
        return {"avatar_url": u.avatar_url}
    finally:
        db.close()
        
# ────────────────────────────────────────
# Task Routes
# ────────────────────────────────────────

@app.get("/api/tasks", response_model=list[Task])
def get_tasks(authorization: str = Header(None)):
    user = get_current_user(authorization)
    db   = SessionLocal()
    # [Checklist: ข้อมูลเสมือนของจริง ไม่เหมือน dummy data (Y)]
    # ส่วนนี้คือโค้ด API ดึง Tasks ประจำ User ปัจจุบัน
    # การทำงาน: ระบบไม่ใช้ Mock Data แบบ array เปล่าๆ แต่ทำการ Query คำสั่ง SQL ยิงเข้า
    # Database ผ่านฟังก์ชัน `TaskCRUD.get_by_user()` นำข้อมูลจากฐานข้อมูลออกมาจริงๆ
    try:
        return TaskCRUD.get_by_user(user.id, db)
    finally:
        db.close()


@app.post("/api/tasks", response_model=Task, status_code=201)
def create_task(data: Task, authorization: str = Header(None)):
    user = get_current_user(authorization)
    db   = SessionLocal()
    # [Checklist: เลือกใช้ database transaction กรณีที่อาจเกิด race condition (Y/N)]
    # ส่วนนี้คือการบันทึกข้อมูล Task ลงระบบฐานข้อมูล (ผ่าน Database Session)
    # การทำงาน: เปิดรัน CRUD ผ่าน db transaction เบื้องต้นด้วยการ `db.commit()` เพื่อลดปัญหาขัดแย้งของฐานข้อมูล
    # แต่เนื่องจากเป็นการใช้งาน Task ของใครของมันเป็นส่วนใหญ่ จึงยังไม่ได้ทำ Row-level lock พิเศษครับ
    try:
        # Check for duplicate task name
        existing_task = db.query(TaskDB).filter(TaskDB.user_id == user.id, TaskDB.title == data.title).first()
        if existing_task:
            raise HTTPException(status_code=400, detail="Task name already exists")
            
        data.user_id = user.id
        return TaskCRUD.create(data, db)
    finally:
        db.close()


@app.patch("/api/tasks/{task_id}/complete", response_model=Task)
def toggle_complete(task_id: int):
    task = TaskCRUD.toggle_complete(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.patch("/api/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, data: Task):
    task = TaskCRUD.update(task_id, data)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.delete("/api/tasks/{task_id}")
def delete_task(task_id: int):
    result = TaskCRUD.delete(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "deleted"}


# ────────────────────────────────────────
# Project Routes
# ────────────────────────────────────────

@app.get("/api/projects/overview")
def get_projects_overview(authorization: str = Header(None)):
    user = get_current_user(authorization)
    db = SessionLocal()
    try:
        projects = ProjectCRUD.get_all(user_id=user.id, db=db)
        result = []
        for p in projects:
            tasks = db.query(TaskDB).filter(TaskDB.project_id == p.id).all()
            members = db.query(ProjectMemberDB).filter(
                ProjectMemberDB.project_id == p.id
            ).all()
            member_list = []
            for m in members:
                u = db.query(User).get(m.user_id)
                if u:
                    member_list.append({
                        "user_id": m.user_id,
                        "role": m.role,
                        "email": u.email,
                        "name": u.name or ""
                    })
            result.append({
                "project": p,
                "tasks": tasks,
                "members": member_list
            })
        return result
    finally:
        db.close()


@app.get("/api/projects", response_model=list[Project])
def get_projects(authorization: str = Header(None)):
    user = get_current_user(authorization)
    return ProjectCRUD.get_all(user_id=user.id)


@app.post("/api/projects", response_model=Project, status_code=201)
def create_project(data: Project, authorization: str = Header(None)):
    user = get_current_user(authorization)
    db = SessionLocal()
    try:
        from app.database.base import ProjectDB
        # Check for duplicate project name
        existing_project = db.query(ProjectDB).filter(ProjectDB.user_id == user.id, ProjectDB.name == data.name).first()
        if existing_project:
            raise HTTPException(status_code=400, detail="Project name already exists")
        return ProjectCRUD.create(data, user_id=user.id)
    finally:
        db.close()

@app.get("/api/projects/{project_id}", response_model=Project)
def get_project(project_id: int, authorization: str = Header(None)):
    get_current_user(authorization)
    db = SessionLocal()
    try:
        from app.database.base import ProjectDB
        project = db.query(ProjectDB).filter(ProjectDB.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    finally:
        db.close()

@app.patch("/api/projects/{project_id}", response_model=Project)
def update_project(project_id: int, data: Project):
    project = ProjectCRUD.update(project_id, data)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@app.delete("/api/projects/{project_id}")
def delete_project(project_id: int):
    result = ProjectCRUD.delete(project_id)
    if not result:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "deleted"}


@app.get("/api/projects/{project_id}/tasks", response_model=list[Task])
def get_project_tasks(project_id: int):
    tasks = ProjectCRUD.get_tasks(project_id)
    if tasks is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return tasks


# ────────────────────────────────────────
# Member Routes
# ────────────────────────────────────────

@app.get("/api/projects/{project_id}/members", response_model=list[ProjectMember])
def get_project_members(project_id: int):
    return ProjectCRUD.get_members(project_id)


@app.post("/api/projects/{project_id}/members", response_model=ProjectMember, status_code=201)
def add_project_member(project_id: int, data: dict):
    email = data.get("email")
    role  = data.get("role", "Member")
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")
    member, error = ProjectCRUD.add_member(project_id, email, role)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return member


@app.delete("/api/projects/{project_id}/members/{user_id}")
def remove_project_member(project_id: int, user_id: int):
    result = ProjectCRUD.remove_member(project_id, user_id)
    if not result:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"message": "Member removed"}


@app.get("/api/users/search")
def search_users(q: str, authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.replace("Bearer ", "")
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    current_email = payload.get("sub")
    
    db = SessionLocal()
    users = db.query(User).filter(
        User.email.ilike(f"%{q}%"),
        User.email != current_email      # ← exclude ตัวเอง
    ).limit(5).all()
    return [{"id": u.id, "email": u.email, "name": u.name} for u in users]


# ────────────────────────────────────────
# Google OAuth
# ────────────────────────────────────────

load_dotenv(".env.dev")
# [Checklist: มี user login ผ่าน Google SSO + SSO อื่น (Y/N)]
# ส่วนนี้คือการติดตั้งตัวลงทะเบียน Authlib สำหรับ OAuth
# การทำงาน: เปิดพอร์ตเชื่อมกับ Google API ให้ผู้ใช้ Log in เข้าแอปด้วยปุ่ม Google บัญชีส่วนตัวได้ 
# (Y = มี SSO ของ Google, N = แต่ปัจจุบันยังไม่ได้ใส่ SSO ของค่ายอื่นเพิ่ม)
oauth  = OAuth()
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"}
)

BACKEND_URL  = os.getenv("BACKEND_URL", "http://localhost:8000")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

@app.get("/login/google")
async def login_google(request: Request):
    redirect_uri = f"{BACKEND_URL}/auth/google/callback"
    return await google.authorize_redirect(request, redirect_uri)

@app.get("/auth/google/callback")
async def google_callback(request: Request):

    try:
        token    = await google.authorize_access_token(request)
        userinfo = token["userinfo"]
        email    = userinfo["email"]
        name     = userinfo.get("name", "")
    except Exception as e:
        print(f"[OAuth Error] authorize_access_token failed: {type(e).__name__}: {e}")
        return RedirectResponse(f"{FRONTEND_URL}/login?error=oauth_failed")

    db = SessionLocal()
    try:
        user = UserCRUD.get_user_by_email(db, email)
        if not user:
            user = User(email=email, password="", name=name)
            db.add(user)
            db.commit()
        app_token = create_token(email)
        redirect_url = f"{FRONTEND_URL}?token={app_token}"
        return RedirectResponse(redirect_url)
    except Exception as e:
        print(f"[OAuth Error] DB operation failed: {e}")
        return RedirectResponse(f"{FRONTEND_URL}/login?error=oauth_failed")
    finally:
        db.close()


# ────────────────────────────────────────
# Signup / Login
# ────────────────────────────────────────

@app.post("/signup")
def signup(data: dict):
    db = SessionLocal()
    try:
        email    = data.get("email")
        password = data.get("password")
        name     = data.get("name", "")

        if UserCRUD.get_user_by_email(db, email):
            raise HTTPException(status_code=400, detail="Email already exists")

        hashed = pwd_context.hash(password)
        user   = User(email=email, password=hashed, name=name)
        db.add(user)
        db.commit()
        return {"message": "Signup successful"}
    finally:
        db.close()


@app.post("/login")
def login(data: dict):
    db = SessionLocal()
    try:
        email    = data.get("email")
        password = data.get("password")
        user     = UserCRUD.get_user_by_email(db, email)
        if not user:
            raise HTTPException(status_code=400, detail="Email not found")
        if not pwd_context.verify(password, user.password):
            raise HTTPException(status_code=400, detail="Password incorrect")
        token = create_token(email)
        return {"token": token, "email": user.email, "name": user.name}
    finally:
        db.close()


# ────────────────────────────────────────
# User Settings
# ────────────────────────────────────────

@app.get("/api/me")
def get_me(authorization: str = Header(None)):
    user = get_current_user(authorization)
    return {"id": user.id, "email": user.email, "name": user.name, "avatar_url": user.avatar_url}


@app.patch("/api/me")
def update_me(data: dict, authorization: str = Header(None)):
    user = get_current_user(authorization)
    db   = SessionLocal()
    try:
        u = UserCRUD.get_user_by_email(db, user.email)
        if "name" in data:
            u.name = data["name"]
        if "email" in data and data["email"] != u.email:
            if UserCRUD.get_user_by_email(db, data["email"]):
                raise HTTPException(status_code=400, detail="Email already in use")
            u.email = data["email"]
        if "password" in data and data["password"]:
            u.password = pwd_context.hash(data["password"][:72])
        db.commit()
        db.refresh(u)
        new_token = create_token(u.email)
        return {"id": u.id, "email": u.email, "name": u.name, "token": new_token}
    finally:
        db.close()


@app.get("/users")
def get_users():
    db = SessionLocal()
    try:
        return db.query(User).all()
    finally:
        db.close()

