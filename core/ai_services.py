from pydantic import BaseModel

class ConsultationSummary(BaseModel):
    brief_summary: str
    key_symptoms: list[str]
    suggested_treatment_plan: str
    requires_urgent_care: bool

