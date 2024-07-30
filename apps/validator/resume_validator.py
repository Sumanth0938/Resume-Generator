from pydantic import BaseModel
from typing import Dict, Any

class ResumeModel(BaseModel):
    resume_data: Dict[str, Any]
