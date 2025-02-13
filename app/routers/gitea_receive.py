import json
from fastapi import APIRouter, Depends, Request
from fastapi.responses import PlainTextResponse
from app.dependencies import get_handler

router = APIRouter()

@router.post("/receive", tags=["test"])
async def read_users(request: Request, handler=(Depends(get_handler))):
    event = request.headers.get('X-Gitea-Event-Type')
    body = await request.body()
    body_str = body.decode('utf-8')
    requestParam = json.loads(body_str)
    handler.handle(event, requestParam)
    return PlainTextResponse(content='Ok')