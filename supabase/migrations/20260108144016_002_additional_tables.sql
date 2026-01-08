/*
  # Additional Security Tables

  ## New Tables
  - `network_services` - Network service discovery
  - `attack_paths` - Attack path modeling
  - `threat_intel` - Threat intelligence feeds
  - `approval_requests` - Governance approvals
  - `knowledge_items` - AI knowledge base
  - `audit_log` - Security audit trail

  ## Security
  All tables have RLS enabled with authenticated user access
*/

-- Network Services Table
CREATE TABLE IF NOT EXISTS network_services (
    id BIGSERIAL PRIMARY KEY,
    asset_id BIGINT REFERENCES assets(id) ON DELETE CASCADE,
    port INTEGER NOT NULL CHECK (port BETWEEN 1 AND 65535),
    protocol TEXT NOT NULL CHECK (protocol IN ('tcp', 'udp')),
    service_name TEXT,
    service_version TEXT,
    state TEXT CHECK (state IN ('open', 'closed', 'filtered')),
    banner TEXT,
    risk_level TEXT CHECK (risk_level IN ('critical', 'high', 'medium', 'low', 'info')),
    discovered_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_network_services_asset ON network_services(asset_id);
CREATE INDEX IF NOT EXISTS idx_network_services_port ON network_services(port);
CREATE INDEX IF NOT EXISTS idx_network_services_risk ON network_services(risk_level);

-- Attack Paths Table
CREATE TABLE IF NOT EXISTS attack_paths (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    entry_point_asset_id BIGINT REFERENCES assets(id),
    target_asset_id BIGINT REFERENCES assets(id),
    path_steps JSONB NOT NULL DEFAULT '[]'::jsonb,
    exploited_vulnerabilities JSONB DEFAULT '[]'::jsonb,
    likelihood_score DECIMAL(4,2) CHECK (likelihood_score BETWEEN 0 AND 10),
    impact_score DECIMAL(4,2) CHECK (impact_score BETWEEN 0 AND 10),
    risk_score DECIMAL(4,2) CHECK (risk_score BETWEEN 0 AND 10),
    mitigation_priority INTEGER CHECK (mitigation_priority BETWEEN 1 AND 5),
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'mitigated', 'risk_accepted', 'false_positive')),
    discovered_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_attack_paths_risk ON attack_paths(risk_score DESC);
CREATE INDEX IF NOT EXISTS idx_attack_paths_status ON attack_paths(status);

-- Threat Intelligence Table
CREATE TABLE IF NOT EXISTS threat_intel (
    id BIGSERIAL PRIMARY KEY,
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT,
    threat_type TEXT CHECK (threat_type IN ('malware', 'apt', 'vulnerability', 'exploit', 'ioc', 'campaign')),
    threat_actor TEXT,
    iocs JSONB DEFAULT '{}'::jsonb,
    confidence_score DECIMAL(3,2) CHECK (confidence_score BETWEEN 0 AND 1),
    severity TEXT CHECK (severity IN ('critical', 'high', 'medium', 'low', 'info')),
    published_date TIMESTAMPTZ,
    ingested_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_threat_intel_source ON threat_intel(source);
CREATE INDEX IF NOT EXISTS idx_threat_intel_type ON threat_intel(threat_type);
CREATE INDEX IF NOT EXISTS idx_threat_intel_date ON threat_intel(published_date DESC);

-- Approval Requests Table
CREATE TABLE IF NOT EXISTS approval_requests (
    id BIGSERIAL PRIMARY KEY,
    request_type TEXT NOT NULL CHECK (request_type IN ('scan', 'remediation', 'config_change', 'risk_acceptance', 'web_pentest_auth')),
    action TEXT NOT NULL,
    target_asset_id BIGINT REFERENCES assets(id),
    target_vulnerability_id BIGINT REFERENCES vulnerabilities(id),
    requester TEXT NOT NULL,
    approver TEXT,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected', 'expired', 'cancelled')),
    priority TEXT DEFAULT 'medium' CHECK (priority IN ('critical', 'high', 'medium', 'low')),
    justification TEXT,
    risk_assessment TEXT,
    details JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    reviewed_at TIMESTAMPTZ,
    expires_at TIMESTAMPTZ,
    approval_notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_approval_requests_status ON approval_requests(status);
CREATE INDEX IF NOT EXISTS idx_approval_requests_requester ON approval_requests(requester);

-- Knowledge Items Table
CREATE TABLE IF NOT EXISTS knowledge_items (
    id BIGSERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    knowledge_type TEXT CHECK (knowledge_type IN ('fact', 'best_practice', 'heuristic', 'learned_pattern')),
    source TEXT NOT NULL,
    tags TEXT[] DEFAULT '{}',
    confidence DECIMAL(3,2) DEFAULT 1.0 CHECK (confidence BETWEEN 0 AND 1),
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_knowledge_items_type ON knowledge_items(knowledge_type);
CREATE INDEX IF NOT EXISTS idx_knowledge_items_source ON knowledge_items(source);

-- Audit Log Table
CREATE TABLE IF NOT EXISTS audit_log (
    id BIGSERIAL PRIMARY KEY,
    user_role TEXT NOT NULL,
    intent TEXT,
    message TEXT,
    action_category TEXT,
    governance_decision TEXT,
    response_summary TEXT,
    knowledge_sources JSONB DEFAULT '[]'::jsonb,
    reasoning_summary TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_log_date ON audit_log(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_log_category ON audit_log(action_category);

-- Enable RLS
ALTER TABLE network_services ENABLE ROW LEVEL SECURITY;
ALTER TABLE attack_paths ENABLE ROW LEVEL SECURITY;
ALTER TABLE threat_intel ENABLE ROW LEVEL SECURITY;
ALTER TABLE approval_requests ENABLE ROW LEVEL SECURITY;
ALTER TABLE knowledge_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE audit_log ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Allow authenticated access" ON network_services FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Allow authenticated access" ON attack_paths FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Allow authenticated access" ON threat_intel FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Allow authenticated access" ON approval_requests FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Allow authenticated access" ON knowledge_items FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Allow authenticated read" ON audit_log FOR SELECT TO authenticated USING (true);
CREATE POLICY "Allow authenticated insert" ON audit_log FOR INSERT TO authenticated WITH CHECK (true);
