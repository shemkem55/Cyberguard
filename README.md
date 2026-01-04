# 🛡️ CyberGuard-AI

### Enterprise-Grade Cybersecurity Intelligence Platform

> **An AI-powered security intelligence system that continuously assesses, explains, and improves security posture—using safe, authorized, and explainable AI.**

[![Enterprise Ready](https://img.shields.io/badge/Enterprise-Ready-blue)]()
[![Governance](https://img.shields.io/badge/Governance-Enabled-green)]()
[![Audit Trail](https://img.shields.io/badge/Audit-Compliant-orange)]()

---

## 🎯 What Makes This Different

Unlike traditional scanners or offensive tools, CyberGuard-AI combines **deep AI reasoning**, **authorized security validation**, and **professional governance**—delivering security insight you can **explain, defend, and act on**.

### Key Differentiators

| Traditional Tools | CyberGuard-AI |
|-------------------|---------------|
| Findings without context | Explainable intelligence |
| High false positives | Confidence-weighted results |
| Static rules | Adaptive reasoning |
| Tool-driven | Decision-driven |
| Black-box outputs | Auditable logic trails |
| Risky automation | Human-aligned control |

---

## 🏗️ Architecture: Enterprise-Grade Foundations

CyberGuard-AI is built on **4 foundational pillars** that ensure trust, compliance, and effectiveness:

### 1️⃣ **Architectural Maturity**

- **Modular Design**: Separate concerns (Intent, Strategy, Reasoning, Knowledge, Governance)
- **Versioned Services**: Safe upgrades without breaking changes
- **Graceful Degradation**: Fallback to mock mode if APIs unavailable

### 2️⃣ **Intelligence Depth & Reasoning Excellence**

- **Multi-Stage Reasoning Pipeline**:
  1. Observation → Hypothesis → Validation → Conclusion
- **Confidence-Aware Outputs**: Known / Likely / Uncertain
- **Explainability**: Every decision has a reasoning trace

### 3️⃣ **Knowledge Engineering & Intellectual Rigor**

- **Cybersecurity Knowledge Graph**:
  - Facts (CVE data, scan results)
  - Best Practices (OWASP, NIST, CIS)
  - Heuristics (expert observations)
  - Learned Patterns (system observations)
- **Knowledge Decay**: Old information loses confidence over time
- **Source Attribution**: All claims cite authoritative sources

### 4️⃣ **Professional Safety & Governance**

- **Decision Boundaries**: Clear authorization rules
- **Human-in-the-Loop**: Critical actions require approval
- **Immutable Audit Trail**: Every decision logged for compliance
- **Prohibited Actions**: Exploit generation, unauthorized access blocked

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL (optional, SQLite by default)
- Google Gemini API Key (for production mode)

### Backend Setup

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Initialize database
python init_db.py

# Run server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Setup

```bash
cd cyberguard-ai

# Install dependencies
npm install

# Run development server
npm run dev
```

### Access

- **Frontend**: <http://localhost:3000>
- **API Docs**: <http://localhost:8000/docs>
- **Audit Dashboard**: <http://localhost:8000/api/audit/summary>

---

## 🧠 How It Works

### The Enterprise AI Pipeline

Every user query flows through a **7-stage governed pipeline**:

```
User Query 
  ↓
1. Intent Classification (What does the user want?)
  ↓
2. Governance Evaluation (Is this allowed? Requires approval?)
  ↓
3. Strategy Planning (How should we respond? Format? Depth?)
  ↓
4. Knowledge Retrieval (What verified sources apply?)
  ↓
5. Deep Reasoning (Fact observation → Analysis → Safety check → Plan)
  ↓
6. Response Generation (With source citations)
  ↓
7. Audit Logging (Immutable record for compliance)
```

### Example: SQL Injection Remediation Request

**User (Analyst)**: *"How do I fix the SQL injection on the payment gateway?"*

**System Pipeline**:

1. **Intent**: `REMEDIATION_ADVICE`
2. **Governance**: ✅ Allowed (informational/recommendation)
3. **Strategy**: Step-by-step format, technical depth
4. **Knowledge**:
   - *"Use parameterized queries..."* (Source: OWASP Top 10, 95% confidence)
   - *"SQL Injection (CWE-89)..."* (Source: MITRE, 100% confidence)
5. **Reasoning**:
   - Facts: CVE detected in payment gateway
   - Analysis: High severity, data exposure risk
   - Safety: User asking for fix (not exploit) ✓
   - Plan: Provide parameterized query example
6. **Response**:
   > "According to OWASP Top 10, the recommended fix is to use parameterized queries..."
7. **Audit**: Logged with full trace

---

## 📊 Core Features

### 🔍 Intelligent Security Analysis

- **Vulnerability Assessment**: Scans with confidence scoring
- **Threat Intelligence**: AI-powered risk prioritization
- **Attack Path Visualization**: Neo4j-based graph analysis
- **Real-time Monitoring**: Continuous security posture tracking

### 💬 ChatGPT-Level Interaction

- **Role-Adaptive Responses**: Tailored for Executives, Analysts, Engineers
- **Multi-Turn Conversations**: Maintains context and memory
- **Source Citations**: Every claim backed by authoritative sources
- **Professional Tone**: Calm, precise, conservative

### 🛡️ Governance & Compliance

- **Authorization Framework**: RBAC with decision boundaries
- **Approval Workflows**: Human-in-the-loop for critical actions
- **Audit Trail API**: Query decisions by category, user, date
- **JSONL Logging**: Immutable, append-only compliance records

### 🧪 Advanced Capabilities

- **Web Application Penetration Testing**: OWASP Top 10 checks
- **Network Scanning**: Port discovery, service identification
- **OS Fingerprinting**: Attack surface analysis
- **Remediation Guidance**: Framework-specific fix recommendations

---

## 🎯 Use Cases

### For Security Analysts

- Reduce false positives with confidence-weighted findings
- Get instant remediation guidance with source citations
- Query historical decisions via audit trail

### For CISOs & Executives

- Understand risk in business terms (not just CVE IDs)
- Review AI decision audit logs for compliance
- Approve critical security actions before execution

### For DevSecOps Teams

- Integrate security intelligence into CI/CD
- Get framework-specific code fixes (not generic advice)
- Track security posture over time with metrics

---

## 📚 Documentation

- **[Architecture Guide](docs/architecture.md)** - System design and modules
- **[API Reference](http://localhost:8000/docs)** - Interactive Swagger docs
- **[Governance Policy](docs/governance.md)** - Authorization rules
- **[Knowledge Graph Schema](docs/knowledge.md)** - Data model
- **[Deployment Guide](docs/deployment.md)** - Production setup

---

## 🔒 Security & Ethics

### Authorization by Design

- **Scope-Locked**: AI only operates on authorized assets
- **No Exploits**: Prohibited from generating functional attack code
- **Explicit Refusals**: Clearly states when requests violate policy

### Compliance-Ready

- **GDPR**: No PII in logs, data minimization
- **SOC 2**: Audit trail, access controls
- **ISO 27001**: Risk-based approach, documentation

### Responsible AI

- **Transparency**: Reasoning traces available
- **Accountability**: Every decision logged
- **Human Control**: Critical actions require approval

---

## 🧪 Testing & Quality

### AI Model Testing

```bash
# Run reasoning engine tests
pytest backend/tests/test_reasoning.py

# Test governance policies
pytest backend/tests/test_governance.py

# Validate knowledge graph
pytest backend/tests/test_knowledge.py
```

### Security Scanning

```bash
# Scan the codebase itself
bandit -r backend/

# Check dependencies for CVEs
safety check
```

---

## 📈 Roadmap

### Current Stage: **Governed & Auditable** (Stage 3/5)

| Stage | Status | Features |
|-------|--------|----------|
| ✅ Stage 1 | Complete | Functional & capable |
| ✅ Stage 2 | Complete | Reliable & explainable |
| ✅ Stage 3 | Complete | Governed & auditable |
| ⏳ Stage 4 | In Progress | Expert-level reasoning |
| 🔜 Stage 5 | Planned | Enterprise-trusted system |

### Next Features

- [ ] Elite-level communication calibration
- [ ] AI test suites (accuracy, consistency, safety)
- [ ] Professional metrics dashboard (KPIs)
- [ ] SIEM integration (Splunk, ELK)
- [ ] Continuous learning (controlled retraining)
- [ ] Multi-tenant support

---

## 🤝 Contributing

We welcome contributions that align with our **governance-first, safety-first** philosophy.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting PRs.

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

---

## 🌟 Credits

Built with:

- **LangChain** & **Google Gemini** - AI reasoning
- **FastAPI** - Backend framework
- **Next.js** & **React** - Frontend
- **Neo4j** - Attack path graph database
- **Framer Motion** - Animations

---

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/shemkem55/Cyberguard/issues)
- **Discussions**: [GitHub Discussions](https://github.com/shemkem55/Cyberguard/discussions)
- **Email**: <security@cyberguard-ai.com>

---

<div align="center">

**Built with 🛡️ by security professionals, for security professionals.**

*Trusted by enterprises. Governed by humans. Powered by AI.*

</div>
