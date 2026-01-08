# CyberGuard-AI Deployment Guide

## Quick Start (Development)

### Prerequisites
- Python 3.10+
- Node.js 18+
- Supabase account (free tier available)
- Google Gemini API key

### Backend Setup

```bash
# 1. Navigate to backend directory
cd backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
# Supabase connection is auto-configured
# Only need to set Gemini API key
export GEMINI_API_KEY="your_gemini_api_key_here"

# 5. Seed knowledge database (one-time)
python -c "
from app.knowledge_seeder import seed_knowledge_database
from app.database import SessionLocal
import asyncio

db = SessionLocal()
asyncio.run(seed_knowledge_database(db))
db.close()
"

# 6. Start backend server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Setup

```bash
# 1. Navigate to frontend directory
cd cyberguard-ai

# 2. Install dependencies
npm install

# 3. Start development server
npm run dev
```

### Initial Data Population

```bash
# Seed sample assets and vulnerabilities
curl -X POST http://localhost:8000/seed

# Ingest CISA threat intelligence
curl -X POST http://localhost:8000/api/threat-intel/ingest/cisa-kev
```

### Verify Installation

```bash
# Check backend health
curl http://localhost:8000/health

# Check AI test results
cd backend
python run_ai_tests.py

# Access frontend
# Open browser to http://localhost:3000
```

---

## Production Deployment

### 1. Supabase Setup

The database is already configured to use Supabase. The migrations have been applied automatically.

**Verify Supabase Connection:**
```bash
# Check tables exist
curl http://localhost:8000/assets
curl http://localhost:8000/vulnerabilities
```

### 2. Environment Variables

**Required:**
```bash
GEMINI_API_KEY=your_gemini_api_key_here
```

**Auto-configured (Supabase):**
```bash
SUPABASE_URL=<provided_by_platform>
SUPABASE_ANON_KEY=<provided_by_platform>
SUPABASE_SERVICE_ROLE_KEY=<provided_by_platform>
```

**Optional:**
```bash
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
```

### 3. Performance Optimization

**Enable Production Mode:**
```bash
# Frontend
cd cyberguard-ai
npm run build
npm start

# Backend
cd backend
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

**Configure Caching:**
```python
# In core_ai.py
self.cache = ResponseCache(ttl_seconds=3600)  # 1 hour
```

### 4. Security Checklist

- [ ] Set strong `GEMINI_API_KEY`
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS properly
- [ ] Enable rate limiting
- [ ] Set up firewall rules
- [ ] Configure Supabase RLS policies per organization
- [ ] Enable audit logging
- [ ] Set up backup schedule

### 5. Monitoring

**Health Checks:**
```bash
# Backend
curl http://localhost:8000/health

# Threat Intelligence Status
curl http://localhost:8000/api/threat-intel/status

# AI Metrics
curl http://localhost:8000/api/metrics/kpis
```

**Log Monitoring:**
```bash
# Backend logs
tail -f logs/cyberguard.log

# Audit trail
curl http://localhost:8000/api/audit/recent
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     User Interface                       │
│  Next.js + React + TailwindCSS + Framer Motion         │
└────────────────┬────────────────────────────────────────┘
                 │
                 │ HTTP/WebSocket
                 ▼
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Backend                       │
├─────────────────────────────────────────────────────────┤
│  Core AI (Gemini 2.0 Flash + Cache)                    │
│  Enhanced Reasoning (Multi-hop + ToT)                   │
│  Vector Search (pgvector + Embeddings)                  │
│  Threat Intelligence (CISA KEV)                         │
│  Governance Engine (Approval Workflows)                 │
└──────┬──────────────┬──────────────┬───────────────────┘
       │              │              │
       ▼              ▼              ▼
  ┌─────────┐  ┌──────────┐  ┌──────────┐
  │Supabase │  │ Gemini   │  │  Neo4j   │
  │PostgreSQL│  │ API      │  │  Graph   │
  │ + RLS   │  │          │  │  (opt)   │
  └─────────┘  └──────────┘  └──────────┘
```

---

## Troubleshooting

### Backend Issues

**Problem: "GEMINI_API_KEY not set. Using Mock Mode."**
- Solution: Set environment variable `export GEMINI_API_KEY="your_key"`
- Verify: `echo $GEMINI_API_KEY`

**Problem: Database connection failed**
- Check Supabase credentials are auto-configured
- Verify network connectivity
- Check Supabase project is active

**Problem: Knowledge seeding fails**
- Ensure database tables exist (migrations applied)
- Check Gemini API key for embeddings
- Verify sufficient API quota

### Frontend Issues

**Problem: "Cannot connect to backend"**
- Verify backend is running on port 8000
- Check CORS configuration
- Verify `NEXT_PUBLIC_API_URL` if using custom URL

**Problem: Chat not responding**
- Check backend logs for errors
- Verify Gemini API key is set
- Test endpoint: `curl http://localhost:8000/chat -d '{"message":"test"}'`

### Performance Issues

**Problem: Slow response times**
- Enable response caching (default: 30min)
- Check Gemini API rate limits
- Consider using Redis for distributed caching
- Monitor database query performance

---

## Scaling Recommendations

### For 100+ Users
- Use Gunicorn with 4-8 workers
- Enable Redis caching
- Configure CDN for frontend
- Set up load balancer

### For 1000+ Users
- Horizontal scaling with Kubernetes
- Separate read/write database replicas
- Implement message queue (RabbitMQ/Redis)
- Use dedicated vector search service

### For Enterprise
- Multi-region deployment
- Dedicated Supabase instance
- Custom Gemini API quota
- 24/7 monitoring and alerting
- Disaster recovery plan

---

## API Documentation

Once deployed, access interactive API docs:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Support & Resources

- **Documentation**: See README.md and implementation docs
- **API Reference**: http://localhost:8000/docs
- **Test Suite**: `python run_ai_tests.py`
- **Upgrade Guide**: See UPGRADE_SUMMARY.md

---

## Success Criteria

Your deployment is successful when:
- [ ] Backend health check returns `{"status": "healthy"}`
- [ ] Frontend loads at http://localhost:3000
- [ ] Chat responds with intelligent answers
- [ ] Test pass rate shows 95%+ (with API key)
- [ ] Threat intelligence ingests successfully
- [ ] Vector search returns relevant results
- [ ] Audit logs are recording decisions

---

**Status**: PRODUCTION READY
**Last Updated**: 2026-01-08
**Version**: 2.0.0 (Enterprise Upgrade)
