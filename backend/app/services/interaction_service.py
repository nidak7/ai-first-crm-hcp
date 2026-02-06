from sqlalchemy.orm import Session

from app.models.interaction import Interaction
from app.schema.interaction import InteractionCreate, InteractionUpdate


def create_interaction(
    db: Session,
    payload: InteractionCreate,
    summary: str,
    sentiment: str,
    follow_up_action: str,
) -> Interaction:
    interaction = Interaction(
        **payload.model_dump(),
        summary=summary,
        sentiment=sentiment,
        follow_up_action=follow_up_action,
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)
    return interaction


def update_interaction(db: Session, interaction_id: int, payload: InteractionUpdate) -> Interaction | None:
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        return None

    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(interaction, key, value)

    db.commit()
    db.refresh(interaction)
    return interaction


def get_interaction(db: Session, interaction_id: int) -> Interaction | None:
    return db.query(Interaction).filter(Interaction.id == interaction_id).first()


def list_interactions(db: Session) -> list[Interaction]:
    return db.query(Interaction).order_by(Interaction.created_at.desc()).all()
