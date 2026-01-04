"use client";

import React, { useState, useRef, useEffect } from "react";
import { Send, Menu, Plus, MessageSquare, User, Terminal, Loader2, LayoutDashboard } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { apiClient } from "@/lib/api/client";

interface Message {
    role: "user" | "bot";
    content: string;
}

interface ChatSession {
    id: number;
    title: string;
    created_at: string;
}

interface FullScreenChatProps {
    onSwitchToDashboard: () => void;
}

// Basic Typing Effect Component
const TypingMessage = ({ content, onTyping }: { content: string; onTyping?: () => void }) => {
    const [displayedContent, setDisplayedContent] = useState("");
    const onTypingRef = useRef(onTyping);

    useEffect(() => {
        onTypingRef.current = onTyping;
    }, [onTyping]);

    useEffect(() => {
        let index = 0;
        const interval = setInterval(() => {
            setDisplayedContent((prev) => {
                // Determine next content
                const next = content.slice(0, index + 1);
                return next;
            });
            index++;

            if (onTypingRef.current) {
                onTypingRef.current();
            }

            if (index > content.length) {
                clearInterval(interval);
            }
        }, 15);

        return () => clearInterval(interval);
    }, [content]); // Removed onTyping from dependency

    return (
        <div className="prose prose-invert prose-sm max-w-none leading-relaxed text-foreground/90 whitespace-pre-wrap">
            {displayedContent}
        </div>
    );
};

