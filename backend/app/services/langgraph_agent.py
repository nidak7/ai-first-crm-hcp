from __future__ import annotations

from dataclasses import dataclass

from langchain_core.tools import tool
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.interaction import Interaction
from app.schemas.interaction import InteractionUpdate
from app.services.interaction_service import (
    get_interaction,
    list_interactions,
    update_interaction,
)


@dataclass
class AIResult:
    summary: str
    sentiment: str
    follow_up_action: str


class HCPAgentService:
    """
    LangGraph-backed service containing five sales tools:
    1) log_interaction
    2) edit_interaction
    3) suggest_next_best_action
    4) generate_followup_email
    5) compliance_check
    """

    def __init__(self, db: Session):
        self.db = db

    def summarize_interaction(self, notes: str, hcp_name: str) -> AIResult:
        if not settings.groq_api_key:
            return AIResult(
                summary=f"Discussed with {hcp_name}: {notes[:160]}",
                sentiment="neutral",
                follow_up_action="Schedule 2-week follow-up and share clinical evidence PDF.",
            )

        from langchain_groq import ChatGroq

        model = ChatGroq(model=settings.groq_model, api_key=settings.groq_api_key, temperature=0.1)
        prompt = (
            "You are a life-sciences CRM copilot."
            "Return strict JSON with keys: summary, sentiment, follow_up_action."
            f"\nHCP: {hcp_name}\nNotes: {notes}"
        )
        raw = model.invoke(prompt).content
        # Lightweight parsing fallback when model returns non-JSON text
        return AIResult(
            summary=raw[:300],
            sentiment="neutral" if "negative" not in raw.lower() else "negative",
            follow_up_action="Send tailored follow-up and update account plan.",
        )

    def _build_tools(self):
        @tool
        def log_interaction_tool(hcp_name: str, notes: str) -> str:
            """Capture and summarize a newly discussed interaction from chat mode."""
            result = self.summarize_interaction(notes, hcp_name)
            interaction = Interaction(
                hcp_name=hcp_name,
                hcp_specialty="General",
                interaction_type="chat_logged",
                channel="Chat",
                raw_notes=notes,
                summary=result.summary,
                sentiment=result.sentiment,
                follow_up_action=result.follow_up_action,
                created_by="agent-chat",
            )
            self.db.add(interaction)
            self.db.commit()
            self.db.refresh(interaction)
            return f"Logged interaction #{interaction.id} for {hcp_name}."

        @tool
        def edit_interaction_tool(interaction_id: int, updated_notes: str) -> str:
            """Modify an existing logged interaction and refresh summary fields."""
            interaction = get_interaction(self.db, interaction_id)
            if not interaction:
                return f"Interaction {interaction_id} not found."
            result = self.summarize_interaction(updated_notes, interaction.hcp_name)
            payload = InteractionUpdate(
                raw_notes=updated_notes,
                summary=result.summary,
                sentiment=result.sentiment,
                follow_up_action=result.follow_up_action,
            )
            update_interaction(self.db, interaction_id, payload)
            return f"Interaction {interaction_id} updated successfully."

        @tool
        def suggest_next_best_action_tool(hcp_name: str) -> str:
            """Suggest a sales next-best-action based on recent HCP interaction history."""
            interactions = [x for x in list_interactions(self.db) if x.hcp_name.lower() == hcp_name.lower()][:3]
            if not interactions:
                return "No history found. Start with introductory clinical value discussion."
            return f"Based on {len(interactions)} interactions, prepare efficacy deck + formulary objection handling for {hcp_name}."

        @tool
        def generate_followup_email_tool(hcp_name: str, key_message: str) -> str:
            """Generate a compliant follow-up email for an HCP after a field interaction."""
            return (
                f"Subject: Follow-up from our discussion\n\nDear Dr. {hcp_name},\n"
                f"Thank you for your time. As discussed: {key_message}.\n"
                "I am sharing approved prescribing and safety material for your review."
            )

        @tool
        def compliance_check_tool(notes: str) -> str:
            """Check notes for potential compliance risk language (off-label, promises, inducements)."""
            risk_terms = ["off-label", "guaranteed", "gift", "cash"]
            found = [term for term in risk_terms if term in notes.lower()]
            return "Compliance Risk: " + (", ".join(found) if found else "None detected")

        return [
            log_interaction_tool,
            edit_interaction_tool,
            suggest_next_best_action_tool,
            generate_followup_email_tool,
            compliance_check_tool,
        ]

    def run_chat(self, message: str) -> str:
        if not settings.groq_api_key:
            return (
                "Groq API key not configured. Running fallback mode. "
                "Try commands like: 'log interaction for Dr Lee: discussed dosing updates'."
            )

        from langchain_groq import ChatGroq
        from langgraph.prebuilt import create_react_agent

        model = ChatGroq(model=settings.groq_model, api_key=settings.groq_api_key, temperature=0)
        graph = create_react_agent(model=model, tools=self._build_tools())

        result = graph.invoke(
            {
                "messages": [
                    (
                        "system",
                        "You are an HCP CRM assistant for pharma field reps. Use tools when useful.",
                    ),
                    ("user", message),
                ]
            }
        )
        messages = result.get("messages", [])
        if not messages:
            return "No response generated."
        return messages[-1].content
