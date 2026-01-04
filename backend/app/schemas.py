from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class AssetBase(BaseModel):
    name: str
    type: str
    ip_address: str
    os: Optional[str] = None
    criticality: int = 1
    metadata_info: Optional[Dict[str, Any]] = None

class AssetCreate(AssetBase):
    pass

class Asset(AssetBase):
    id: int
    discovery_date: datetime
    last_scanned: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class VulnerabilityBase(BaseModel):
    cve_id: str
    title: str
    description: str
    severity: float
    status: str = "open"
    remediation_steps: Optional[str] = None

class VulnerabilityCreate(VulnerabilityBase):
    asset_id: int

class Vulnerability(VulnerabilityBase):
    id: int
    detected_at: datetime
    asset_id: int

    model_config = ConfigDict(from_attributes=True)

