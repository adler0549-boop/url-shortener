import sqlite3
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from database import get_db
from repository import get_stats
from schemas import LinkCreate, LinkResponse, LinkStats
from services import click_link, create_short_link, get_link

router = APIRouter()

@router.post("/links", response_model=LinkResponse)
def create_link_endpoint(data: LinkCreate, request: Request, db: sqlite3.Connection = Depends(get_db)) -> LinkResponse:
    original_url = str(data.url)

    code, _ = create_short_link(db=db, original_url=original_url)
    short_url = str(request.base_url).rstrip("/") + f"/{code}"
    return LinkResponse(code=code, short_url=short_url)


@router.get("/links/{code}/stats", response_model=LinkStats)
def link_stats(code: str, db: sqlite3.Connection = Depends(get_db)) -> LinkStats:
    link = get_link(db, code)

    if link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    return get_stats(db, link)


@router.get("/{code}")
def redirect_to_original(code: str, db: sqlite3.Connection = Depends(get_db)) -> RedirectResponse:
    link = click_link(db, code)

    if link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    return RedirectResponse(url=link["original_url"], status_code=302)