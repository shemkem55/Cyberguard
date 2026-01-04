"use client";

import React, { useState } from "react";
import { Shield, Scan, CheckCircle, XCircle, Clock, Terminal, Wrench } from "lucide-react";
import { motion } from "framer-motion";
import { apiClient } from "@/lib/api/client";

interface ScanHistoryItem {
    id: number;
    scan_type: string;
    status: string;
    summary: string;
    performed_at: string;
}

interface ScanResult {
    status: "success" | "error";
    message?: string;
    os_version?: string;
    findings_count?: number;
    findings?: { cve_id: string; title: string; severity: number; description: string }[];
    services_found?: number;
    high_risk_services?: number;
}

interface ScannerPanelProps {
    assetId: number;
    assetName: string;
}

export const ScannerPanel: React.FC<ScannerPanelProps> = ({ assetId, assetName }) => {
    const [scanning, setScanning] = useState(false);
    const [scanResult, setScanResult] = useState<ScanResult | null>(null);
    const [history, setHistory] = useState<ScanHistoryItem[]>([]);
    const [showHistory, setShowHistory] = useState(false);

    const runOSScan = async () => {
        setScanning(true);
        setScanResult(null);

        try {
            const { data } = await apiClient.post(`/scan/os/${assetId}`);
            setScanResult(data);
            loadHistory();
        } catch (error) {
            console.error("Scan failed:", error);
            setScanResult({ status: "error", message: "Scan failed. Check backend logs." });
        } finally {
            setScanning(false);
        }
    };

    const runNetworkScan = async () => {
        setScanning(true);
        setScanResult(null);

        try {
            const { data } = await apiClient.post(`/scan/network/${assetId}`);
            setScanResult(data);
            loadHistory();
        } catch (error) {
            console.error("Network scan failed:", error);
            setScanResult({ status: "error", message: "Network scan failed. Check backend logs." });
        } finally {
            setScanning(false);
        }
    };

    const loadHistory = async () => {
        try {
            const { data } = await apiClient.get(`/scan/history/${assetId}`);
            setHistory(data);
            setShowHistory(true);
        } catch (error) {
            console.error("Failed to load history:", error);
        }
    };

    const requestRemediation = async (cveId: string, title: string) => {
        try {
            await apiClient.post("/approval/request", {
                request_type: "remediation",
                action: `Remediate ${cveId}`,
                target_asset_id: assetId,
                priority: "high",
                justification: `Automated remediation request for ${title}`,
                risk_assessment: "Standard automated patch application. Low risk as per pre-approved policy.",
                details: { cve_id: cveId }
            });
            alert(`Remediation request sent for ${cveId}`);
        } catch (error) {
            console.error("Failed to request remediation:", error);
            alert("Failed to send remediation request.");
        }
    };

    return (
        <div className="glass rounded-2xl p-6 border border-white/10">
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center border border-primary/20">
                        <Shield className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                        <h3 className="font-bold text-white">OS Scanner</h3>
                        <p className="text-xs text-foreground/40">Target: {assetName}</p>
                    </div>
                </div>

                <div className="flex items-center gap-2">
                    <button
                        onClick={runOSScan}
                        disabled={scanning}
                        className="px-3 py-2 bg-primary hover:bg-primary/80 disabled:bg-primary/20 text-white rounded-xl text-xs font-bold transition-all flex items-center gap-2"
                    >
                        {scanning ? (
                            <>
                                <div className="w-3 h-3 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                                Scanning...
                            </>
                        ) : (
                            <>
                                <Scan className="w-3 h-3" />
                                OS
                            </>
                        )}
                    </button>

                    <button
                        onClick={runNetworkScan}
                        disabled={scanning}
                        className="px-3 py-2 bg-secondary hover:bg-secondary/80 disabled:bg-secondary/20 text-white rounded-xl text-xs font-bold transition-all flex items-center gap-2"
                    >
                        {scanning ? (
                            <>
                                <div className="w-3 h-3 border-2 border-white/20 border-t-white rounded-full animate-spin" />
                                Scanning...
                            </>
                        ) : (
                            <>
                                <Terminal className="w-3 h-3" />
                                Network
                            </>
                        )}
                    </button>
                </div>
            </div>

            {scanResult && (
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className={`p-4 rounded-xl border ${scanResult.status === "success"
                        ? "bg-success/10 border-success/20"
                        : "bg-destructive/10 border-destructive/20"
                        }`}
                >
                    <div className="flex items-start gap-3">
                        {scanResult.status === "success" ? (
                            <CheckCircle className="w-5 h-5 text-success shrink-0 mt-0.5" />
                        ) : (
                            <XCircle className="w-5 h-5 text-destructive shrink-0 mt-0.5" />
                        )}
                        <div className="flex-1">
                            <p className="text-sm font-bold mb-1">
                                {scanResult.status === "success" ? "Scan Complete" : "Scan Failed"}
                            </p>
                            {scanResult.os_version && (
                                <div className="space-y-1 text-xs">
                                    <p><span className="text-foreground/40">OS:</span> {scanResult.os_version}</p>
                                    <p><span className="text-foreground/40">Findings:</span> {scanResult.findings_count} issues detected</p>

                                    {scanResult.findings && scanResult.findings.length > 0 && (
                                        <div className="mt-4 space-y-2">
                                            <p className="text-[10px] uppercase font-bold text-destructive tracking-wider">Vulnerabilities Detected</p>
                                            {scanResult.findings.map((vuln, i) => (
                                                <div key={i} className="p-3 bg-destructive/5 rounded-lg border border-destructive/20 flex items-center justify-between">
                                                    <div>
                                                        <div className="flex items-center gap-2">
                                                            <span className="font-mono font-bold text-destructive">{vuln.cve_id}</span>
                                                            <span className="text-[10px] px-1.5 py-0.5 rounded bg-destructive text-white font-bold">{vuln.severity}</span>
                                                        </div>
                                                        <p className="text-xs text-foreground/80 mt-1">{vuln.title}</p>
                                                    </div>
                                                    <button
                                                        onClick={() => requestRemediation(vuln.cve_id, vuln.title)}
                                                        className="px-3 py-1.5 bg-destructive hover:bg-destructive/80 text-white rounded-lg text-[10px] font-bold uppercase tracking-wider flex items-center gap-1.5 transition-all"
                                                    >
                                                        <Wrench className="w-3 h-3" />
                                                        Fix
                                                    </button>
                                                </div>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            )}
                            {scanResult.services_found !== undefined && (
                                <div className="space-y-1 text-xs">
                                    <p><span className="text-foreground/40">Services:</span> {scanResult.services_found} discovered</p>
                                    <p><span className="text-foreground/40">High Risk:</span> {scanResult.high_risk_services} services</p>
                                </div>
                            )}
                            {scanResult.message && (
                                <p className="text-xs text-foreground/60">{scanResult.message}</p>
                            )}
                        </div>
                    </div>
                </motion.div>
            )}

            {showHistory && history.length > 0 && (
                <div className="mt-6 pt-6 border-t border-white/10">
                    <div className="flex items-center gap-2 mb-4">
                        <Clock className="w-4 h-4 text-foreground/40" />
                        <h4 className="text-sm font-bold text-foreground/60 uppercase tracking-wider">Scan History</h4>
                    </div>
                    <div className="space-y-2">
                        {history.slice(0, 3).map((scan) => (
                            <div key={scan.id} className="p-3 bg-white/5 rounded-lg border border-white/5 text-xs">
                                <div className="flex items-center justify-between mb-1">
                                    <span className="font-mono text-primary">{scan.scan_type}</span>
                                    <span className="text-foreground/40">{new Date(scan.performed_at).toLocaleString()}</span>
                                </div>
                                <p className="text-foreground/60">{scan.summary}</p>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};
