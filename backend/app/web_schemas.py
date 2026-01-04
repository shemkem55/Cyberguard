from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class WebTargetBase(BaseModel):
    domain: str
    root_url: str
    scope_description: str

class WebTargetCreate(WebTargetBase):
    pass

class WebTarget(WebTargetBase):
    id: int
    authorized: bool
    tech_stack: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class PentestSessionBase(BaseModel):
    target_id: int
    status: str

class PentestSession(PentestSessionBase):
    id: int
    start_time: datetime
    end_time: Optional[datetime] = None
    findings_summary: Optional[Dict[str, Any]] = None
    
    model_config = ConfigDict(from_attributes=True)

class WebFindingBase(BaseModel):
    title: str
    url: str
    severity: str
    description: str
    evidence: Optional[str] = None
    remediation_advice: Optional[str] = None

class WebFinding(WebFindingBase):
    id: int
    session_id: int
    confirmed_by_validation: bool
    
    model_config = ConfigDict(from_attributes=True)
