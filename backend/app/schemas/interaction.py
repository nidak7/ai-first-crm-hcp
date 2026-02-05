from datetime import datetime

from pydantic import BaseModel, Field


class InteractionBase(BaseModel):
    hcp_name: str = Field(min_length=2)
    hcp_specialty: str = "General"
    interaction_type: str
    channel: str = "In-person"
    raw_notes: str = Field(min_length=5)
    created_by: str = "field-rep"


class InteractionCreate(InteractionBase):
    pass


class InteractionUpdate(BaseModel):
    hcp_name: str | None = None
    hcp_specialty: str | None = None
    interaction_type: str | None = None
    channel: str | None = None
    raw_notes: str | None = None
    summary: str | None = None
    sentiment: str | None = None
    follow_up_action: str | None = None


class InteractionOut(InteractionBase):
    id: int
    summary: str
    sentiment: str
    follow_up_action: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
