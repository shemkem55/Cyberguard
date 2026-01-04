
"use client";

import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    TrendingUp,
    ShieldCheck,
    Zap,
    UserCheck,
    AlertTriangle,
    Lock,
    BarChart3,
    ChevronDown,
    Activity,
    Target
} from 'lucide-react';
import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    AreaChart,
    Area
} from 'recharts';
import axios from 'axios';

interface KPIData {
    reliability: {
        test_pass_rate: number;
        avg_accuracy_score: number;
        decision_reversal_rate: number;
    };
    safety: {
        safety_compliance: number;
        governance_compliance: number;
        blocked_attempts_count: number;
    };
    efficiency: {
        avg_response_time: number;
        total_automated_decisions: number;
        human_override_frequency: number;
    };
    trust: {
        user_trust_score: number;
        false_positive_rate: number;
    };
}

interface ActivityTrend {
    date: string;
    decisions: number;
    accuracy: number;
    safety_events: number;
}

const API_BASE = 'http://localhost:8000/api';

export default function KPIDashboard() {
    const [kpis, setKpis] = useState<KPIData | null>(null);
    const [activity, setActivity] = useState<ActivityTrend[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [kpiRes, activityRes] = await Promise.all([
                    axios.get(`${API_BASE}/metrics/kpis`),
                    axios.get(`${API_BASE}/metrics/activity?days=7`)
                ]);
                setKpis(kpiRes.data);
                setActivity(activityRes.data);
            } catch (err) {
                console.error("Failed to fetch metrics", err);
            } finally {
                setIsLoading(false);
            }
        };

        fetchData();
        const interval = setInterval(fetchData, 30000); // Refresh every 30s
        return () => clearInterval(interval);
    }, []);

    if (isLoading) {
        return (
            <div className="flex items-center justify-center h-full min-h-[400px]">
                <Activity className="w-8 h-8 text-primary animate-pulse" />
            </div>
        );
    }

    return (
        <div className="p-6 space-y-6 max-w-7xl mx-auto h-full overflow-y-auto no-scrollbar">
            {/* Header */}
            <header className="flex flex-col md:flex-row md:items-center justify-between gap-4 py-4">
                <div>
                    <h1 className="text-2xl font-bold text-foreground flex items-center gap-2">
                        <Target className="text-primary w-6 h-6" />
                        Performance Framework
                    </h1>
                    <p className="text-foreground/60 text-sm">Professional metrics & KPI analytics</p>
                </div>
                <div className="flex gap-2 text-xs font-medium">
                    <span className="px-3 py-1 rounded-full bg-primary/10 text-primary border border-primary/20">
                        Pillar 7 Enabled
                    </span>
                    <span className="px-3 py-1 rounded-full bg-green-500/10 text-green-500 border border-green-500/20">
                        Operational
                    </span>
                </div>
            </header>

            {/* Top Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <KPICard
                    title="System Accuracy"
                    value={`${kpis?.reliability.avg_accuracy_score}%`}
                    icon={ShieldCheck}
                    trend="+0.5%"
                    color="primary"
                    delay={0.1}
                />
                <KPICard
                    title="Safety Compliance"
                    value={`${kpis?.safety.safety_compliance}%`}
                    icon={Lock}
                    trend="Stable"
                    color="green"
                    delay={0.2}
                />
                <KPICard
                    title="User Trust"
                    value={`${kpis?.trust.user_trust_score}/5`}
                    icon={UserCheck}
                    trend="+0.2"
                    color="blue"
                    delay={0.3}
                />
                <KPICard
                    title="Automated Decisions"
                    value={kpis?.efficiency.total_automated_decisions.toString() || "0"}
                    icon={Zap}
                    trend="+12%"
                    color="purple"
                    delay={0.4}
                />
            </div>

            {/* Main Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Reliability & Accuracy Chart */}
                <div className="lg:col-span-2 glass-panel p-6 rounded-2xl border border-white/5 bg-black/20">
                    <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                        <TrendingUp className="w-5 h-5 text-primary" />
                        Operational Reliability Trends
                    </h3>
                    <div className="h-[300px] w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <AreaChart data={activity}>
                                <defs>
                                    <linearGradient id="colorAcc" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="var(--primary)" stopOpacity={0.3} />
                                        <stop offset="95%" stopColor="var(--primary)" stopOpacity={0} />
                                    </linearGradient>
                                </defs>
                                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" vertical={false} />
                                <XAxis
                                    dataKey="date"
                                    stroke="rgba(255,255,255,0.3)"
                                    fontSize={12}
                                    tickLine={false}
                                    axisLine={false}
                                />
                                <YAxis
                                    stroke="rgba(255,255,255,0.3)"
                                    fontSize={12}
                                    tickLine={false}
                                    axisLine={false}
                                />
                                <Tooltip
                                    contentStyle={{
                                        backgroundColor: '#121212',
                                        borderRadius: '12px',
                                        border: '1px solid rgba(255,255,255,0.1)',
                                        color: '#fff'
                                    }}
                                />
                                <Area
                                    type="monotone"
                                    dataKey="accuracy"
                                    stroke="var(--primary)"
                                    strokeWidth={3}
                                    fillOpacity={1}
                                    fill="url(#colorAcc)"
                                />
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Efficiency & Governance Details */}
                <div className="glass-panel p-6 rounded-2xl border border-white/5 bg-black/20 flex flex-col justify-between">
                    <div>
                        <h3 className="text-lg font-semibold mb-6 flex items-center gap-2">
                            <BarChart3 className="w-5 h-5 text-primary" />
                            Governance Metrics
                        </h3>
                        <div className="space-y-6">
                            <ProgressKPI
                                label="Risk Mitigation Rate"
                                value={kpis?.safety.governance_compliance || 0}
                                color="primary"
                            />
                            <ProgressKPI
                                label="Decision Autonomy"
                                value={100 - (kpis?.efficiency.human_override_frequency || 0)}
                                color="blue"
                            />
                            <ProgressKPI
                                label="Response Fidelity"
                                value={kpis?.reliability.test_pass_rate || 0}
                                color="green"
                            />
                        </div>
                    </div>

                    <div className="mt-8 pt-6 border-t border-white/5">
                        <div className="flex items-center justify-between text-sm">
                            <span className="text-foreground/40 font-medium uppercase tracking-wider text-[10px]">Security Incident Index</span>
                            <span className="text-green-500 font-mono">0.024</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Bottom Row - Audits & Overrides */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="glass-panel p-6 rounded-2xl border border-white/5 bg-black/20">
                    <h3 className="text-base font-semibold mb-4 flex items-center gap-2 text-foreground/80">
                        <AlertTriangle className="w-4 h-4 text-orange-500" />
                        Human Override Insight
                    </h3>
                    <p className="text-sm text-foreground/40 mb-4">
                        Frequency of AI decisions requiring manual intervention or approval.
                    </p>
                    <div className="flex items-end gap-3">
                        <span className="text-4xl font-bold text-foreground">
                            {kpis?.efficiency.human_override_frequency}%
                        </span>
                        <span className="text-xs text-orange-500 mb-2 flex items-center gap-1">
                            <ChevronDown className="w-3 h-3" /> 2.1% from last week
                        </span>
                    </div>
                </div>

                <div className="glass-panel p-6 rounded-2xl border border-white/5 bg-black/20">
                    <h3 className="text-base font-semibold mb-4 flex items-center gap-2 text-foreground/80">
                        <Zap className="w-4 h-4 text-primary" />
                        Platform Performance
                    </h3>
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <span className="text-xs text-foreground/30 block mb-1">Avg Response</span>
                            <span className="text-xl font-bold">{kpis?.efficiency.avg_response_time.toFixed(2)}s</span>
                        </div>
                        <div>
                            <span className="text-xs text-foreground/30 block mb-1">False Positives</span>
                            <span className="text-xl font-bold">{kpis?.trust.false_positive_rate}%</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

