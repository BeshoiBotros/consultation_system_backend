from celery import shared_task
import ollama
import json
import logging
from core.ai_services import ConsultationSummary
from . import models

logger = logging.getLogger(__name__)

@shared_task
def generate_ai_summary_task(consultation_id: str):
    
    consultation = models.Consultation.objects.filter(pk=consultation_id).first()
    if consultation is None:
        return

    system_prompt = """
    You are a clinical AI assistant. Analyze the doctor's notes.
    Extract the key symptoms, summarize the visit, and suggest a standard treatment plan based on the diagnosis.
    Determine if the situation requires urgent care.
    """
    
    user_prompt = f"Symptoms: {consultation.symptoms}\nDiagnosis: {consultation.diagnosis}"

    try:
        response = ollama.chat(
            model='llama3.2:1b',
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ],
            format=ConsultationSummary.model_json_schema(),
            options={'temperature': 0} 
        )
        content = response['message']['content']
        
        try:
            consultation.ai_summary = json.loads(content)
            
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse JSON for Consultation {consultation_id}. Raw output stored.")
            consultation.ai_summary = {"raw": content}
            
        consultation.save()
        
    except Exception as e:
        logger.error(f"Error generating AI summary for Consultation {consultation_id}: {str(e)}")