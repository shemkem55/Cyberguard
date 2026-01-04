"use client";

import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
    ShieldAlert,
    ShieldCheck,
    Activity,
    Database,
    Cpu,
    Search,
    Bell,
    User,
    Zap,
    Lock,
    Terminal,
    BarChart3,
    FileDown
} from "lucide-react";
import { getAssets, getVulnerabilities, Asset, Vulnerability, apiClient } from "@/lib/api/client";
import { VoiceAssistant } from "@/components/voice/VoiceAssistant";
import { ChatAssistant } from "@/components/chat/ChatAssistant";
import { ScannerPanel } from "@/components/scanner/ScannerPanel";
import { AttackPathViewer } from "@/components/attack/AttackPathViewer";
import { ApprovalManager } from "@/components/approval/ApprovalManager";
import { WebPentestPanel } from "@/components/pentest/WebPentestPanel";
import KPIDashboard from "@/components/metrics/KPIDashboard";

export function DashboardLayout() {
    const [assets, setAssets] = useState<Asset[]>([]);
    const [vulnerabilities, setVulnerabilities] = useState<Vulnerability[]>([]);
    const [loading, setLoading] = useState(true);
    const [activeView, setActiveView] = useState<"overview" | "performance">("overview");

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [assetsData, vulnsData] = await Promise.all([
                    getAssets(),
                    getVulnerabilities()
                ]);
                setAssets(assetsData);
                setVulnerabilities(vulnsData);
            } catch (error) {
                console.error("Error fetching data:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    const generateReport = async () => {
        try {
            const { data } = await apiClient.get("/generate-report");
            const blob = new Blob([data.report], { type: "text/markdown" });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `CyberGuard_Report_${new Date().toISOString().split('T')[0]}.md`;
            a.click();
        } catch (error) {
            console.error("Failed to generate report:", error);
        }
    };

    return (
        <main className="min-h-screen p-6 md:p-12 relative overflow-hidden bg-background">
            {/* Background Glows */}
            <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary/20 rounded-full blur-[120px] pointer-events-none" />
            <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-accent/20 rounded-full blur-[120px] pointer-events-none" />

            {/* Navigation Header */}
            <nav className="flex items-center justify-between mb-12 glass p-4 rounded-2xl sticky top-6 z-50 backdrop-blur-xl">
                <div className="flex items-center gap-3">
                    <div className="p-2 bg-primary/10 rounded-xl">
                        <ShieldAlert className="w-8 h-8 text-primary animate-pulse" />
                    </div>
                    <span className="text-2xl font-bold tracking-tight gradient-text">CyberGuard-AI</span>
                </div>

                <div className="hidden md:flex items-center gap-8 text-sm font-medium text-foreground/60">
                    <button
                        onClick={() => setActiveView("overview")}
                        className={`hover:text-primary transition-colors ${activeView === 'overview' ? 'text-primary' : ''}`}
                    >
                        Overview
                    </button>
                    <button
                        onClick={() => setActiveView("performance")}
                        className={`hover:text-primary transition-colors ${activeView === 'performance' ? 'text-primary' : ''}`}
                    >
                        Performance
                    </button>
                    <a href="#" className="hover:text-primary transition-colors">Assets</a>
                    <a href="#" className="hover:text-primary transition-colors">Vulnerabilities</a>
                </div>

                <div className="flex items-center gap-4">
                    <button
                        onClick={generateReport}
                        className="hidden md:flex items-center gap-2 px-4 py-2 bg-primary/10 hover:bg-primary/20 border border-primary/20 rounded-xl text-xs font-bold text-primary transition-all"
                    >
                        <FileDown className="w-4 h-4" />
                        GENERATE REPORT
                    </button>
                    <div className="p-2 hover:bg-white/5 rounded-full cursor-pointer transition-colors">
                        <Search className="w-5 h-5" />
                    </div>
                    <div className="p-2 hover:bg-white/5 rounded-full cursor-pointer transition-colors relative">
                        <Bell className="w-5 h-5" />
                        <span className="absolute top-2 right-2 w-2 h-2 bg-destructive rounded-full" />
                    </div>
                    <div className="h-10 w-10 rounded-full bg-gradient-to-tr from-primary to-accent p-[2px]">
                        <div className="h-full w-full rounded-full bg-background flex items-center justify-center">
                            <User className="w-5 h-5" />
                        </div>
                    </div>
                </div>
            </nav>

            {/* Dashboard Content */}
            <AnimatePresence mode="wait">
                {activeView === "performance" ? (
                    <motion.div
                        key="performance"
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -20 }}
                        transition={{ duration: 0.3 }}
                    >
                        <KPIDashboard />
                    </motion.div>
                ) : (
                    <motion.div
                        key="overview"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: 20 }}
                        transition={{ duration: 0.3 }}
                    >
                        {/* Dash Stats Grid */}
                        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                            {[
                                { icon: <ShieldCheck className="text-success" />, label: "Security Score", value: "94/100", trend: "+2.4%" },
                                { icon: <ShieldAlert className="text-destructive" />, label: "Active Threats", value: vulnerabilities.length.toString(), trend: `${vulnerabilities.filter(v => v.severity > 7).length} severe` },
                                { icon: <Activity className="text-primary" />, label: "Sys Health", value: loading ? "..." : "Optimal", trend: "99.9% uptime" },
                                { icon: <Database className="text-accent" />, label: "Assets Scanned", value: assets.length.toString(), trend: "+0 new" },
                            ].map((stat, i) => (
                                <div
                                    key={i}
                                    className="glass p-6 rounded-2xl glass-hover cursor-pointer"
                                >
                                    <div className="flex items-start justify-between mb-4">
                                        <div className="p-2 bg-foreground/5 rounded-lg">{stat.icon}</div>
                                        <span className={`text-xs font-semibold px-2 py-1 rounded-full bg-foreground/5 ${stat.trend.startsWith('+') ? 'text-success' : 'text-foreground/40'}`}>
                                            {stat.trend}
                                        </span>
                                    </div>
                                    <p className="text-sm text-foreground/50 mb-1">{stat.label}</p>
                                    <h3 className="text-2xl font-bold">{stat.value}</h3>
                                </div>
                            ))}
                        </div>

                        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                            {/* Main Console */}
                            <div className="lg:col-span-2 space-y-6">
                                <div className="glass rounded-3xl p-8 relative overflow-hidden h-[400px]">
                                    <div className="flex items-center justify-between mb-8">
                                        <div>
                                            <h2 className="text-2xl font-bold mb-2">Vulnerability Map</h2>
                                            <p className="text-foreground/50 text-sm">Real-time visualization of network weaknesses</p>
                                        </div>
                                        <button
                                            onClick={() => window.location.reload()}
                                            className="px-4 py-2 bg-primary/10 text-primary rounded-xl text-sm font-bold hover:bg-primary/20 transition-all">
                                            Refresh
                                        </button>
                                    </div>

                                    {/* Visual Placeholder for Graph/Map */}
                                    <div className="w-full h-48 border-2 border-dashed border-border rounded-2xl flex items-center justify-center group cursor-crosshair">
                                        {loading ? (
                                            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
                                        ) : (
                                            <>
                                                <Terminal className="w-8 h-8 text-foreground/20 group-hover:text-primary transition-colors" />
                                                <span className="ml-3 text-foreground/20 group-hover:text-foreground/40 transition-colors uppercase tracking-widest text-xs font-bold">
                                                    {assets.length} Nodes Discovered
                                                </span>
                                            </>
                                        )}
                                    </div>

                                    <div className="mt-8 flex gap-4">
                                        <div className="flex-1 p-4 bg-foreground/5 rounded-xl border border-white/5">
                                            <p className="text-xs text-foreground/40 uppercase mb-2">Logic Engine</p>
                                            <div className="flex items-center gap-2">
                                                <Cpu className="w-4 h-4 text-primary" />
                                                <span className="text-sm font-mono tracking-tighter">Gemini-Pro-2.4</span>
                                            </div>
                                        </div>
                                        <div className="flex-1 p-4 bg-foreground/5 rounded-xl border border-white/5">
                                            <p className="text-xs text-foreground/40 uppercase mb-2">Assets</p>
                                            <div className="flex items-center gap-2">
                                                <Database className="w-4 h-4 text-warning" />
                                                <span className="text-sm font-mono tracking-tighter">{assets.length} Active</span>
                                            </div>
                                        </div>
                                        <div className="flex-1 p-4 bg-foreground/5 rounded-xl border border-white/5">
                                            <p className="text-xs text-foreground/40 uppercase mb-2">Protection</p>
                                            <div className="flex items-center gap-2">
                                                <Lock className="w-4 h-4 text-success" />
                                                <span className="text-sm font-mono tracking-tighter">Verified</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <div className="glass rounded-3xl p-8">
                                    <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                                        <BarChart3 className="w-5 h-5 text-primary" />
                                        Recent Vulnerabilities
                                    </h2>
                                    <div className="space-y-4">
                                        {loading ? (
                                            [1, 2, 3].map(i => <div key={i} className="h-16 w-full glass animate-pulse rounded-2xl" />)
                                        ) : vulnerabilities.length === 0 ? (
                                            <p className="text-foreground/40 text-center py-8">No vulnerabilities detected.</p>
                                        ) : (
                                            vulnerabilities.map((vuln, i) => (
                                                <div key={i} className="flex items-center justify-between p-4 bg-foreground/5 rounded-2xl border border-white/5 hover:border-primary/20 transition-all cursor-pointer">
                                                    <div className="flex items-center gap-4">
                                                        <div className={`w-2 h-2 rounded-full ${vuln.severity > 7 ? 'bg-destructive' : vuln.severity > 4 ? 'bg-warning' : 'bg-primary'}`} />
                                                        <div>
                                                            <p className="font-medium text-sm">{vuln.title}</p>
                                                            <p className="text-xs text-foreground/40">{vuln.cve_id} • Severity: {vuln.severity}</p>
                                                        </div>
                                                    </div>
                                                    <button className="text-xs font-bold text-primary hover:underline">Analyze</button>
                                                </div>
                                            ))
                                        )}
                                    </div>
                                </div>
                            </div>


                            {/* Sidebar */}
                            <div className="space-y-6">
                                <div className="glass rounded-3xl p-6">
                                    <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
                                        <Zap className="w-5 h-5 text-warning" />
                                        AI Recommendations
                                    </h2>
                                    <div className="space-y-4">
                                        <div className="p-4 bg-primary/10 rounded-2xl border border-primary/20">
                                            <p className="text-xs font-bold text-primary mb-1 uppercase tracking-wider">Critical Patch</p>
                                            <p className="text-sm font-medium mb-3">Update Nginx to 1.25.4 to mitigate CVE-2024-XXXXX</p>
                                            <button className="w-full py-2 bg-primary text-background rounded-xl text-xs font-bold">Apply Mitigation</button>
                                        </div>
                                        <div className="p-4 bg-accent/10 rounded-2xl border border-accent/20">
                                            <p className="text-xs font-bold text-accent mb-1 uppercase tracking-wider">Security Tip</p>
                                            <p className="text-sm font-medium">Implement MFA for 3 admin accounts with high privilege.</p>
                                            <button className="w-full py-2 border border-accent/20 text-accent rounded-xl text-xs font-bold hover:bg-accent/5">Remind Later</button>
                                        </div>
                                    </div>
                                </div>

                                {assets.length > 0 && (
                                    <div className="transition-all">
                                        <ScannerPanel assetId={assets[0].id} assetName={assets[0].name} />
                                    </div>
                                )}

                                <AttackPathViewer />
                                <ApprovalManager />
                                <WebPentestPanel />
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
            <VoiceAssistant />
            <ChatAssistant />
        </main>
    );
}
