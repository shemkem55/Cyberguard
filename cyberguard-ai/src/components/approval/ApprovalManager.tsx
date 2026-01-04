"use client";

import React, { useState, useEffect } from "react";
import { CheckCircle, XCircle, Clock, AlertCircle, User, FileText } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { apiClient } from "@/lib/api/client";

interface ApprovalRequest {
    id: number;
    request_type: string;
    action: string;
    target_asset: string | null;
    target_vulnerability: string | null;
    requester: string;
    approver: string | null;
    status: string;
    priority: string;
    justification: string;
    risk_assessment: string;
    details: Record<string, unknown>;
    created_at: string;
    reviewed_at: string | null;
    expires_at: string | null;
    approval_notes: string | null;
}

export const ApprovalManager: React.FC = () => {
    const [requests, setRequests] = useState<ApprovalRequest[]>([]);
    const [selectedRequest, setSelectedRequest] = useState<ApprovalRequest | null>(null);
    const [reviewNotes, setReviewNotes] = useState("");
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadRequests();
    }, []);

    const loadRequests = async () => {
        try {
            const { data } = await apiClient.get("/approval/requests");
            setRequests(data);
        } catch (error) {
            console.error("Failed to load approval requests:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleReview = async (requestId: number, decision: "approved" | "rejected") => {
        try {
            await apiClient.post(`/approval/${requestId}/review`, {
                decision,
                approver: "Security Admin",
                notes: reviewNotes
            });
            setSelectedRequest(null);
            setReviewNotes("");
            await loadRequests();
        } catch (error) {
            console.error("Review failed:", error);
        }
    };

    const getPriorityColor = (priority: string) => {
        switch (priority) {
            case "critical": return "text-destructive";
            case "high": return "text-warning";
            case "medium": return "text-primary";
            default: return "text-foreground/60";
        }
    };

    const getPriorityBg = (priority: string) => {
        switch (priority) {
            case "critical": return "bg-destructive/10 border-destructive/20";
            case "high": return "bg-warning/10 border-warning/20";
            case "medium": return "bg-primary/10 border-primary/20";
            default: return "bg-white/5 border-white/10";
        }
    };

    const getStatusIcon = (status: string) => {
        switch (status) {
            case "approved": return <CheckCircle className="w-4 h-4 text-success" />;
            case "rejected": return <XCircle className="w-4 h-4 text-destructive" />;
            case "pending": return <Clock className="w-4 h-4 text-warning animate-pulse" />;
            default: return <AlertCircle className="w-4 h-4 text-foreground/40" />;
        }
    };

    const pendingRequests = requests.filter(r => r.status === "pending");
    const reviewedRequests = requests.filter(r => r.status !== "pending");

    return (
        <div className="glass rounded-2xl p-6 border border-white/10">
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-warning/10 flex items-center justify-center border border-warning/20">
                        <FileText className="w-6 h-6 text-warning" />
                    </div>
                    <div>
                        <h3 className="font-bold text-white">Approval Requests</h3>
                        <p className="text-xs text-foreground/40">
                            {pendingRequests.length} pending authorization
                        </p>
                    </div>
                </div>

                <div className="flex items-center gap-2 text-xs">
                    <span className="px-2 py-1 bg-warning/10 border border-warning/20 rounded-lg text-warning font-bold">
                        {pendingRequests.length} Pending
                    </span>
                    <span className="px-2 py-1 bg-white/5 border border-white/10 rounded-lg text-foreground/60">
                        {reviewedRequests.length} Reviewed
                    </span>
                </div>
            </div>

            {loading ? (
                <div className="flex items-center justify-center py-12">
                    <div className="w-8 h-8 border-2 border-primary/20 border-t-primary rounded-full animate-spin" />
                </div>
            ) : requests.length === 0 ? (
                <div className="text-center py-12">
                    <CheckCircle className="w-12 h-12 text-success/40 mx-auto mb-3" />
                    <p className="text-foreground/40 text-sm">No approval requests</p>
                    <p className="text-foreground/20 text-xs mt-1">All operations are authorized</p>
                </div>
            ) : (
                <div className="space-y-4">
                    {/* Pending Requests */}
                    {pendingRequests.length > 0 && (
                        <div>
                            <h4 className="text-xs font-bold uppercase tracking-wider text-warning mb-3">
                                Awaiting Review
                            </h4>
                            <div className="space-y-2">
                                {pendingRequests.map((req) => (
                                    <motion.div
                                        key={req.id}
                                        initial={{ opacity: 0, x: -10 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        className={`p-4 rounded-xl border cursor-pointer transition-all hover:border-white/20 ${getPriorityBg(req.priority)}`}
                                        onClick={() => setSelectedRequest(req)}
                                    >
                                        <div className="flex items-start justify-between mb-2">
                                            <div className="flex-1">
                                                <div className="flex items-center gap-2 mb-1">
                                                    {getStatusIcon(req.status)}
                                                    <h5 className="font-bold text-sm">{req.action}</h5>
                                                    <span className={`text-[10px] uppercase font-bold ${getPriorityColor(req.priority)}`}>
                                                        {req.priority}
                                                    </span>
                                                </div>
                                                <p className="text-xs text-foreground/60 line-clamp-1">{req.justification}</p>
                                            </div>
                                        </div>

                                        <div className="flex items-center gap-4 text-xs text-foreground/40">
                                            <span>Type: <span className="text-white font-mono">{req.request_type}</span></span>
                                            {req.target_asset && (
                                                <span>Target: <span className="text-primary">{req.target_asset}</span></span>
                                            )}
                                            <span>By: <span className="text-white">{req.requester}</span></span>
                                        </div>
                                    </motion.div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Reviewed Requests */}
                    {reviewedRequests.length > 0 && (
                        <div>
                            <h4 className="text-xs font-bold uppercase tracking-wider text-foreground/40 mb-3">
                                Recently Reviewed
                            </h4>
                            <div className="space-y-2">
                                {reviewedRequests.slice(0, 3).map((req) => (
                                    <div
                                        key={req.id}
                                        className="p-3 bg-white/5 rounded-lg border border-white/5 text-xs"
                                    >
                                        <div className="flex items-center justify-between mb-1">
                                            <div className="flex items-center gap-2">
                                                {getStatusIcon(req.status)}
                                                <span className="font-bold">{req.action}</span>
                                            </div>
                                            <span className="text-foreground/40">
                                                {new Date(req.reviewed_at!).toLocaleDateString()}
                                            </span>
                                        </div>
                                        <p className="text-foreground/60">
                                            {req.status === "approved" ? "Approved" : "Rejected"} by {req.approver}
                                        </p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}

            {/* Review Modal */}
            <AnimatePresence>
                {selectedRequest && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="fixed inset-0 z-50 flex items-center justify-center p-6 bg-black/80 backdrop-blur-sm"
                        onClick={() => setSelectedRequest(null)}
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
                                    <div className="flex items-center gap-2 mb-2">
                                        <h2 className="text-2xl font-bold">{selectedRequest.action}</h2>
                                        <span className={`px-2 py-1 rounded-lg text-xs font-bold ${getPriorityBg(selectedRequest.priority)} ${getPriorityColor(selectedRequest.priority)}`}>
                                            {selectedRequest.priority}
                                        </span>
                                    </div>
                                    <p className="text-sm text-foreground/60">Request ID: #{selectedRequest.id}</p>
                                </div>
                                <button
                                    onClick={() => setSelectedRequest(null)}
                                    className="p-2 hover:bg-white/5 rounded-lg transition-colors"
                                >
                                    ✕
                                </button>
                            </div>

                            {/* Request Details */}
                            <div className="space-y-4 mb-6">
                                <div className="p-4 bg-white/5 rounded-xl border border-white/5">
                                    <p className="text-xs text-foreground/40 uppercase mb-2">Justification</p>
                                    <p className="text-sm">{selectedRequest.justification}</p>
                                </div>

                                <div className="p-4 bg-destructive/5 rounded-xl border border-destructive/10">
                                    <p className="text-xs text-destructive uppercase mb-2">Risk Assessment</p>
                                    <p className="text-sm text-foreground/80">{selectedRequest.risk_assessment}</p>
                                </div>

                                <div className="grid grid-cols-2 gap-4">
                                    <div className="p-4 bg-white/5 rounded-xl border border-white/5">
                                        <p className="text-xs text-foreground/40 uppercase mb-1">Request Type</p>
                                        <p className="text-sm font-mono">{selectedRequest.request_type}</p>
                                    </div>
                                    <div className="p-4 bg-white/5 rounded-xl border border-white/5">
                                        <p className="text-xs text-foreground/40 uppercase mb-1">Requester</p>
                                        <div className="flex items-center gap-2">
                                            <User className="w-3 h-3 text-primary" />
                                            <p className="text-sm">{selectedRequest.requester}</p>
                                        </div>
                                    </div>
                                </div>

                                {selectedRequest.target_asset && (
                                    <div className="p-4 bg-primary/5 rounded-xl border border-primary/10">
                                        <p className="text-xs text-primary uppercase mb-1">Target Asset</p>
                                        <p className="text-sm font-bold">{selectedRequest.target_asset}</p>
                                    </div>
                                )}
                            </div>

                            {/* Review Actions */}
                            {selectedRequest.status === "pending" && (
                                <div className="space-y-4">
                                    <div>
                                        <label className="text-xs text-foreground/60 uppercase mb-2 block">
                                            Approval Notes (Optional)
                                        </label>
                                        <textarea
                                            value={reviewNotes}
                                            onChange={(e) => setReviewNotes(e.target.value)}
                                            placeholder="Add comments or conditions..."
                                            className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-primary/50 transition-all placeholder:text-foreground/20 min-h-[80px]"
                                        />
                                    </div>

                                    <div className="flex gap-3">
                                        <button
                                            onClick={() => handleReview(selectedRequest.id, "approved")}
                                            className="flex-1 py-3 bg-success hover:bg-success/80 text-white rounded-xl font-bold transition-all flex items-center justify-center gap-2"
                                        >
                                            <CheckCircle className="w-5 h-5" />
                                            Approve Request
                                        </button>
                                        <button
                                            onClick={() => handleReview(selectedRequest.id, "rejected")}
                                            className="flex-1 py-3 bg-destructive hover:bg-destructive/80 text-white rounded-xl font-bold transition-all flex items-center justify-center gap-2"
                                        >
                                            <XCircle className="w-5 h-5" />
                                            Reject Request
                                        </button>
                                    </div>
                                </div>
                            )}
                        </motion.div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};