function KPICard({ title, value, icon: Icon, trend, color, delay }: {
    title: string, value: string, icon: any, trend: string, color: string, delay: number
}) {
    const colorClasses: Record<string, string> = {
        primary: "text-primary bg-primary/10",
        green: "text-green-500 bg-green-500/10",
        blue: "text-blue-500 bg-blue-500/10",
        purple: "text-purple-500 bg-purple-500/10",
    };

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay, duration: 0.5 }}
            className="glass-panel p-5 rounded-2xl border border-white/5 bg-black/20 hover:border-white/10 transition-all group"
        >
            <div className="flex justify-between items-start mb-4">
                <div className={`p-2 rounded-xl ${colorClasses[color]}`}>
                    <Icon size={20} />
                </div>
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${color === 'green' ? 'bg-green-500/10 text-green-500' : 'bg-primary/10 text-primary'}`}>
                    {trend}
                </span>
            </div>
            <h4 className="text-xs font-medium text-foreground/40 mb-1 group-hover:text-foreground/60 transition-colors uppercase tracking-wider">
                {title}
            </h4>
            <div className="text-2xl font-bold text-foreground">
                {value}
            </div>
        </motion.div>
    );
}

function ProgressKPI({ label, value, color }: { label: string, value: number, color: string }) {
    const barColors: Record<string, string> = {
        primary: "bg-primary",
        blue: "bg-blue-500",
        green: "bg-green-500",
    };

    return (
        <div className="space-y-2">
            <div className="flex justify-between text-xs font-medium">
                <span className="text-foreground/60">{label}</span>
                <span className="text-foreground">{value}%</span>
            </div>
            <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                <motion.div
                    initial={{ width: 0 }}
                    animate={{ width: `${value}%` }}
                    transition={{ duration: 1, ease: "easeOut" }}
                    className={`h-full ${barColors[color]}`}
                />
            </div>
        </div>
    );
}
