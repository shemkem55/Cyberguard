from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey, Text, Float, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)  # workstation, server, network_device, etc.
    ip_address = Column(String, index=True)
    os_version = Column(String)
    os_kernel = Column(String)
    patch_level = Column(String)
    compliance_status = Column(String) # Compliant, Non-Compliant
    criticality = Column(Integer, default=1)  # 1-10
    discovery_date = Column(DateTime, default=datetime.datetime.utcnow)
    last_scanned = Column(DateTime)
    metadata_info = Column(JSON)  # Store additional dynamic data

    vulnerabilities = relationship("Vulnerability", back_populates="asset")
    scan_history = relationship("ScanResult", back_populates="asset")
    
class ScanResult(Base):
    __tablename__ = "scan_results"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    scan_type = Column(String) # os_scan, network_scan
    status = Column(String) # success, failure
    summary = Column(Text)
    raw_data = Column(JSON) # Can store findings for structured access
    performed_at = Column(DateTime, default=datetime.datetime.utcnow)

    asset = relationship("Asset", back_populates="scan_history")

class Vulnerability(Base):
    __tablename__ = "vulnerabilities"

    id = Column(Integer, primary_key=True, index=True)
    cve_id = Column(String, index=True)
    title = Column(String)
    description = Column(Text)
    severity = Column(Float)  # CVSS score
    status = Column(String, default="open")  # open, closed, risk_accepted, remediated
    asset_id = Column(Integer, ForeignKey("assets.id"))
    detected_at = Column(DateTime, default=datetime.datetime.utcnow)
    remediation_steps = Column(Text)
    resolved_at = Column(DateTime, nullable=True) # When it was remediated
    resolution_notes = Column(Text, nullable=True) # How it was remediated

    asset = relationship("Asset", back_populates="vulnerabilities")

class ThreatIntel(Base):
    __tablename__ = "threat_intel"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String)
    title = Column(String)
    content = Column(Text)
    threat_actor = Column(String)
    published_date = Column(DateTime)
    ingested_at = Column(DateTime, default=datetime.datetime.utcnow)
    confidence_score = Column(Float)

class NetworkService(Base):
    __tablename__ = "network_services"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    port = Column(Integer)
    protocol = Column(String)  # tcp, udp
    service_name = Column(String)  # http, ssh, mysql, etc.
    service_version = Column(String)
    state = Column(String)  # open, closed, filtered
    banner = Column(Text)  # Service banner for fingerprinting
    discovered_at = Column(DateTime, default=datetime.datetime.utcnow)
    risk_level = Column(String)  # low, medium, high, critical

    asset = relationship("Asset", back_populates="network_services")

class AttackPath(Base):
    __tablename__ = "attack_paths"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    entry_point_asset_id = Column(Integer, ForeignKey("assets.id"))
    target_asset_id = Column(Integer, ForeignKey("assets.id"))
    path_steps = Column(JSON)  # List of exploitation steps
    exploited_vulnerabilities = Column(JSON)  # CVE IDs used in path
    likelihood_score = Column(Float)  # 0-10 probability
    impact_score = Column(Float)  # 0-10 damage potential
    risk_score = Column(Float)  # likelihood * impact
    mitigation_priority = Column(Integer)  # 1-5, 1 being highest
    discovered_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String, default="active")  # active, mitigated, risk_accepted

    entry_point = relationship("Asset", foreign_keys=[entry_point_asset_id])
    target = relationship("Asset", foreign_keys=[target_asset_id])

class ApprovalRequest(Base):
    __tablename__ = "approval_requests"

    id = Column(Integer, primary_key=True, index=True)
    request_type = Column(String)  # scan, remediation, config_change, risk_acceptance, web_pentest_auth
    action = Column(String)  # Specific action being requested
    target_asset_id = Column(Integer, ForeignKey("assets.id"), nullable=True)
    target_vulnerability_id = Column(Integer, ForeignKey("vulnerabilities.id"), nullable=True)
    requester = Column(String)  # User who initiated the request
    approver = Column(String, nullable=True)  # User who approved/rejected
    status = Column(String, default="pending")  # pending, approved, rejected, expired
    priority = Column(String, default="medium")  # low, medium, high, critical
    justification = Column(Text)  # Why this action is needed
    risk_assessment = Column(Text)  # Potential risks of the action
    details = Column(JSON)  # Additional context (scan parameters, remediation steps, etc.)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)  # Auto-reject after this time
    approval_notes = Column(Text, nullable=True)  # Approver's comments

    target_asset = relationship("Asset", foreign_keys=[target_asset_id])
    target_vulnerability = relationship("Vulnerability", foreign_keys=[target_vulnerability_id])

# --- WEB PENTESTING MODELS (NEW) ---

class WebTarget(Base):
    __tablename__ = "web_targets"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, unique=True, index=True)
    root_url = Column(String)
    scope_description = Column(Text) # Explicit scope definition
    authorized = Column(Boolean, default=False) # MUST be true to run scans (Phase 1)
    authorization_ref = Column(String, nullable=True) # Reference to signed auth agreement
    tech_stack = Column(JSON) # Fingerprinted technologies (Frameworks, CMS, etc.)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    sessions = relationship("PentestSession", back_populates="target")

class PentestSession(Base):
    __tablename__ = "pentest_sessions"

    id = Column(Integer, primary_key=True, index=True)
    target_id = Column(Integer, ForeignKey("web_targets.id"))
    status = Column(String) # planning, scanning, analyzing, validating, done
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    findings_summary = Column(JSON)
    logs = Column(JSON) # High-level audit log of actions

    target = relationship("WebTarget", back_populates="sessions")
    findings = relationship("WebFinding", back_populates="session")

class WebFinding(Base):
    __tablename__ = "web_findings"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("pentest_sessions.id"))
    title = Column(String)
    url = Column(String)
    severity = Column(String) # critical, high, medium, low, info
    description = Column(Text)
    evidence = Column(Text) # Request/Response dump
    remediation_advice = Column(Text)
    confirmed_by_validation = Column(Boolean, default=False) # Phase 4

    session = relationship("PentestSession", back_populates="findings")

# Update Asset model to include network_services relationship
Asset.network_services = relationship("NetworkService", back_populates="asset")

# --- CHAT & CONTEXT MODELS (NEW) ---

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String) # Placeholder for user auth
    title = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)

    messages = relationship("ChatMessage", back_populates="session")

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"))
    role = Column(String) # user, bot, system
    content = Column(Text)
    intent = Column(String, nullable=True) # captured intent
    context_used = Column(JSON, nullable=True) # IDs of assets/vulns referenced
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")
