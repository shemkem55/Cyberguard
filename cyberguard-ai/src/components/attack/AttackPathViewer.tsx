"use client";

import React, { useState, useEffect } from "react";
import { Network, AlertTriangle, TrendingUp, Shield, ChevronRight } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { apiClient } from "@/lib/api/client";

interface AttackPath {
    id: number;
    name: string;
    description: string;
    entry_point: string;
    target: string;
    path_steps: Array<{
        step: number;
        action: string;
        asset: string;
        method: string;
        description: string;
    }>;
    exploited_vulnerabilities: string[];
    likelihood_score: number;
    impact_score: number;
    risk_score: number;
    mitigation_priority: number;
    status: string;
}

export const AttackPathViewer: React.FC = () => {
    const [paths, setPaths] = useState<AttackPath[]>([]);
    const [analyzing, setAnalyzing] = useState(false);
    const [selectedPath, setSelectedPath] = useState<AttackPath | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadPaths();
    }, []);

    const loadPaths = async () => {
        try {
            const { data } = await apiClient.get("/attack-paths");
            setPaths(data);
        } catch (error) {
            console.error("Failed to load attack paths:", error);
        } finally {
            setLoading(false);
        }
    };

    const runAnalysis = async () => {
        setAnalyzing(true);
        try {
            await apiClient.post("/analyze/attack-paths");
            await loadPaths();
        } catch (error) {
            console.error("Analysis failed:", error);
        } finally {
            setAnalyzing(false);
        }
    };

    const getRiskColor = (score: number) => {
        if (score >= 7) return "text-destructive";
        if (score >= 5) return "text-warning";
        return "text-primary";
    };

    const getRiskBg = (score: number) => {
        if (score >= 7) return "bg-destructive/10 border-destructive/20";
        if (score >= 5) return "bg-warning/10 border-warning/20";
        return "bg-primary/10 border-primary/20";
    };

    return (
        <div className="glass rounded-2xl p-6 border border-white/10">
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-destructive/10 flex items-center justify-center border border-destructive/20">
                        <Network className="w-6 h-6 text-destructive" />
                    </div>
                    <div>
                        <h3 className="font-bold text-white">Attack Path Analysis</h3>
                        <p className="text-xs text-foreground/40">
                            {paths.length} exploitation chains identified
                        </p>
                    </div>
                </div>

                <button
                    onClick={runAnalysis}
                    disabled={analyzing}
                    className="px-4 py-2 bg-destructive hover:bg-destructive/80 disabled:bg-destructive/20 text-white rounded-xl text-sm font-bold transition-all flex items-center gap-2"
                >
                    {analyzing ? (
                        <>
                            <div className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                            Analyzing...
                        </>
                    ) : (
                        <>
                            <TrendingUp className="w-4 h-4" />
                            Analyze Paths
                        </>
                    )}
                </button>
            </div>

            {loading ? (
                <div className="flex items-center justify-center py-12">
                    <div className="w-8 h-8 border-2 border-primary/20 border-t-primary rounded-full animate-spin" />
                </div>
            ) : paths.length === 0 ? (
                <div className="text-center py-12">
                    <Shield className="w-12 h-12 text-foreground/20 mx-auto mb-3" />
                    <p className="text-foreground/40 text-sm">No attack paths identified yet</p>
                    <p className="text-foreground/20 text-xs mt-1">Run analysis to discover potential threats</p>
                </div>
            ) : (
                <div className="space-y-3">
                    {paths.slice(0, 5).map((path) => (
                        <motion.div
                            key={path.id}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            className={`p-4 rounded-xl border cursor-pointer transition-all hover:border-white/20 ${getRiskBg(path.risk_score)}`}
                            onClick={() => setSelectedPath(path)}
                        >
                            <div className="flex items-start justify-between mb-2">
                                <div className="flex-1">
                                    <div className="flex items-center gap-2 mb-1">
                                        <AlertTriangle className={`w-4 h-4 ${getRiskColor(path.risk_score)}`} />
                                        <h4 className="font-bold text-sm">{path.name}</h4>
                                    </div>
                                    <p className="text-xs text-foreground/60 line-clamp-1">{path.description}</p>
                                </div>
                                <div className="flex items-center gap-2">
                                    <div className="text-right">
                                        <p className={`text-lg font-bold ${getRiskColor(path.risk_score)}`}>
                                            {path.risk_score.toFixed(1)}
                                        </p>
                                        <p className="text-[10px] text-foreground/40 uppercase">Risk</p>
                                    </div>
                                    <ChevronRight className="w-4 h-4 text-foreground/40" />
                                </div>
                            </div>

                            <div className="flex items-center gap-4 text-xs">
                                <span className="text-foreground/40">
                                    Priority: <span className="text-white font-bold">{path.mitigation_priority}</span>
                                </span>
                                <span className="text-foreground/40">
                                    CVEs: <span className="text-primary font-mono">{path.exploited_vulnerabilities.length}</span>
                                </span>
                                <span className="text-foreground/40">
                                    Steps: <span className="text-white">{path.path_steps.length}</span>
                                </span>
                            </div>
                        </motion.div>
                    ))}
                </div>
            )}

            {/* Attack Path Detail Modal */}
            <AnimatePresence>
                {selectedPath && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="fixed inset-0 z-50 flex items-center justify-center p-6 bg-black/80 backdrop-blur-sm"
                        onClick={() => setSelectedPath(null)}
                    >
                        <motion.div
                            initial={{ scale: 0.9, y: 20 }}
                            animate={{ scale: 1, y: 0 }}
                            exit={{ scale: 0.9, y: 20 }}
                            className="glass rounded-3xl p-8 max-w-2xl w-full max-h-[80vh] overflow-y-auto border border-white/10"
                            onClick={(e) => e.stopPropagation()}
                        >
                            <div className="flex items-start justify-between mb-6">
                                <div>
                                    <h2 className="text-2xl font-bold mb-2">{selectedPath.name}</h2>
                                    <p className="text-sm text-foreground/60">{selectedPath.description}</p>
                                </div>
                                <button
                                    onClick={() => setSelectedPath(null)}
                                    className="p-2 hover:bg-white/5 rounded-lg transition-colors"
                                >
                                    ✕
                                </button>
                            </div>

                            {/* Risk Metrics */}
                            <div className="grid grid-cols-3 gap-4 mb-6">
                                <div className="p-4 bg-white/5 rounded-xl border border-white/5">
                                    <p className="text-xs text-foreground/40 uppercase mb-1">Likelihood</p>
                                    <p className="text-2xl font-bold">{selectedPath.likelihood_score.toFixed(1)}</p>
                                </div>
                                <div className="p-4 bg-white/5 rounded-xl border border-white/5">
                                    <p className="text-xs text-foreground/40 uppercase mb-1">Impact</p>
                                    <p className="text-2xl font-bold">{selectedPath.impact_score.toFixed(1)}</p>
                                </div>
                                <div className={`p-4 rounded-xl border ${getRiskBg(selectedPath.risk_score)}`}>
                                    <p className="text-xs text-foreground/40 uppercase mb-1">Risk Score</p>
                                    <p className={`text-2xl font-bold ${getRiskColor(selectedPath.risk_score)}`}>
                                        {selectedPath.risk_score.toFixed(1)}
                                    </p>
                                </div>
                            </div>

                            {/* Attack Steps */}
                            <div className="mb-6">
                                <h3 className="text-sm font-bold uppercase tracking-wider text-foreground/60 mb-4">
                                    Exploitation Chain
                                </h3>
                                <div className="space-y-4">
                                    {selectedPath.path_steps.map((step, idx) => (
                                        <div key={idx} className="flex gap-4">
                                            <div className="flex flex-col items-center">
                                                <div className="w-8 h-8 rounded-full bg-primary/20 border-2 border-primary flex items-center justify-center text-xs font-bold">
                                                    {step.step}
                                                </div>
                                                {idx < selectedPath.path_steps.length - 1 && (
                                                    <div className="w-0.5 h-full bg-primary/20 my-1" />
                                                )}
                                            </div>
                                            <div className="flex-1 pb-4">
                                                <p className="font-bold text-sm mb-1">{step.action}</p>
                                                <p className="text-xs text-foreground/60 mb-2">{step.description}</p>
                                                <div className="flex items-center gap-2 text-xs">
                                                    <span className="text-foreground/40">Target:</span>
                                                    <span className="font-mono text-primary">{step.asset}</span>
                                                    <span className="text-foreground/40">•</span>
                                                    <span className="text-foreground/40">Method:</span>
                                                    <span className="text-warning">{step.method}</span>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* Exploited CVEs */}
                            <div>
                                <h3 className="text-sm font-bold uppercase tracking-wider text-foreground/60 mb-3">
                                    Exploited Vulnerabilities
                                </h3>
                                <div className="flex flex-wrap gap-2">
                                    {selectedPath.exploited_vulnerabilities.map((cve, idx) => (
                                        <span
                                            key={idx}
                                            className="px-3 py-1 bg-destructive/10 border border-destructive/20 rounded-lg text-xs font-mono text-destructive"
                                        >
                                            {cve}
                                        </span>
                                    ))}
                                </div>
                            </div>
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};
