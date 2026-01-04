"use client";

import React, { useState, useRef, useEffect } from "react";
import { MessageSquare, Send, X, Shield, User, Bot, Loader2 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { apiClient } from "@/lib/api/client";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

function cn(...inputs: ClassValue[]) {
    return twMerge(clsx(inputs));
}

interface Message {
    role: "user" | "bot";
    content: string;
    audit_id?: string;
    feedback_submitted?: boolean;
}

export const ChatAssistant: React.FC = () => {
    const [isOpen, setIsOpen] = useState(false);
    const [input, setInput] = useState("");
    const [messages, setMessages] = useState<Message[]>([
        { role: "bot", content: "Identity verified. Security Operations Assistant online. How can I assist with your defense posture today?" }
    ]);
    const [isLoading, setIsLoading] = useState(false);
    const [mounted, setMounted] = useState(false);
    const [showCorrectionId, setShowCorrectionId] = useState<number | null>(null);
    const [correctionText, setCorrectionText] = useState("");
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        setMounted(true);
    }, []);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages]);

    if (!mounted) return null;

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMsg = input.trim();
        setInput("");
        setMessages(prev => [...prev, { role: "user", content: userMsg }]);
        setIsLoading(true);

        try {
            const { data } = await apiClient.post("/chat", { message: userMsg });
            // The audit_id would ideally come from the backend chat response
            // For now we simulate it if not present
            setMessages(prev => [...prev, {
                role: "bot",
                content: data.response,
                audit_id: data.audit_id || `audit-${Date.now()}`
            }]);
        } catch {
            setMessages(prev => [...prev, { role: "bot", content: "Error: Could not reach the Neural Link. Please check your connection." }]);
        } finally {
            setIsLoading(false);
        }
    };

    const submitFeedback = async (msgIndex: number, rating: number, correction?: string) => {
        const msg = messages[msgIndex];
        if (!msg.audit_id) return;

        try {
            await apiClient.post("/learning/feedback", {
                audit_id: msg.audit_id,
                rating,
                correction
            });

            const newMessages = [...messages];
            newMessages[msgIndex] = { ...msg, feedback_submitted: true };
            setMessages(newMessages);
            setShowCorrectionId(null);
            setCorrectionText("");
        } catch (err) {
            console.error("Failed to submit feedback", err);
        }
    };

    return (
        <>
            {/* Floating Toggle Button */}
            {!isOpen && (
                <motion.button
                    initial={{ scale: 0, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    whileHover={{ scale: 1.1 }}
                    whileTap={{ scale: 0.9 }}
                    onClick={() => setIsOpen(true)}
                    className="fixed bottom-24 right-8 z-40 p-4 bg-primary rounded-full shadow-2xl text-white"
                >
                    <MessageSquare className="w-6 h-6" />
                </motion.button>
            )}

            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ x: 400, opacity: 0 }}
                        animate={{ x: 0, opacity: 1 }}
                        exit={{ x: 400, opacity: 0 }}
                        className="fixed top-0 right-0 h-full w-[400px] z-50 glass border-l border-white/10 shadow-[0_0_50px_rgba(0,0,0,0.5)] flex flex-col"
                    >
                        {/* Header */}
                        <div className="p-6 border-b border-white/10 flex items-center justify-between bg-gradient-to-r from-primary/20 to-transparent">
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 rounded-xl bg-primary/20 flex items-center justify-center border border-primary/40">
                                    <Shield className="w-6 h-6 text-primary" />
                                </div>
                                <div>
                                    <h3 className="font-bold text-white leading-tight">Neural Link Chat</h3>
                                    <div className="flex items-center gap-1.5">
                                        <div className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
                                        <span className="text-[10px] uppercase tracking-wider text-foreground/40 font-bold">Encrypted Session</span>
                                    </div>
                                </div>
                            </div>
                            <button
                                onClick={() => setIsOpen(false)}
                                className="p-2 hover:bg-white/5 rounded-lg transition-colors"
                                aria-label="Close chat"
                            >
                                <X className="w-5 h-5 text-foreground/40" />
                            </button>
                        </div>

                        {/* Messages */}
                        <div
                            ref={scrollRef}
                            className="flex-1 overflow-y-auto p-6 space-y-6 scrollbar-hide"
                        >
                            {messages.map((msg, i) => (
                                <motion.div
                                    initial={{ opacity: 0, y: 10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    key={i}
                                    className="space-y-2"
                                >
                                    <div className={cn(
                                        "flex gap-3",
                                        msg.role === "user" ? "flex-row-reverse" : "flex-row"
                                    )}>
                                        <div className={cn(
                                            "w-8 h-8 rounded-lg flex items-center justify-center shrink-0 border",
                                            msg.role === "user"
                                                ? "bg-white/5 border-white/10"
                                                : "bg-primary/10 border-primary/20"
                                        )}>
                                            {msg.role === "user" ? <User className="w-4 h-4 text-foreground/60" /> : <Bot className="w-4 h-4 text-primary" />}
                                        </div>
                                        <div className={cn(
                                            "max-w-[80%] p-3 rounded-2xl text-sm leading-relaxed relative group",
                                            msg.role === "user"
                                                ? "bg-white/5 text-white rounded-tr-none"
                                                : "bg-primary/5 text-foreground/90 rounded-tl-none border border-primary/10"
                                        )}>
                                            {msg.content}

                                            {/* Feedback Actions */}
                                            {msg.role === "bot" && msg.audit_id && !msg.feedback_submitted && (
                                                <div className="absolute -bottom-6 left-0 flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity pt-1">
                                                    <button
                                                        onClick={() => submitFeedback(i, 5)}
                                                        className="p-1 hover:text-green-500 text-foreground/20 transition-colors"
                                                        title="Good response"
                                                    >
                                                        <Shield className="w-3 h-3" />
                                                    </button>
                                                    <button
                                                        onClick={() => setShowCorrectionId(i)}
                                                        className="p-1 hover:text-red-500 text-foreground/20 transition-colors"
                                                        title="Correction needed"
                                                    >
                                                        <X className="w-3 h-3" />
                                                    </button>
                                                </div>
                                            )}
                                        </div>
                                    </div>

                                    {/* Correction Input Area */}
                                    {showCorrectionId === i && (
                                        <motion.div
                                            initial={{ height: 0, opacity: 0 }}
                                            animate={{ height: "auto", opacity: 1 }}
                                            className="bg-red-500/5 border border-red-500/20 rounded-xl p-3 ml-11"
                                        >
                                            <p className="text-[10px] text-red-400 font-bold uppercase mb-2">Provide Correction</p>
                                            <textarea
                                                value={correctionText}
                                                onChange={(e) => setCorrectionText(e.target.value)}
                                                className="w-full bg-black/20 border border-white/5 rounded-lg p-2 text-xs text-white focus:outline-none focus:border-red-500/50 resize-none h-16"
                                                placeholder="Explain what's wrong or provide a correction..."
                                            />
                                            <div className="flex justify-end gap-2 mt-2">
                                                <button
                                                    onClick={() => setShowCorrectionId(null)}
                                                    className="px-2 py-1 text-[10px] text-foreground/40 hover:text-white"
                                                >
                                                    Cancel
                                                </button>
                                                <button
                                                    onClick={() => submitFeedback(i, 1, correctionText)}
                                                    className="px-3 py-1 bg-red-500/20 text-red-500 text-[10px] font-bold rounded-lg border border-red-500/20"
                                                >
                                                    Submit Improvement
                                                </button>
                                            </div>
                                        </motion.div>
                                    )}

                                    {msg.feedback_submitted && (
                                        <div className="ml-11 text-[10px] text-primary/60 font-medium flex items-center gap-1">
                                            <Shield className="w-2.5 h-2.5" />
                                            Feedback utilized in model refinement cycle.
                                        </div>
                                    )}
                                </motion.div>
                            ))}
                            {isLoading && (
                                <div className="flex gap-3">
                                    <div className="w-8 h-8 rounded-lg bg-primary/10 border border-primary/20 flex items-center justify-center">
                                        <Loader2 className="w-4 h-4 text-primary animate-spin" />
                                    </div>
                                    <div className="bg-primary/5 p-3 rounded-2xl rounded-tl-none border border-primary/10">
                                        <div className="flex gap-1">
                                            <span className="w-1.5 h-1.5 bg-primary/40 rounded-full animate-bounce [animation-delay:-0.3s]" />
                                            <span className="w-1.5 h-1.5 bg-primary/40 rounded-full animate-bounce [animation-delay:-0.15s]" />
                                            <span className="w-1.5 h-1.5 bg-primary/40 rounded-full animate-bounce" />
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* Input */}
                        <div className="p-6 bg-black/20 border-t border-white/10">
                            <div className="relative group">
                                <input
                                    type="text"
                                    value={input}
                                    onChange={(e) => setInput(e.target.value)}
                                    onKeyDown={(e) => e.key === "Enter" && handleSend()}
                                    placeholder="Ask about systems or vulnerabilities..."
                                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3 pr-12 text-sm focus:outline-none focus:border-primary/50 transition-all placeholder:text-foreground/20"
                                />
                                <button
                                    onClick={handleSend}
                                    disabled={!input.trim() || isLoading}
                                    className="absolute right-2 top-1/2 -translate-y-1/2 p-2 bg-primary/20 hover:bg-primary text-primary hover:text-white rounded-lg transition-all disabled:opacity-50 disabled:grayscale"
                                    aria-label="Send message"
                                >
                                    <Send className="w-4 h-4" />
                                </button>
                            </div>
                            <p className="mt-3 text-[10px] text-center text-foreground/20 italic">
                                Pillar 8: Human-in-the-loop learning active.
                            </p>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </>
    );
};
