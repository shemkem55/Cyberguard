"use client";

import React, { useState, useEffect, useRef, useCallback } from "react";
import { Mic, MicOff, Volume2, Command, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { apiClient } from "@/lib/api/client";

// Basic types for Web Speech API
interface SpeechRecognitionEvent {
    results: SpeechRecognitionResultList;
}

interface SpeechRecognitionResultList {
    length: number;
    item(index: number): SpeechRecognitionResult;
    [index: number]: SpeechRecognitionResult;
    // iterable iterator
    [Symbol.iterator](): IterableIterator<SpeechRecognitionResult>;
}

interface SpeechRecognitionResult {
    isFinal: boolean;
    length: number;
    item(index: number): SpeechRecognitionAlternative;
    [index: number]: SpeechRecognitionAlternative;
}

interface SpeechRecognitionAlternative {
    transcript: string;
    confidence: number;
}

interface SpeechRecognition extends EventTarget {
    continuous: boolean;
    interimResults: boolean;
    lang: string;
    onresult: ((event: SpeechRecognitionEvent) => void) | null;
    onend: (() => void) | null;
    onerror: ((event: any) => void) | null;
    start: () => void;
    stop: () => void;
    abort: () => void;
}

interface SpeechRecognitionWindow extends Window {
    SpeechRecognition?: { new(): SpeechRecognition };
    webkitSpeechRecognition?: { new(): SpeechRecognition };
}

export const VoiceAssistant: React.FC = () => {
    const [isListening, setIsListening] = useState(false);
    const [transcript, setTranscript] = useState("");
    const [response, setResponse] = useState("");
    const [isOpen, setIsOpen] = useState(false);
    const [mounted, setMounted] = useState(false);

    const recognitionRef = useRef<SpeechRecognition | null>(null);

    const speak = useCallback((text: string) => {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 0.9;
        utterance.pitch = 1.1;
        window.speechSynthesis.speak(utterance);
    }, []);

    const handleSendCommand = useCallback(async (text: string) => {
        try {
            const { data } = await apiClient.post("/voice-command", { command: text });
            // For now, let's assume Gemini returns the spoken text directly or within a JSON block
            // We'll clean up potential markdown JSON wrapping
            const cleanResponse = data.response.replace(/```json|```/g, "").trim();
            let spokenText = cleanResponse;

            try {
                const parsed = JSON.parse(cleanResponse);
                spokenText = parsed.speech_response;
            } catch {
                // fallback if not JSON
            }

            setResponse(spokenText);
            speak(spokenText);
        } catch (error) {
            console.error("Voice command error:", error);
            setResponse("I encountered an error processing your query.");
        }
    }, [speak]);

    useEffect(() => {
        setMounted(true);

        const win = window as unknown as SpeechRecognitionWindow;
        const SpeechRecognitionConstructor = win.SpeechRecognition || win.webkitSpeechRecognition;

        if (SpeechRecognitionConstructor) {
            recognitionRef.current = new SpeechRecognitionConstructor();
            if (recognitionRef.current) {
                recognitionRef.current.continuous = false;
                recognitionRef.current.interimResults = true;

                recognitionRef.current.onresult = (event: SpeechRecognitionEvent) => {
                    const currentTranscript = Array.from(event.results)
                        .map((result) => result[0])
                        .map((result) => result.transcript)
                        .join("");
                    setTranscript(currentTranscript);

                    if (event.results[0].isFinal) {
                        handleSendCommand(currentTranscript);
                    }
                };

                recognitionRef.current.onend = () => {
                    setIsListening(false);
                };
            }
        }
    }, [handleSendCommand]);

    const toggleListening = () => {
        if (isListening) {
            recognitionRef.current?.stop();
        } else {
            setTranscript("");
            setResponse("");
            recognitionRef.current?.start();
            setIsListening(true);
            if (!isOpen) setIsOpen(true);
        }
    };

    if (!mounted) return null;

    return (
        <>
            {/* Floating Action Button */}
            <motion.button
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={toggleListening}
                aria-label={isListening ? "Stop listening" : "Start listening"}
                className={`fixed bottom-8 right-8 z-50 p-4 rounded-full shadow-2xl transition-all ${isListening ? "bg-destructive animate-pulse" : "bg-primary"
                    }`}
            >
                {isListening ? <MicOff className="w-6 h-6 text-white" /> : <Mic className="w-6 h-6 text-white" />}
            </motion.button>

            {/* Assistant Modal */}
            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9, y: 20 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.9, y: 20 }}
                        className="fixed bottom-24 right-8 z-50 w-80 glass rounded-3xl p-6 overflow-hidden"
                    >
                        <div className="flex items-center justify-between mb-4">
                            <div className="flex items-center gap-2">
                                <Command className="w-4 h-4 text-primary" />
                                <span className="text-sm font-bold gradient-text uppercase tracking-widest">Neural Link</span>
                            </div>
                            <button
                                onClick={() => setIsOpen(false)}
                                aria-label="Close assistant"
                                className="text-foreground/40 hover:text-white"
                            >
                                <X className="w-4 h-4" />
                            </button>
                        </div>

                        <div className="space-y-4">
                            <div className="p-3 bg-white/5 rounded-xl border border-white/5 min-h-[60px]">
                                <p className="text-xs text-foreground/40 mb-1 uppercase">Analyst Input</p>
                                <p className="text-sm italic">
                                    {transcript || "Waiting for signal..."}
                                </p>
                            </div>

                            {response && (
                                <motion.div
                                    initial={{ opacity: 0, x: -10 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    className="p-3 bg-primary/10 rounded-xl border border-primary/20"
                                >
                                    <div className="flex items-center gap-2 mb-1">
                                        <Volume2 className="w-3 h-3 text-primary" />
                                        <p className="text-[10px] text-primary uppercase font-bold">CyberGuard Pulse</p>
                                    </div>
                                    <p className="text-sm">{response}</p>
                                </motion.div>
                            )}
                        </div>

                        {isListening && (
                            <div className="mt-4 flex justify-center gap-1">
                                {[1, 2, 3, 4, 5].map((i) => (
                                    <motion.div
                                        key={i}
                                        animate={{ height: [4, 12, 4] }}
                                        transition={{ repeat: Infinity, duration: 0.6, delay: i * 0.1 }}
                                        className="w-1 bg-primary rounded-full"
                                    />
                                ))}
                            </div>
                        )}
                    </motion.div>
                )}
            </AnimatePresence>
        </>
    );
};
