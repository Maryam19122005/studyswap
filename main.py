from starlette.middleware.sessions import SessionMiddleware
from auth import hash_password, verify_password
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import SessionLocal, engine
from models import Base, StudySpot, User

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key="study_swap_secret_2024")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

LOCATIONS = [
    "Library Floor 1",
    "Library Floor 2",
    "Study Room 1 (next to reception desk)",
    "Study Room 2 (next to water dispenser)",
    "Any group study table"
]

KARMA_RULES = {
    "share": 10,
    "claim": 2,
}

def get_karma_status(points: int) -> dict:
    if points < 50:
        return {"title": "Rookie Sharer", "icon": "🌱", "next": 50, "color": "#6ee7b7"}
    elif points < 200:
        return {"title": "Helpful Hunter", "icon": "🔍", "next": 200, "color": "#60a5fa"}
    else:
        return {"title": "Spot Master", "icon": "⭐", "next": None, "color": "#fbbf24"}


# HOME
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    username = request.session.get("user")
    if not username:
        return RedirectResponse("/login", status_code=303)

    db = SessionLocal()
    spots = db.query(StudySpot).filter(StudySpot.is_claimed == False).all()
    user = db.query(User).filter(User.username == username).first()
    karma = user.karma_points if user else 0
    status = get_karma_status(karma)
    db.close()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "spots": spots,
            "username": username,
            "karma": karma,
            "status": status,
            "locations": LOCATIONS,
            "karma_rules": KARMA_RULES,
        }
    )


# LOGIN PAGE
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    username = request.session.get("user")
    if username:
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse(request=request, name="login.html", context={"error": None})


# LOGIN LOGIC
@app.post("/login", response_class=HTMLResponse)
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    db.close()

    if not user:
        return templates.TemplateResponse(request=request, name="login.html", context={"error": "User not found. Please sign up first."})

    if not verify_password(password, user.password):
        return templates.TemplateResponse(request=request, name="login.html", context={"error": "Wrong password. Try again."})

    request.session["user"] = username
    return RedirectResponse("/", status_code=303)


# SIGNUP PAGE
@app.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    username = request.session.get("user")
    if username:
        return RedirectResponse("/", status_code=303)
    return templates.TemplateResponse(request=request, name="signup.html", context={"error": None})


# SIGNUP LOGIC
@app.post("/signup", response_class=HTMLResponse)
def signup(request: Request, username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    existing = db.query(User).filter(User.username == username).first()

    if existing:
        db.close()
        return templates.TemplateResponse(request=request, name="signup.html", context={"error": "Username already taken. Try another."})

    new_user = User(username=username, password=hash_password(password), karma_points=0)
    db.add(new_user)
    db.commit()
    db.close()

    return RedirectResponse("/login", status_code=303)


# LOGOUT
@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login", status_code=303)


# SHARE SPOT
@app.post("/share")
def share_spot(
    request: Request,
    location: str = Form(...),
    time_left: int = Form(...),
    has_power: bool = Form(False),
    noise_level: str = Form(...)
):
    username = request.session.get("user")
    if not username:
        return RedirectResponse("/login", status_code=303)

    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    user.karma_points += KARMA_RULES["share"]

    new_spot = StudySpot(
        location=location,
        time_left=time_left,
        has_power=has_power,
        noise_level=noise_level,
        shared_by=username,
        is_claimed=False
    )
    db.add(new_spot)
    db.commit()
    db.close()

    return RedirectResponse("/?tab=spots", status_code=303)


# CLAIM SPOT
@app.post("/claim/{spot_id}")
def claim_spot(request: Request, spot_id: int):
    username = request.session.get("user")
    if not username:
        return RedirectResponse("/login", status_code=303)

    db = SessionLocal()
    spot = db.query(StudySpot).filter(StudySpot.id == spot_id).first()
    user = db.query(User).filter(User.username == username).first()

    if spot and not spot.is_claimed:
        spot.is_claimed = True
        user.karma_points += KARMA_RULES["claim"]
        db.commit()

    db.close()
    return RedirectResponse("/?tab=spots", status_code=303)


# KARMA PAGE
@app.get("/karma", response_class=HTMLResponse)
def karma_page(request: Request):
    username = request.session.get("user")
    if not username:
        return RedirectResponse("/login", status_code=303)

    db = SessionLocal()
    user = db.query(User).filter(User.username == username).first()
    karma = user.karma_points if user else 0
    status = get_karma_status(karma)

    shared_count = db.query(StudySpot).filter(StudySpot.shared_by == username).count()
    db.close()

    progress = min((karma / (status["next"] or karma or 1)) * 100, 100) if status["next"] else 100

    return templates.TemplateResponse(
        request=request,
        name="karma.html",
        context={
            "username": username,
            "karma": karma,
            "status": status,
            "shared_count": shared_count,
            "claimed_count": karma // KARMA_RULES["claim"] if karma else 0,
            "progress": progress,
            "karma_rules": KARMA_RULES,
        }
    )
