
export interface WebTarget {
    id: number;
    domain: string;
    root_url: string;
    scope_description: string;
    authorized: boolean;
    created_at: string;
    tech_stack?: any;
}

export interface PentestSession {
    id: number;
    target_id: number;
    status: string;
    start_time: string;
    end_time?: string;
    findings_summary?: any;
}

export interface WebFinding {
    id: number;
    session_id: number;
    title: string;
    url: string;
    severity: string;
    description: string;
    evidence: string;
    remediation_advice: string;
    confirmed_by_validation: boolean;
}
