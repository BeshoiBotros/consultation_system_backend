import ollama
from pydantic import BaseModel
import json

class ConsultationSummary(BaseModel):
    brief_summary: str
    key_symptoms: list[str]
    suggested_treatment_plan: str
    requires_urgent_care: bool

def generate_arabic_summary(symptoms: str, diagnosis: str) -> str:
    
    system_prompt = """
    You are a clinical AI assistant. Analyze the doctor's notes.
    Extract the key symptoms, summarize the visit, and suggest a standard treatment plan based on the diagnosis.
    Determine if the situation requires urgent care.
    """
    
    user_prompt = f"Symptoms: {symptoms}\nDiagnosis: {diagnosis}"

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
        return response['message']['content']
    except Exception as e:
        return json.dumps({"error": str(e)})

# Test with Arabic inputs
symptoms_ar = "الم مبرح في اسفل البطن من الجهة اليمنى، غثيان وقيء مستمر منذ ٤ ساعات."
diagnosis_ar = "اشتباه بالتهاب الزائدة الدودية الحاد."

result = generate_arabic_summary(symptoms_ar, diagnosis_ar)
print(json.dumps(json.loads(result), indent=2, ensure_ascii=False))