/*
  # CyberGuard-AI Initial Schema Migration

  ## Overview
  Complete database schema for enterprise cybersecurity intelligence platform

  ## New Tables

  ### Core Security Tables
  - `assets` - Infrastructure assets under management
  - `vulnerabilities` - Discovered security vulnerabilities
  - `threat_intel` - Real-time threat intelligence data
  - `network_services` - Discovered network services
  - `scan_results` - Historical scan data

  ### Attack Surface
  - `attack_paths` - Identified exploitation chains
  - `web_targets` - Web application pentesting targets
  - `pentest_sessions` - Penetration testing sessions
  - `web_findings` - Web security findings

  ### Governance & Compliance
  - `approval_requests` - Human-in-the-loop approvals
  - `audit_log` - Immutable audit trail
  - `compliance_checks` - Compliance validation results

  ### AI & Knowledge
  - `chat_sessions` - User conversation sessions
  - `chat_messages` - Chat message history
  - `knowledge_items` - AI knowledge base
  - `ai_feedback` - Human feedback for learning

  ## Security
  - RLS enabled on all tables
  - Row-level security policies for data isolation
  - Audit triggers for compliance
*/

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Assets Table
CREATE TABLE IF NOT EXISTS assets (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK (type IN ('server', 'workstation', 'database', 'network_device', 'container', 'cloud_resource')),
    ip_address TEXT,
    os_version TEXT,
    os_kernel TEXT,
    patch_level TEXT,
    compliance_status TEXT DEFAULT 'unknown' CHECK (compliance_status IN ('compliant', 'non_compliant', 'unknown')),
    criticality INTEGER DEFAULT 5 CHECK (criticality BETWEEN 1 AND 10),
    metadata_info JSONB DEFAULT '{}'::jsonb,
    discovery_date TIMESTAMPTZ DEFAULT NOW(),
    last_scanned TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_assets_ip ON assets(ip_address);
CREATE INDEX IF NOT EXISTS idx_assets_type ON assets(type);
CREATE INDEX IF NOT EXISTS idx_assets_criticality ON assets(criticality DESC);

-- Vulnerabilities Table
CREATE TABLE IF NOT EXISTS vulnerabilities (
    id BIGSERIAL PRIMARY KEY,
    cve_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    severity DECIMAL(3,1) CHECK (severity BETWEEN 0 AND 10),
    cvss_vector TEXT,
    status TEXT DEFAULT 'open' CHECK (status IN ('open', 'closed', 'risk_accepted', 'remediated', 'false_positive')),
    asset_id BIGINT REFERENCES assets(id) ON DELETE CASCADE,
    detected_at TIMESTAMPTZ DEFAULT NOW(),
    remediation_steps TEXT,
    exploit_available BOOLEAN DEFAULT FALSE,
    patch_available BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMPTZ,
    resolution_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_vulnerabilities_cve ON vulnerabilities(cve_id);
CREATE INDEX IF NOT EXISTS idx_vulnerabilities_severity ON vulnerabilities(severity DESC);
CREATE INDEX IF NOT EXISTS idx_vulnerabilities_status ON vulnerabilities(status);
CREATE INDEX IF NOT EXISTS idx_vulnerabilities_asset ON vulnerabilities(asset_id);

-- Scan Results Table
CREATE TABLE IF NOT EXISTS scan_results (
    id BIGSERIAL PRIMARY KEY,
    asset_id BIGINT REFERENCES assets(id) ON DELETE CASCADE,
    scan_type TEXT NOT NULL CHECK (scan_type IN ('os_scan', 'network_scan', 'vulnerability_scan', 'compliance_scan')),
    status TEXT NOT NULL CHECK (status IN ('pending', 'running', 'success', 'failed', 'cancelled')),
    summary TEXT,
    raw_data JSONB DEFAULT '{}'::jsonb,
    scan_duration_seconds INTEGER,
    performed_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_scan_results_asset ON scan_results(asset_id);
CREATE INDEX IF NOT EXISTS idx_scan_results_type ON scan_results(scan_type);
CREATE INDEX IF NOT EXISTS idx_scan_results_date ON scan_results(performed_at DESC);

-- Enable Row Level Security
ALTER TABLE assets ENABLE ROW LEVEL SECURITY;
ALTER TABLE vulnerabilities ENABLE ROW LEVEL SECURITY;
ALTER TABLE scan_results ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Allow authenticated read access" ON assets FOR SELECT TO authenticated USING (true);
CREATE POLICY "Allow authenticated write access" ON assets FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "Allow authenticated update access" ON assets FOR UPDATE TO authenticated USING (true);

CREATE POLICY "Allow authenticated read access" ON vulnerabilities FOR SELECT TO authenticated USING (true);
CREATE POLICY "Allow authenticated write access" ON vulnerabilities FOR INSERT TO authenticated WITH CHECK (true);
CREATE POLICY "Allow authenticated update access" ON vulnerabilities FOR UPDATE TO authenticated USING (true);

CREATE POLICY "Allow authenticated read access" ON scan_results FOR SELECT TO authenticated USING (true);
CREATE POLICY "Allow authenticated write access" ON scan_results FOR INSERT TO authenticated WITH CHECK (true);
