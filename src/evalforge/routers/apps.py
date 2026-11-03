from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..db.models import App, TestCase
from ..schemas import AppCreate, AppOut, TestCaseCreate, TestCaseOut

router = APIRouter(prefix="/apps", tags=["apps"])


@router.post("", response_model=AppOut, status_code=201)
def create_app(payload: AppCreate, db: Session = Depends(get_db)):
    existing = db.scalar(select(App).where(App.name == payload.name))
    if existing:
        raise HTTPException(status_code=409, detail="App name already exists")
    app = App(name=payload.name, description=payload.description)
    db.add(app)
    db.commit()
    db.refresh(app)
    return app


@router.get("", response_model=list[AppOut])
def list_apps(db: Session = Depends(get_db)):
    return db.scalars(select(App)).all()


@router.post("/{app_id}/test-cases", response_model=TestCaseOut, status_code=201)
def create_test_case(app_id: int, payload: TestCaseCreate, db: Session = Depends(get_db)):
    if not db.get(App, app_id):
        raise HTTPException(status_code=404, detail="App not found")
    case = TestCase(app_id=app_id, **payload.model_dump())
    db.add(case)
    db.commit()
    db.refresh(case)
    return case


@router.get("/{app_id}/test-cases", response_model=list[TestCaseOut])
def list_test_cases(app_id: int, db: Session = Depends(get_db)):
    if not db.get(App, app_id):
        raise HTTPException(status_code=404, detail="App not found")
    return db.scalars(select(TestCase).where(TestCase.app_id == app_id)).all()