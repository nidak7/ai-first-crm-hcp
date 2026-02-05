from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.interaction import (
    ChatRequest,
    ChatResponse,
    InteractionCreate,
    InteractionOut,
    InteractionUpdate,
)
from app.services.interaction_service import (
    create_interaction,
    get_interaction,
    list_interactions,
    update_interaction,
)
from app.services.langgraph_agent import HCPAgentService

router = APIRouter(prefix="/api")


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/interactions", response_model=InteractionOut)
def create_interaction_endpoint(payload: InteractionCreate, db: Session = Depends(get_db)):
    agent = HCPAgentService(db)
    ai = agent.summarize_interaction(payload.raw_notes, payload.hcp_name)
    return create_interaction(db, payload, ai.summary, ai.sentiment, ai.follow_up_action)


@router.put("/interactions/{interaction_id}", response_model=InteractionOut)
def update_interaction_endpoint(
    interaction_id: int, payload: InteractionUpdate, db: Session = Depends(get_db)
):
    updated = update_interaction(db, interaction_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return updated


@router.get("/interactions", response_model=list[InteractionOut])
def list_interactions_endpoint(db: Session = Depends(get_db)):
    return list_interactions(db)


@router.get("/interactions/{interaction_id}", response_model=InteractionOut)
def get_interaction_endpoint(interaction_id: int, db: Session = Depends(get_db)):
    interaction = get_interaction(db, interaction_id)
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return interaction


@router.post("/agent/chat", response_model=ChatResponse)
def chat_endpoint(payload: ChatRequest, db: Session = Depends(get_db)):
    agent = HCPAgentService(db)
    response = agent.run_chat(payload.message)
    return ChatResponse(response=response)
