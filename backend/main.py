from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app import models, crud, database
from app.audit_routes import router as audit_router
from app.testing_routes import router as testing_router
from app.metrics_routes import router as metrics_router
from app.learning_routes import router as learning_router
from typing import List
import datetime

app = FastAPI(
    title="CyberGuard-AI API",
    description="Backend API for CyberGuard-AI Security Platform",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes for enterprise pillars
app.include_router(audit_router, prefix="/api", tags=["audit"])
app.include_router(testing_router, prefix="/api", tags=["testing"])
app.include_router(metrics_router, prefix="/api", tags=["metrics"])
app.include_router(learning_router, prefix="/api", tags=["learning"])

@app.get("/")
async def root():
    return {"message": "Welcome to CyberGuard-AI API", "status": "online"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/assets", response_model=List[dict])
def read_assets(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    assets = crud.get_assets(db, skip=skip, limit=limit)
    # Convert to dict for simplicity in this prototype
    return [
        {
            "id": a.id, 
            "name": a.name, 
            "type": a.type, 
            "ip_address": a.ip_address, 
            "criticality": a.criticality
        } for a in assets
    ]

@app.get("/vulnerabilities", response_model=List[dict])
def read_vulnerabilities(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    vulns = crud.get_vulnerabilities(db, skip=skip, limit=limit)
    return [
        {
            "id": v.id,
            "cve_id": v.cve_id,
            "title": v.title,
            "severity": v.severity,
            "status": v.status
        } for v in vulns
    ]

from app.ai_service import ai_service
from app.scanner_service import scanner_service
from app.remediation_service import remediation_service

@app.post("/analyze-vulnerability/{vuln_id}")
async def analyze_vulnerability(vuln_id: int, db: Session = Depends(database.get_db)):
    vuln = db.query(models.Vulnerability).filter(models.Vulnerability.id == vuln_id).first()
    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    
    analysis = await ai_service.analyze_vulnerability(vuln.cve_id, vuln.description)
    return {"id": vuln_id, "analysis": analysis}

@app.post("/voice-command")
async def handle_voice_command(data: dict):
    command = data.get("command")
    if not command:
        raise HTTPException(status_code=400, detail="Command is required")
    
    try:
        result = await ai_service.parse_voice_command(command)
        return {"response": result}
    except Exception as e:
        print(f"Voice Command Error: {str(e)}")
        return {"response": "I'm having trouble connecting to my neural core. Please ensure the API key is configured."}

@app.post("/chat")
async def chat_with_ai(data: dict, db: Session = Depends(database.get_db)):
    message = data.get("message")
    session_id = data.get("session_id")
    # Phase 6: Role Adaptation
    user_role = data.get("user_role", "Analyst") 
    
    if not message:
        raise HTTPException(status_code=400, detail="Message is required")
    
    # Get or Create Session
    if session_id:
        session = db.query(models.ChatSession).filter(models.ChatSession.id == session_id).first()
        if not session:
             # Fallback to new session if ID invalid
             session = models.ChatSession(title=message[:30], user_id="user_1")
             db.add(session)
             db.commit()
             db.refresh(session)
    else:
        session = models.ChatSession(title=message[:30], user_id="user_1")
        db.add(session)
        db.commit()
        db.refresh(session)
    
    # Store User Message
    user_msg = models.ChatMessage(session_id=session.id, role="user", content=message)
    db.add(user_msg)
    db.commit()
    
    # Get History
    history_objs = db.query(models.ChatMessage).filter(models.ChatMessage.session_id == session.id).order_by(models.ChatMessage.created_at.desc()).limit(10).all()
    history = [{"role": m.role, "content": m.content} for m in reversed(history_objs)]
    
    # Gather Context (Phase 3: RAG)
    try:
        from app.knowledge_service import knowledge_service
        context = knowledge_service.retrieve_context(db, message)
        print(f"RAG Context retrieved: {len(context)} chars")
    except Exception as e:
        print(f"RAG Error: {e}")
        context = "Context retrieval failed. Answer based on general knowledge."
        
    try:
        # Call AI Service with History and Role (Phase 6)
        result = await ai_service.chat_response(message, context=context, history=history, user_role=user_role)
        response_text = result["response"]
        intent = result["intent"]
        
        # Store Bot Message
        bot_msg = models.ChatMessage(
            session_id=session.id, 
            role="bot", 
            content=response_text,
            intent=intent
        )
        db.add(bot_msg)
        db.commit()
        
        return {
            "response": response_text, 
            "session_id": session.id, 
            "intent": intent,
            "audit_id": result.get("audit_id")
        }
        
    except Exception as e:
        print(f"Chat Error: {str(e)}")
        return {"response": "Neural Link synchronization failed. Please check backend credentials.", "session_id": session.id}

@app.get("/chat/sessions")
def get_chat_sessions(db: Session = Depends(database.get_db)):
    sessions = db.query(models.ChatSession).filter(models.ChatSession.is_active == True).order_by(models.ChatSession.created_at.desc()).limit(20).all()
    return sessions

@app.get("/chat/session/{session_id}")
def get_chat_history(session_id: int, db: Session = Depends(database.get_db)):
    messages = db.query(models.ChatMessage).filter(models.ChatMessage.session_id == session_id).order_by(models.ChatMessage.created_at.asc()).all()
    return messages

@app.get("/generate-report")
async def generate_report(db: Session = Depends(database.get_db)):
    assets = crud.get_assets(db)
    vulns = crud.get_vulnerabilities(db)
    
    report_content = f"# CyberGuard-AI Security Posture Report\n\n"
    report_content += f"## Executive Summary\n"
    report_content += f"Total Assets Scanned: {len(assets)}\n"
    report_content += f"Active Vulnerabilities: {len(vulns)}\n\n"
    
    report_content += "## Critical Assets\n"
    for a in assets:
        if a.criticality >= 8:
            report_content += f"- **{a.name}** ({a.ip_address}): Criticality {a.criticality}/10\n"
            
    report_content += "\n## Vulnerability Details\n"
    for v in vulns:
        report_content += f"### {v.cve_id}: {v.title}\n"
        report_content += f"- Severity: {v.severity}/10\n"
        report_content += f"- Status: {v.status}\n\n"

    # Optionally use AI to summarize the report
    try:
        summary = await ai_service.chat_response(
            "Summarize this security report for a CISO. Keep it to 3 bullet points.", 
            context=report_content
        )
        report_content += f"\n## AI Executive Summary\n{summary}"
    except:
        report_content += "\n## AI Executive Summary\n*Neural Link unavailable. Summary skipped.*"

    return {"report": report_content}

@app.post("/scan/os/{asset_id}")
async def scan_os(asset_id: int, db: Session = Depends(database.get_db)):
    """
    Perform an authorized OS scan on the specified asset.
    This simulates credentialed scanning (SSH/WinRM) to gather:
    - OS version and kernel information
    - Patch levels
    - Compliance status
    - OS-level vulnerabilities
    """
    result = await scanner_service.run_os_scan(db, asset_id)
    return result

@app.get("/scan/history/{asset_id}")
def get_scan_history(asset_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve the scan history for a specific asset.
    """
    scans = db.query(models.ScanResult).filter(
        models.ScanResult.asset_id == asset_id
    ).order_by(models.ScanResult.performed_at.desc()).all()
    
    return [
        {
            "id": s.id,
            "scan_type": s.scan_type,
            "status": s.status,
            "summary": s.summary,
            "performed_at": s.performed_at.isoformat()
        } for s in scans
    ]

@app.post("/scan/network/{asset_id}")
async def scan_network(asset_id: int, db: Session = Depends(database.get_db)):
    """
    Perform network service enumeration and port scanning on the specified asset.
    Discovers open ports, running services, versions, and assesses risk levels.
    """
    result = await scanner_service.run_network_scan(db, asset_id)
    return result

@app.get("/services/{asset_id}")
def get_asset_services(asset_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve all discovered network services for a specific asset.
    """
    services = db.query(models.NetworkService).filter(
        models.NetworkService.asset_id == asset_id
    ).all()
    
    return [
        {
            "id": s.id,
            "port": s.port,
            "protocol": s.protocol,
            "service_name": s.service_name,
            "service_version": s.service_version,
            "state": s.state,
            "risk_level": s.risk_level,
            "discovered_at": s.discovered_at.isoformat()
        } for s in services
    ]

@app.post("/analyze/attack-paths")
async def analyze_attack_paths(db: Session = Depends(database.get_db)):
    """
    Analyze the entire infrastructure to identify potential attack paths.
    Maps exploitation chains from entry points to critical assets.
    """
    result = await scanner_service.analyze_attack_paths(db)
    return result

@app.get("/attack-paths")
def get_attack_paths(db: Session = Depends(database.get_db)):
    """
    Retrieve all identified attack paths, sorted by risk score.
    """
    paths = db.query(models.AttackPath).order_by(
        models.AttackPath.risk_score.desc()
    ).all()
    
    return [
        {
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "entry_point": p.entry_point.name if p.entry_point else "Unknown",
            "target": p.target.name if p.target else "Unknown",
            "path_steps": p.path_steps,
            "exploited_vulnerabilities": p.exploited_vulnerabilities,
            "likelihood_score": p.likelihood_score,
            "impact_score": p.impact_score,
            "risk_score": p.risk_score,
            "mitigation_priority": p.mitigation_priority,
            "status": p.status
        } for p in paths
    ]

@app.post("/approval/request")
def create_approval_request(request_data: dict, db: Session = Depends(database.get_db)):
    """
    Create a new approval request for high-risk operations.
    Requires justification and risk assessment.
    """
    approval = models.ApprovalRequest(
        request_type=request_data.get("request_type"),
        action=request_data.get("action"),
        target_asset_id=request_data.get("target_asset_id"),
        target_vulnerability_id=request_data.get("target_vulnerability_id"),
        requester=request_data.get("requester", "system"),
        priority=request_data.get("priority", "medium"),
        justification=request_data.get("justification"),
        risk_assessment=request_data.get("risk_assessment"),
        details=request_data.get("details", {}),
        expires_at=datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    )
    
    db.add(approval)
    db.commit()
    db.refresh(approval)
    
    return {
        "id": approval.id,
        "status": "pending",
        "message": "Approval request created. Awaiting authorization."
    }

@app.get("/approval/requests")
def get_approval_requests(
    status: str = None,
    db: Session = Depends(database.get_db)
):
    """
    Retrieve all approval requests, optionally filtered by status.
    """
    query = db.query(models.ApprovalRequest)
    
    if status:
        query = query.filter(models.ApprovalRequest.status == status)
    
    requests = query.order_by(models.ApprovalRequest.created_at.desc()).all()
    
    return [
        {
            "id": r.id,
            "request_type": r.request_type,
            "action": r.action,
            "target_asset": r.target_asset.name if r.target_asset else None,
            "target_vulnerability": r.target_vulnerability.cve_id if r.target_vulnerability else None,
            "requester": r.requester,
            "approver": r.approver,
            "status": r.status,
            "priority": r.priority,
            "justification": r.justification,
            "risk_assessment": r.risk_assessment,
            "details": r.details,
            "created_at": r.created_at.isoformat(),
            "reviewed_at": r.reviewed_at.isoformat() if r.reviewed_at else None,
            "expires_at": r.expires_at.isoformat() if r.expires_at else None,
            "approval_notes": r.approval_notes
        } for r in requests
    ]

@app.post("/approval/{request_id}/review")
async def review_approval_request(
    request_id: int,
    review_data: dict,
    db: Session = Depends(database.get_db)
):
    """
    Approve or reject an approval request.
    """
    approval = db.query(models.ApprovalRequest).filter(
        models.ApprovalRequest.id == request_id
    ).first()
    
    if not approval:
        raise HTTPException(status_code=404, detail="Approval request not found")
    
    if approval.status != "pending":
        raise HTTPException(status_code=400, detail=f"Request already {approval.status}")
    
    decision = review_data.get("decision")  # "approved" or "rejected"
    if decision not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Decision must be 'approved' or 'rejected'")
    
    approval.status = decision
    approval.approver = review_data.get("approver", "admin")
    approval.approval_notes = review_data.get("notes")
    approval.reviewed_at = datetime.datetime.utcnow()
    
    db.commit()
    
    # If approved, execute the action
    result = None
    if decision == "approved":
        if approval.request_type == "scan":
            # Trigger the scan that was requested
            result = {"message": f"Scan approved and queued for {approval.target_asset.name if approval.target_asset else 'target'}"}
        elif approval.request_type == "remediation":
            # Execute remediation immediately upon approval
            result = await remediation_service.execute_remediation(db, approval)
        elif approval.request_type == "risk_acceptance":
            # Mark vulnerability as risk accepted
            if approval.target_vulnerability_id:
                vuln = db.query(models.Vulnerability).filter(
                    models.Vulnerability.id == approval.target_vulnerability_id
                ).first()
                if vuln:
                    vuln.status = "risk_accepted"
                    db.commit()
                if vuln:
                    vuln.status = "risk_accepted"
                    db.commit()
                    result = {"message": f"Risk accepted for {vuln.cve_id}"}
        elif approval.request_type == "web_pentest_auth":
            # Phase 1: Activate the Authorization in the WebPentestService
            target_id = approval.details.get("web_target_id")
            if target_id:
                # Import here to avoid circular dependencies if any
                from app.web_pentest_service import web_pentest_service
                web_pentest_service.authorize_target(db, target_id, f"Approved by {approval.approver} on {approval.reviewed_at}")
                result = {"message": "Web Target Authorized. Scanning is now permitted."}
    
    return {
        "id": approval.id,
        "status": approval.status,
        "reviewed_by": approval.approver,
        "reviewed_at": approval.reviewed_at.isoformat(),
        "action_result": result
    }

@app.post("/seed")
def seed_database(db: Session = Depends(database.get_db)):
    # Seed Assets
    assets = [
        {"name": "Web-Server-01", "type": "server", "ip_address": "192.168.1.10", "criticality": 8},
        {"name": "DB-Primary", "type": "database", "ip_address": "192.168.1.20", "criticality": 10},
        {"name": "Admin-Workstation", "type": "workstation", "ip_address": "192.168.1.50", "criticality": 5},
    ]
    for asset_data in assets:
        crud.create_asset(db, asset_data)
    
    # Reload assets to get IDs
    db_assets = crud.get_assets(db)
    
    # Seed Vulnerabilities
    vulns = [
        {"cve_id": "CVE-2024-1234", "title": "SSRF in Web API", "description": "High severity SSRF...", "severity": 8.5, "asset_id": db_assets[0].id},
        {"cve_id": "CVE-2023-5678", "title": "Weak SSH Auth", "description": "Medium severity...", "severity": 5.0, "asset_id": db_assets[1].id},
    ]
    for vuln_data in vulns:
        crud.create_vulnerability(db, vuln_data)
        
# --- WEB PENTESTING ENDPOINTS ---

from app.web_pentest_service import web_pentest_service
import app.web_schemas as web_schemas

@app.post("/web/targets")
def register_web_target(target_data: dict, db: Session = Depends(database.get_db)):
    """
    Phase 1: Register a new website target.
    Start as UNAUTHORIZED.
    """
    target = web_pentest_service.create_target(db, target_data)
    
    # Auto-create an approval request for this target
    approval = models.ApprovalRequest(
        request_type="web_pentest_auth",
        action=f"Authorize Pentesting for {target.domain}",
        target_asset_id=None, # It's a web target, not an infrastructure asset yet
        priority="critical",
        justification=f"User requested penetration testing scope for {target.domain}",
        risk_assessment="High risk if unauthorized. Ownership verification required.",
        details={"web_target_id": target.id, "domain": target.domain},
        expires_at=datetime.datetime.utcnow() + datetime.timedelta(hours=48)
    )
    db.add(approval)
    db.commit()
    
    return {"message": "Target registered. Authorization request created.", "target_id": target.id, "approval_id": approval.id}

@app.get("/web/targets")
def get_web_targets(db: Session = Depends(database.get_db)):
    targets = db.query(models.WebTarget).all()
    return targets

@app.post("/web/scan/{target_id}")
def start_web_scan(target_id: int, db: Session = Depends(database.get_db)):
    """
    Phase 2: Start a safe recon scan.
    Enforces authorization check inside the service.
    """
    result = web_pentest_service.start_recon_session(db, target_id)
    if isinstance(result, dict) and result.get("status") == "error":
        raise HTTPException(status_code=403, detail=result["message"])
    
    return {"message": "Scan session started", "session_id": result.id}

@app.get("/web/sessions/{target_id}")
def get_pentest_sessions(target_id: int, db: Session = Depends(database.get_db)):
    sessions = db.query(models.PentestSession).filter(models.PentestSession.target_id == target_id).all()
    return sessions

@app.get("/web/findings/{session_id}")
def get_session_findings(session_id: int, db: Session = Depends(database.get_db)):
    findings = db.query(models.WebFinding).filter(models.WebFinding.session_id == session_id).all()
    return findings


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