export const FullScreenChat: React.FC<FullScreenChatProps> = ({ onSwitchToDashboard }) => {
    const [messages, setMessages] = useState<Message[]>([
        { role: "bot", content: "I am CyberGuard, your AI security architect. How can I assist you with your infrastructure today?" }
    ]);
    const [input, setInput] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [sidebarOpen, setSidebarOpen] = useState(true);
    const [sessionId, setSessionId] = useState<number | null>(null);
    const [sessions, setSessions] = useState<ChatSession[]>([]);
    const [userRole, setUserRole] = useState<"Analyst" | "Executive" | "Engineer">("Analyst");
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        loadSessions();
    }, []);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages, isLoading]);

    const loadSessions = async () => {
        try {
            const { data } = await apiClient.get("/chat/sessions");
            setSessions(data);
        } catch (error) {
            console.error("Failed to load sessions", error);
        }
    };

    const loadHistory = async (id: number) => {
        try {
            setSessionId(id);
            const { data } = await apiClient.get(`/chat/session/${id}`);
            setMessages(data.map((m: any) => ({ role: m.role, content: m.content })));
            if (window.innerWidth < 640) setSidebarOpen(false);
        } catch (error) {
            console.error("Failed to load history", error);
        }
    };

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMsg = input.trim();
        setInput("");
        setMessages(prev => [...prev, { role: "user", content: userMsg }]);
        setIsLoading(true);

        try {
            const { data } = await apiClient.post("/chat", {
                message: userMsg,
                session_id: sessionId,
                user_role: userRole
            });

            setMessages(prev => [...prev, { role: "bot", content: data.response }]);

            if (!sessionId && data.session_id) {
                setSessionId(data.session_id);
                loadSessions(); // Refresh sidebar to show new chat
            }
        } catch {
            setMessages(prev => [...prev, { role: "bot", content: "Error: Could not reach the Neural Link. Please check your connection." }]);
        } finally {
            setIsLoading(false);
        }
    };

    const clearChat = () => {
        setMessages([{ role: "bot", content: "I am CyberGuard, your AI security architect. How can I assist you with your infrastructure today?" }]);
        setSessionId(null);
    };

    return (
        <div className="flex h-screen bg-background text-foreground font-sans overflow-hidden cyber-grid relative">
            {/* Background Glows (matching Dashboard) */}
            <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary/20 rounded-full blur-[120px] pointer-events-none" />
            <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-accent/20 rounded-full blur-[120px] pointer-events-none" />

            {/* Sidebar - CyberGuard Style */}
            <AnimatePresence mode="wait">
                {sidebarOpen && (
                    <motion.div
                        initial={{ width: 0, opacity: 0 }}
                        animate={{ width: 280, opacity: 1 }}
                        exit={{ width: 0, opacity: 0 }}
                        className="glass border-r border-white/10 flex flex-col h-full relative z-20 shrink-0 backdrop-blur-xl"
                        key="sidebar"
                    >
                        <div className="p-4 border-b border-white/10">
                            <div className="flex items-center gap-2 mb-4">
                                <div className="w-8 h-8 rounded-lg bg-primary/20 flex items-center justify-center border border-primary/50">
                                    <Terminal className="w-5 h-5 text-primary" />
                                </div>
                                <span className="font-bold text-lg tracking-tight gradient-text">CyberGuard</span>
                            </div>
                            <button
                                onClick={clearChat}
                                className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl border border-primary/20 bg-primary/10 hover:bg-primary/20 transition-all text-sm font-medium text-primary hover:text-white hover:shadow-[0_0_15px_rgba(56,189,248,0.3)]"
                            >
                                <Plus className="w-4 h-4" />
                                New Session
                            </button>
                        </div>

                        <div className="flex-1 overflow-y-auto px-3 py-4 space-y-1 scrollbar-thin scrollbar-thumb-white/10">
                            <div className="text-xs font-bold text-foreground/40 uppercase tracking-wider mb-3 px-2">History</div>
                            {sessions.map((session) => (
                                <div
                                    key={session.id}
                                    onClick={() => loadHistory(session.id)}
                                    className={`flex items-center gap-3 px-3 py-2.5 rounded-lg cursor-pointer text-sm transition-colors truncate group border border-transparent ${sessionId === session.id ? "bg-white/10 border-white/5 text-primary" : "hover:bg-white/5 text-foreground/80 hover:border-white/5"}`}
                                >
                                    <MessageSquare className={`w-4 h-4 ${sessionId === session.id ? "text-primary" : "text-foreground/40 group-hover:text-primary"} transition-colors`} />
                                    <span className="truncate">{session.title || "New Chat"}</span>
                                </div>
                            ))}
                        </div>

                        <div className="border-t border-white/10 p-4 space-y-4">
                            {/* Role Selector */}
                            <div className="space-y-2">
                                <label className="text-[10px] uppercase tracking-wider text-foreground/40 font-bold px-1">Simulate Role</label>
                                <div className="flex bg-black/20 p-1 rounded-lg border border-white/10">
                                    {(["Analyst", "Executive", "Engineer"] as const).map((role) => (
                                        <button
                                            key={role}
                                            onClick={() => setUserRole(role)}
                                            className={`flex-1 text-[10px] py-1.5 rounded-md transition-all font-medium ${userRole === role ? "bg-primary/20 text-primary border border-primary/30 shadow-[0_0_10px_rgba(56,189,248,0.15)]" : "text-foreground/40 hover:text-foreground/60"}`}
                                        >
                                            {role}
                                        </button>
                                    ))}
                                </div>
                            </div>

                            <button
                                onClick={onSwitchToDashboard}
                                className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-white/5 transition-colors text-sm text-foreground/80 font-medium group"
                            >
                                <LayoutDashboard className="w-4 h-4 text-foreground/40 group-hover:text-primary transition-colors" />
                                Open Dashboard
                            </button>

                            <div className="flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-white/5 cursor-pointer text-sm text-foreground transition-colors border border-transparent hover:border-white/10">
                                <div className="w-6 h-6 rounded-full bg-gradient-to-tr from-primary to-accent p-[1px]">
                                    <div className="w-full h-full rounded-full bg-black flex items-center justify-center">
                                        <User className="w-3 h-3 text-white" />
                                    </div>
                                </div>
                                <div className="flex flex-col">
                                    <span className="font-medium text-xs leading-none">Overlord55</span>
                                    <span className="text-[10px] text-foreground/40 leading-none mt-1">Admin</span>
                                </div>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Main Chat Area */}
            <div className="flex-1 flex flex-col relative h-full">
                {/* Top Mobile Bar / Toggle */}
                <div className="h-14 flex items-center px-4 absolute top-0 left-0 w-full z-10 sm:hidden bg-background/80 backdrop-blur-md border-b border-white/10">
                    <button onClick={() => setSidebarOpen(!sidebarOpen)} className="p-2 text-foreground/60" title="Toggle Sidebar" aria-label="Toggle Sidebar">
                        <Menu className="w-6 h-6" />
                    </button>
                    <span className="ml-2 font-bold gradient-text">CyberGuard AI</span>
                </div>

                {!sidebarOpen && (
                    <button
                        onClick={() => setSidebarOpen(true)}
                        className="absolute top-4 left-4 p-2.5 rounded-xl bg-black/40 border border-white/10 hover:bg-white/10 text-foreground/60 transition-all z-10 hidden sm:block backdrop-blur"
                        title="Open Sidebar"
                        aria-label="Open Sidebar"
                    >
                        <Menu className="w-5 h-5" />
                    </button>
                )}

                {/* Messages */}
                <div className="flex-1 overflow-y-auto w-full scrollbar-transparent" ref={scrollRef}>
                    <div className="flex flex-col min-h-full pb-36 pt-14 sm:pt-0 max-w-4xl mx-auto w-full">
                        {messages.map((msg, idx) => (
                            <div
                                key={idx}
                                className={`w-full px-4 py-8 border-b border-white/5 ${msg.role === 'bot' ? 'bg-white/[0.02]' : 'bg-transparent'
                                    }`}
                            >
                                <div className="flex gap-4 md:gap-6 w-full max-w-3xl mx-auto">
                                    <div className="flex-shrink-0 flex flex-col relative items-end">
                                        <div className="w-8 h-8">
                                            {msg.role === 'bot' ? (
                                                <div className="w-8 h-8 rounded-lg bg-primary/20 border border-primary/40 flex items-center justify-center shadow-[0_0_15px_rgba(56,189,248,0.2)]">
                                                    <Terminal className="w-4 h-4 text-primary" />
                                                </div>
                                            ) : (
                                                <div className="w-8 h-8 rounded-lg bg-white/10 border border-white/20 flex items-center justify-center">
                                                    <User className="w-4 h-4 text-foreground" />
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                    <div className="relative flex-1 overflow-hidden break-words">
                                        {msg.role === 'bot' && idx === messages.length - 1 && !isLoading ? (
                                            <TypingMessage
                                                content={msg.content}
                                                onTyping={() => {
                                                    if (scrollRef.current) {
                                                        scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
                                                    }
                                                }}
                                            />
                                        ) : (
                                            <div className="prose prose-invert prose-sm max-w-none leading-relaxed text-foreground/90 whitespace-pre-wrap">
                                                {msg.content}
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        ))}

                        {isLoading && (
                            <div className="w-full px-4 py-8 border-b border-white/5 bg-white/[0.02]">
                                <div className="flex gap-4 md:gap-6 w-full max-w-3xl mx-auto">
                                    <div className="w-8 h-8">
                                        <div className="w-8 h-8 rounded-lg bg-primary/20 border border-primary/40 flex items-center justify-center">
                                            <Loader2 className="w-4 h-4 text-primary animate-spin" />
                                        </div>
                                    </div>
                                    <div className="flex items-center gap-1.5 pt-2">
                                        <div className="w-1.5 h-1.5 bg-primary rounded-full animate-bounce [animation-delay:-0.3s]" />
                                        <div className="w-1.5 h-1.5 bg-primary rounded-full animate-bounce [animation-delay:-0.15s]" />
                                        <div className="w-1.5 h-1.5 bg-primary rounded-full animate-bounce" />
                                    </div>
                                </div>
                            </div>
                        )}

                        <div className="h-32 flex-shrink-0" />
                    </div>
                </div>

                {/* Input Area */}
                <div className="absolute bottom-0 left-0 w-full bg-gradient-to-t from-background via-background/90 to-transparent pt-12 pb-8 px-4">
                    <div className="max-w-3xl mx-auto w-full">
                        <div className="relative flex h-full flex-1 items-stretch md:flex-col group">
                            <div className="relative flex flex-col w-full flex-grow p-3 bg-black/40 backdrop-blur-xl border border-white/10 text-foreground rounded-2xl shadow-2xl overflow-hidden focus-within:border-primary/50 focus-within:ring-1 focus-within:ring-primary/50 transition-all">
                                <textarea
                                    value={input}
                                    onChange={(e) => setInput(e.target.value)}
                                    onKeyDown={(e) => {
                                        if (e.key === 'Enter' && !e.shiftKey) {
                                            e.preventDefault();
                                            handleSend();
                                        }
                                    }}
                                    placeholder="Send a command to CyberGuard..."
                                    className="m-0 w-full resize-none border-0 bg-transparent p-0 pr-10 focus:ring-0 focus-visible:ring-0 md:pr-12 pl-2 h-[24px] max-h-[200px] overflow-y-hidden text-sm leading-6 placeholder:text-foreground/30 outline-none font-medium"
                                />
                                <button
                                    onClick={handleSend}
                                    disabled={!input.trim() || isLoading}
                                    title="Send Message"
                                    aria-label="Send Message"
                                    className="absolute md:bottom-2.5 md:right-3 right-2 bottom-2 p-1.5 rounded-lg text-foreground/40 hover:bg-primary hover:text-white disabled:hover:bg-transparent disabled:opacity-30 transition-all"
                                >
                                    <Send className="w-4 h-4" />
                                </button>
                            </div>
                            <div className="text-center text-[10px] text-foreground/30 mt-3 font-medium tracking-wide uppercase">
                                AI-Driven Security Operations • Authorized Personnel Only
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
