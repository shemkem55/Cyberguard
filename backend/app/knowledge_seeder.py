from typing import List, Dict
from .vector_search import vector_search_service

class SecurityKnowledge:
    @staticmethod
    def get_cve_knowledge() -> List[Dict]:
        return [
            {
                "content": "CVE-2021-44228 (Log4Shell) is a critical remote code execution vulnerability in Apache Log4j versions 2.0-beta9 to 2.15.0. Allows unauthenticated remote code execution via JNDI lookup.",
                "type": "fact",
                "source": "NIST NVD",
                "tags": ["cve", "rce", "log4j", "critical"]
            },
            {
                "content": "CVE-2023-23397 (Outlook Elevation of Privilege) allows attackers to access Net-NTLMv2 hash and relay for authentication. CVSS 9.8. Affects Microsoft Outlook 2013-2019.",
                "type": "fact",
                "source": "Microsoft Security Response Center",
                "tags": ["cve", "microsoft", "outlook", "elevation"]
            },
            {
                "content": "CVE-2024-3094 (XZ Utils backdoor) is a supply chain compromise affecting XZ Utils 5.6.0 and 5.6.1. Backdoor in SSH authentication allowing unauthorized access.",
                "type": "fact",
                "source": "CISA",
                "tags": ["cve", "supply-chain", "ssh", "backdoor"]
            },
            {
                "content": "CVE-2022-0185 (Linux Kernel heap overflow) allows local privilege escalation in Linux kernel 5.1-rc1 through 5.16. CVSS 8.4. Exploitable through unprivileged user namespace.",
                "type": "fact",
                "source": "Linux Kernel Security",
                "tags": ["cve", "linux", "privilege-escalation"]
            },
            {
                "content": "CVE-2023-34362 (MOVEit Transfer SQL Injection) allows attackers to access MOVEit Transfer database through SQL injection. Zero-day exploited by Cl0p ransomware group.",
                "type": "fact",
                "source": "Progress Software",
                "tags": ["cve", "sql-injection", "zero-day", "ransomware"]
            },
            {
                "content": "CVE-2023-38545 (curl SOCKS5 heap buffer overflow) allows heap-based buffer overflow in curl versions 7.69.0 to 8.3.0 when using SOCKS5 proxy. CVSS 9.8.",
                "type": "fact",
                "source": "curl Security Advisory",
                "tags": ["cve", "curl", "buffer-overflow"]
            },
            {
                "content": "CVE-2022-30190 (Follina) is a Microsoft Support Diagnostic Tool (MSDT) remote code execution vulnerability. Exploited via Microsoft Office documents with malicious external links.",
                "type": "fact",
                "source": "Microsoft",
                "tags": ["cve", "microsoft", "rce", "office"]
            },
            {
                "content": "CVE-2021-26855 (ProxyLogon) is one of four Microsoft Exchange vulnerabilities exploited in the wild. Allows authentication bypass and arbitrary code execution. CVSS 9.8.",
                "type": "fact",
                "source": "Microsoft Exchange Security",
                "tags": ["cve", "exchange", "authentication-bypass"]
            }
        ]

    @staticmethod
    def get_owasp_knowledge() -> List[Dict]:
        return [
            {
                "content": "Broken Access Control (OWASP #1) occurs when users can act outside their intended permissions. Examples: accessing other users' accounts, viewing sensitive files, modifying data.",
                "type": "best_practice",
                "source": "OWASP Top 10 2021",
                "tags": ["owasp", "access-control", "authorization"]
            },
            {
                "content": "Cryptographic Failures (OWASP #2) relate to protecting data in transit and at rest. Use TLS 1.3, avoid deprecated algorithms (MD5, SHA-1), encrypt sensitive data with AES-256.",
                "type": "best_practice",
                "source": "OWASP Top 10 2021",
                "tags": ["owasp", "crypto", "encryption"]
            },
            {
                "content": "Injection attacks (OWASP #3) occur when untrusted data is sent to interpreters. SQL injection, NoSQL injection, OS command injection, LDAP injection. Always use parameterized queries.",
                "type": "best_practice",
                "source": "OWASP Top 10 2021",
                "tags": ["owasp", "injection", "sql-injection"]
            },
            {
                "content": "Insecure Design (OWASP #4) refers to missing or ineffective control design. Establish secure development lifecycle, use threat modeling, implement security patterns.",
                "type": "best_practice",
                "source": "OWASP Top 10 2021",
                "tags": ["owasp", "design", "threat-modeling"]
            },
            {
                "content": "Security Misconfiguration (OWASP #5) includes unnecessary features enabled, default accounts unchanged, error messages revealing stack traces, missing security headers.",
                "type": "best_practice",
                "source": "OWASP Top 10 2021",
                "tags": ["owasp", "configuration", "hardening"]
            },
            {
                "content": "Vulnerable and Outdated Components (OWASP #6): Regularly scan dependencies, remove unused dependencies, obtain components from official sources, monitor CVE databases.",
                "type": "best_practice",
                "source": "OWASP Top 10 2021",
                "tags": ["owasp", "dependencies", "patching"]
            },
            {
                "content": "Identification and Authentication Failures (OWASP #7): Implement multi-factor authentication, avoid default credentials, check password strength, protect against automated attacks.",
                "type": "best_practice",
                "source": "OWASP Top 10 2021",
                "tags": ["owasp", "authentication", "mfa"]
            },
            {
                "content": "Software and Data Integrity Failures (OWASP #8): Verify digital signatures for updates, use CI/CD pipelines with proper separation, ensure data integrity with checksums.",
                "type": "best_practice",
                "source": "OWASP Top 10 2021",
                "tags": ["owasp", "integrity", "supply-chain"]
            },
            {
                "content": "Security Logging and Monitoring Failures (OWASP #9): Log authentication, access control, input validation failures. Enable real-time alerting for suspicious activities.",
                "type": "best_practice",
                "source": "OWASP Top 10 2021",
                "tags": ["owasp", "logging", "monitoring"]
            },
            {
                "content": "Server-Side Request Forgery (SSRF) (OWASP #10): Validate and sanitize all user-supplied URLs, implement network segmentation, use allowlists for remote resources.",
                "type": "best_practice",
                "source": "OWASP Top 10 2021",
                "tags": ["owasp", "ssrf", "validation"]
            }
        ]

    @staticmethod
    def get_mitre_attack_knowledge() -> List[Dict]:
        return [
            {
                "content": "T1059 (Command and Scripting Interpreter): Adversaries abuse command-line interfaces (cmd.exe, PowerShell, Bash) to execute arbitrary commands. Detection: Monitor process creation with command-line arguments.",
                "type": "fact",
                "source": "MITRE ATT&CK",
                "tags": ["mitre", "execution", "powershell"]
            },
            {
                "content": "T1078 (Valid Accounts): Attackers use legitimate credentials to maintain access. Defense: MFA, monitor for impossible travel, detect concurrent sessions from different locations.",
                "type": "fact",
                "source": "MITRE ATT&CK",
                "tags": ["mitre", "persistence", "credential-abuse"]
            },
            {
                "content": "T1003 (OS Credential Dumping): Attackers dump credentials from memory (LSASS), SAM database, or credential stores. Defense: Credential Guard, disable WDigest, monitor LSASS access.",
                "type": "fact",
                "source": "MITRE ATT&CK",
                "tags": ["mitre", "credential-access", "mimikatz"]
            },
            {
                "content": "T1071 (Application Layer Protocol): C2 communications over HTTP/HTTPS, DNS, or common protocols. Detection: Analyze beaconing patterns, inspect TLS certificates, monitor DNS queries.",
                "type": "fact",
                "source": "MITRE ATT&CK",
                "tags": ["mitre", "command-control", "c2"]
            },
            {
                "content": "T1566 (Phishing): Initial access via spear-phishing emails with malicious attachments or links. Defense: Email filtering, security awareness training, link sandboxing.",
                "type": "fact",
                "source": "MITRE ATT&CK",
                "tags": ["mitre", "initial-access", "phishing"]
            },
            {
                "content": "T1486 (Data Encrypted for Impact): Ransomware encrypts files to extort victims. Defense: Offline backups, restrict file system permissions, monitor for mass encryption events.",
                "type": "fact",
                "source": "MITRE ATT&CK",
                "tags": ["mitre", "impact", "ransomware"]
            },
            {
                "content": "T1090 (Proxy): Adversaries use proxies to obfuscate C2 traffic. Includes SOCKS proxies, multi-hop proxies. Detection: Network traffic analysis, identify proxy tools.",
                "type": "fact",
                "source": "MITRE ATT&CK",
                "tags": ["mitre", "command-control", "proxy"]
            },
            {
                "content": "T1053 (Scheduled Task/Job): Persistence via Windows Task Scheduler, cron, at commands. Detection: Monitor scheduled task creation, audit task configurations.",
                "type": "fact",
                "source": "MITRE ATT&CK",
                "tags": ["mitre", "persistence", "scheduled-task"]
            }
        ]

    @staticmethod
    def get_nist_knowledge() -> List[Dict]:
        return [
            {
                "content": "NIST CSF Identify function: Develop organizational understanding of cybersecurity risk to systems, assets, data, and capabilities. Includes asset management, risk assessment.",
                "type": "best_practice",
                "source": "NIST Cybersecurity Framework",
                "tags": ["nist", "csf", "risk-management"]
            },
            {
                "content": "NIST CSF Protect function: Implement safeguards to ensure delivery of critical services. Includes access control, awareness training, data security, protective technology.",
                "type": "best_practice",
                "source": "NIST Cybersecurity Framework",
                "tags": ["nist", "csf", "protection"]
            },
            {
                "content": "NIST CSF Detect function: Develop activities to identify cybersecurity events. Continuous monitoring, detection processes, anomaly detection.",
                "type": "best_practice",
                "source": "NIST Cybersecurity Framework",
                "tags": ["nist", "csf", "detection"]
            },
            {
                "content": "NIST CSF Respond function: Take action regarding detected cybersecurity incidents. Response planning, communications, analysis, mitigation, improvements.",
                "type": "best_practice",
                "source": "NIST Cybersecurity Framework",
                "tags": ["nist", "csf", "incident-response"]
            },
            {
                "content": "NIST CSF Recover function: Maintain plans for resilience and restore capabilities impaired due to cybersecurity incidents. Recovery planning, improvements, communications.",
                "type": "best_practice",
                "source": "NIST Cybersecurity Framework",
                "tags": ["nist", "csf", "recovery"]
            },
            {
                "content": "NIST SP 800-53 Access Control: Implement least privilege, separation of duties, account management, remote access controls, session termination.",
                "type": "best_practice",
                "source": "NIST SP 800-53",
                "tags": ["nist", "access-control", "compliance"]
            },
            {
                "content": "NIST Password Guidelines: Minimum 8 characters for user passwords, 15 for admin. No complexity requirements. Check against compromised password lists. Allow paste functionality.",
                "type": "best_practice",
                "source": "NIST SP 800-63B",
                "tags": ["nist", "passwords", "authentication"]
            }
        ]

    @staticmethod
    def get_cis_controls_knowledge() -> List[Dict]:
        return [
            {
                "content": "CIS Control 1 (Inventory of Assets): Actively manage all enterprise assets connected to infrastructure. Maintain accurate and up-to-date inventory.",
                "type": "best_practice",
                "source": "CIS Controls v8",
                "tags": ["cis", "asset-management"]
            },
            {
                "content": "CIS Control 2 (Software Inventory): Actively manage all software on network to prevent unauthorized software execution and ensure only authorized software is installed.",
                "type": "best_practice",
                "source": "CIS Controls v8",
                "tags": ["cis", "software-inventory"]
            },
            {
                "content": "CIS Control 3 (Data Protection): Develop processes to identify, classify, securely handle, retain, and dispose of data. Implement encryption for data at rest and in transit.",
                "type": "best_practice",
                "source": "CIS Controls v8",
                "tags": ["cis", "data-protection"]
            },
            {
                "content": "CIS Control 4 (Secure Configuration): Establish and maintain secure configurations for enterprise assets and software. Remove unnecessary services, configure security settings.",
                "type": "best_practice",
                "source": "CIS Controls v8",
                "tags": ["cis", "hardening", "configuration"]
            },
            {
                "content": "CIS Control 5 (Account Management): Use strong authentication methods, implement MFA, regularly review and disable unnecessary accounts, audit privileged access.",
                "type": "best_practice",
                "source": "CIS Controls v8",
                "tags": ["cis", "identity", "authentication"]
            },
            {
                "content": "CIS Control 6 (Access Control Management): Implement least privilege principle, use separate accounts for different access levels, regularly review permissions.",
                "type": "best_practice",
                "source": "CIS Controls v8",
                "tags": ["cis", "access-control"]
            },
            {
                "content": "CIS Control 7 (Continuous Vulnerability Management): Establish automated vulnerability scanning, prioritize remediation based on risk, track remediation progress.",
                "type": "best_practice",
                "source": "CIS Controls v8",
                "tags": ["cis", "vulnerability-management"]
            },
            {
                "content": "CIS Control 8 (Audit Log Management): Collect audit logs for security events, centralize log collection, retain logs for at least 90 days, implement SIEM solution.",
                "type": "best_practice",
                "source": "CIS Controls v8",
                "tags": ["cis", "logging", "siem"]
            }
        ]

    @staticmethod
    def get_remediation_knowledge() -> List[Dict]:
        return [
            {
                "content": "SQL Injection Remediation: Use parameterized queries (prepared statements) in all database interactions. Never concatenate user input into SQL queries. Use ORM frameworks securely.",
                "type": "best_practice",
                "source": "OWASP Prevention Cheat Sheet",
                "tags": ["remediation", "sql-injection"]
            },
            {
                "content": "XSS Prevention: Encode all user-controlled data before output. Use Content Security Policy headers. Implement HTTPOnly and Secure flags on cookies.",
                "type": "best_practice",
                "source": "OWASP XSS Prevention",
                "tags": ["remediation", "xss"]
            },
            {
                "content": "CSRF Protection: Use anti-CSRF tokens in all state-changing requests. Implement SameSite cookie attribute. Verify origin/referer headers.",
                "type": "best_practice",
                "source": "OWASP CSRF Prevention",
                "tags": ["remediation", "csrf"]
            },
            {
                "content": "Authentication Hardening: Implement account lockout after failed attempts, use CAPTCHA for public-facing authentication, enforce strong passwords, enable MFA.",
                "type": "best_practice",
                "source": "OWASP Authentication Cheat Sheet",
                "tags": ["remediation", "authentication"]
            },
            {
                "content": "API Security: Use API keys or OAuth 2.0, implement rate limiting, validate all inputs, use HTTPS exclusively, implement proper CORS policies.",
                "type": "best_practice",
                "source": "OWASP API Security Top 10",
                "tags": ["remediation", "api-security"]
            },
            {
                "content": "Insecure Deserialization Fix: Avoid accepting serialized objects from untrusted sources. If necessary, implement integrity checks, use allow-lists, isolate deserialization code.",
                "type": "best_practice",
                "source": "OWASP Deserialization",
                "tags": ["remediation", "deserialization"]
            },
            {
                "content": "XXE Prevention: Disable XML external entity processing. Use less complex data formats like JSON. Implement input validation and sanitization.",
                "type": "best_practice",
                "source": "OWASP XXE Prevention",
                "tags": ["remediation", "xxe"]
            },
            {
                "content": "RCE Prevention: Never execute user-supplied input. Use safe APIs that don't invoke shell interpreters. Implement strict input validation and sandboxing.",
                "type": "best_practice",
                "source": "Security Best Practices",
                "tags": ["remediation", "rce"]
            }
        ]

    @staticmethod
    def get_security_patterns() -> List[Dict]:
        return [
            {
                "content": "Zero Trust Architecture: Never trust, always verify. Verify explicitly, use least privilege access, assume breach. Implement continuous verification.",
                "type": "best_practice",
                "source": "NIST SP 800-207",
                "tags": ["architecture", "zero-trust"]
            },
            {
                "content": "Defense in Depth: Implement multiple layers of security controls. No single point of failure. Combine preventive, detective, and corrective controls.",
                "type": "best_practice",
                "source": "Security Architecture",
                "tags": ["architecture", "defense-in-depth"]
            },
            {
                "content": "Principle of Least Privilege: Grant minimum access required for job function. Regularly review and revoke unnecessary permissions. Use just-in-time access.",
                "type": "best_practice",
                "source": "Security Fundamentals",
                "tags": ["access-control", "least-privilege"]
            },
            {
                "content": "Secure by Default: Systems should be secure in their default configuration. Security features enabled by default, unnecessary services disabled.",
                "type": "best_practice",
                "source": "Security Design Principles",
                "tags": ["design", "secure-defaults"]
            },
            {
                "content": "Fail Securely: When errors occur, fail to a secure state. Don't expose sensitive error information. Log security-relevant errors.",
                "type": "best_practice",
                "source": "Security Design Principles",
                "tags": ["design", "error-handling"]
            }
        ]

    @staticmethod
    def get_threat_actor_knowledge() -> List[Dict]:
        return [
            {
                "content": "APT29 (Cozy Bear): Russian state-sponsored group. Known for sophisticated phishing campaigns, targeting government and critical infrastructure. Uses WellMess, WellMail malware.",
                "type": "fact",
                "source": "MITRE Threat Groups",
                "tags": ["apt", "russia", "state-sponsored"]
            },
            {
                "content": "APT28 (Fancy Bear): Russian military intelligence group. Targets government, military, security organizations. Known for Zebrocy, X-Agent malware.",
                "type": "fact",
                "source": "MITRE Threat Groups",
                "tags": ["apt", "russia", "military"]
            },
            {
                "content": "Lazarus Group: North Korean state-sponsored APT. Known for financial cybercrime, WannaCry ransomware, SWIFT attacks. Targets financial institutions.",
                "type": "fact",
                "source": "MITRE Threat Groups",
                "tags": ["apt", "north-korea", "financial"]
            },
            {
                "content": "APT41: Chinese dual-espionage and financially-motivated group. Targets healthcare, telecom, technology sectors. Uses custom backdoors and ransomware.",
                "type": "fact",
                "source": "Mandiant Threat Intelligence",
                "tags": ["apt", "china", "dual-purpose"]
            },
            {
                "content": "Cl0p Ransomware Group: Financially motivated cybercriminal group. Known for exploiting zero-day vulnerabilities (MOVEit, GoAnywhere). Double extortion tactics.",
                "type": "fact",
                "source": "Threat Intelligence",
                "tags": ["ransomware", "cybercrime", "zero-day"]
            }
        ]

    @staticmethod
    def get_all_knowledge() -> List[Dict]:
        all_knowledge = []
        all_knowledge.extend(SecurityKnowledge.get_cve_knowledge())
        all_knowledge.extend(SecurityKnowledge.get_owasp_knowledge())
        all_knowledge.extend(SecurityKnowledge.get_mitre_attack_knowledge())
        all_knowledge.extend(SecurityKnowledge.get_nist_knowledge())
        all_knowledge.extend(SecurityKnowledge.get_cis_controls_knowledge())
        all_knowledge.extend(SecurityKnowledge.get_remediation_knowledge())
        all_knowledge.extend(SecurityKnowledge.get_security_patterns())
        all_knowledge.extend(SecurityKnowledge.get_threat_actor_knowledge())
        return all_knowledge

async def seed_knowledge_database(db_session):
    print("Seeding security knowledge database...")
    knowledge_items = SecurityKnowledge.get_all_knowledge()

    print(f"Total knowledge items to seed: {len(knowledge_items)}")

    for idx, item in enumerate(knowledge_items):
        try:
            embedding = vector_search_service.generate_embedding(item["content"])

            db_session.execute(
                """
                INSERT INTO knowledge_items (content, knowledge_type, source, tags, confidence, embedding)
                VALUES (:content, :type, :source, :tags, 1.0, :embedding)
                ON CONFLICT DO NOTHING
                """,
                {
                    "content": item["content"],
                    "type": item["type"],
                    "source": item["source"],
                    "tags": item["tags"],
                    "embedding": embedding
                }
            )

            if (idx + 1) % 10 == 0:
                print(f"Seeded {idx + 1}/{len(knowledge_items)} items...")
                db_session.commit()

        except Exception as e:
            print(f"ERROR seeding item {idx}: {e}")
            continue

    db_session.commit()
    print(f"Knowledge database seeded successfully with {len(knowledge_items)} items!")
