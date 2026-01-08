/*
  # Chat and Web Pentesting Tables

  ## New Tables
  - `chat_sessions` - Chat conversation sessions
  - `chat_messages` - Individual chat messages
  - `web_targets` - Web application targets
  - `pentest_sessions` - Penetration testing sessions
  - `web_findings` - Web security findings
  - `ai_feedback` - Human feedback for AI learning

  ## Security
  All tables secured with RLS policies
*/

-- Chat Sessions Table
CREATE TABLE IF NOT EXISTS chat_sessions (
    id BIGSERIAL PRIMARY KEY,
    user_id TEXT,
    title TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_chat_sessions_user ON chat_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_sessions_active ON chat_sessions(is_active);

-- Chat Messages Table
CREATE TABLE IF NOT EXISTS chat_messages (
    id BIGSERIAL PRIMARY KEY,
    session_id BIGINT REFERENCES chat_sessions(id) ON DELETE CASCADE,
    role TEXT CHECK (role IN ('user', 'bot', 'system')),
    content TEXT NOT NULL,
    intent TEXT,
    context_used JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_chat_messages_session ON chat_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_date ON chat_messages(created_at DESC);

-- Web Targets Table
CREATE TABLE IF NOT EXISTS web_targets (
    id BIGSERIAL PRIMARY KEY,
    domain TEXT UNIQUE NOT NULL,
    root_url TEXT NOT NULL,
    scope_description TEXT,
    authorized BOOLEAN DEFAULT FALSE,
    authorization_ref TEXT,
    tech_stack JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_web_targets_domain ON web_targets(domain);
CREATE INDEX IF NOT EXISTS idx_web_targets_authorized ON web_targets(authorized);

-- Pentest Sessions Table
CREATE TABLE IF NOT EXISTS pentest_sessions (
    id BIGSERIAL PRIMARY KEY,
    target_id BIGINT REFERENCES web_targets(id) ON DELETE CASCADE,
    status TEXT CHECK (status IN ('planning', 'scanning', 'analyzing', 'validating', 'completed', 'failed')),
    start_time TIMESTAMPTZ DEFAULT NOW(),
    end_time TIMESTAMPTZ,
    findings_summary JSONB DEFAULT '{}'::jsonb,
    logs JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_pentest_sessions_target ON pentest_sessions(target_id);
CREATE INDEX IF NOT EXISTS idx_pentest_sessions_status ON pentest_sessions(status);

-- Web Findings Table
CREATE TABLE IF NOT EXISTS web_findings (
    id BIGSERIAL PRIMARY KEY,
    session_id BIGINT REFERENCES pentest_sessions(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    url TEXT,
    severity TEXT CHECK (severity IN ('critical', 'high', 'medium', 'low', 'info')),
    description TEXT,
    evidence TEXT,
    remediation_advice TEXT,
    confirmed_by_validation BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_web_findings_session ON web_findings(session_id);
CREATE INDEX IF NOT EXISTS idx_web_findings_severity ON web_findings(severity);

-- AI Feedback Table
CREATE TABLE IF NOT EXISTS ai_feedback (
    id BIGSERIAL PRIMARY KEY,
    audit_id TEXT NOT NULL,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    comments TEXT,
    correction TEXT,
    status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'reviewed', 'applied', 'rejected')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    reviewed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_ai_feedback_audit ON ai_feedback(audit_id);
CREATE INDEX IF NOT EXISTS idx_ai_feedback_status ON ai_feedback(status);

-- Enable RLS
ALTER TABLE chat_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE chat_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE web_targets ENABLE ROW LEVEL SECURITY;
ALTER TABLE pentest_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE web_findings ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_feedback ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Allow authenticated access" ON chat_sessions FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Allow authenticated access" ON chat_messages FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Allow authenticated access" ON web_targets FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Allow authenticated access" ON pentest_sessions FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Allow authenticated access" ON web_findings FOR ALL TO authenticated USING (true) WITH CHECK (true);
CREATE POLICY "Allow authenticated access" ON ai_feedback FOR ALL TO authenticated USING (true) WITH CHECK (true);

-- Updated at triggers
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_chat_sessions_updated_at BEFORE UPDATE ON chat_sessions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_web_targets_updated_at BEFORE UPDATE ON web_targets FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_knowledge_items_updated_at BEFORE UPDATE ON knowledge_items FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_assets_updated_at BEFORE UPDATE ON assets FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_vulnerabilities_updated_at BEFORE UPDATE ON vulnerabilities FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_attack_paths_updated_at BEFORE UPDATE ON attack_paths FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
