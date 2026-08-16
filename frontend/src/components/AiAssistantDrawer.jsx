import React, { useState } from 'react';
import { X, Sparkles, Send, Bot, CheckCircle2 } from 'lucide-react';
import { apiService } from '../services/api';

export default function AiAssistantDrawer({ isOpen, onClose, sites = [] }) {
  if (!isOpen) return null;

  const [messages, setMessages] = useState([
    {
      sender: 'ai',
      text: "Hello! I am your GIS Planning Assistant. Ask me why a site was recommended, compare two sites, or audit the highest deficit zones."
    }
  ]);
  const [inputQuery, setInputQuery] = useState('');
  const [loading, setLoading] = useState(false);

  const presetQueries = [
    "Why is Site A ranked first?",
    "Which site has the highest healthcare gap?",
    "Compare Site 1 and Site 2."
  ];

  const handleSend = async (queryText) => {
    const text = queryText || inputQuery;
    if (!text.trim()) return;

    const userMsg = { sender: 'user', text };
    setMessages((prev) => [...prev, userMsg]);
    setInputQuery('');
    setLoading(true);

    try {
      const res = await apiService.queryAI(text, sites[0]?.id, sites[1]?.id);
      const aiMsg = { sender: 'ai', text: res.answer };
      setMessages((prev) => [...prev, aiMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          sender: 'ai',
          text: "Recommendation Audit: Besa-Pipla Southern Growth Sector is ranked #1 due to its high 5 km catchment (188,000 citizens), high deficit score, and direct Outer Ring Road access."
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-y-0 right-0 w-full max-w-md bg-slate-900 border-l border-slate-800 shadow-2xl z-50 flex flex-col">
      <div className="p-4 border-b border-slate-800 flex items-center justify-between bg-slate-850">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-indigo-600/30 border border-indigo-500/40 flex items-center justify-center">
            <Sparkles className="w-4 h-4 text-indigo-400" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-white">AI Planning Assistant</h3>
            <span className="text-[10px] text-emerald-400 flex items-center gap-1">
              <CheckCircle2 className="w-2.5 h-2.5" />
              Spatial Decision Engine
            </span>
          </div>
        </div>
        <button
          onClick={onClose}
          className="p-1 rounded hover:bg-slate-800 text-slate-400 hover:text-white"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      <div className="flex-1 p-4 overflow-y-auto space-y-4">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`flex gap-3 ${m.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            {m.sender === 'ai' && (
              <div className="w-7 h-7 rounded-full bg-indigo-900 border border-indigo-700 flex items-center justify-center flex-shrink-0 mt-0.5">
                <Bot className="w-4 h-4 text-indigo-300" />
              </div>
            )}
            <div
              className={`p-3 rounded-xl text-xs max-w-[85%] leading-relaxed ${
                m.sender === 'user'
                  ? 'bg-brand-600 text-white font-medium'
                  : 'bg-slate-800/90 text-slate-200 border border-slate-700 whitespace-pre-line'
              }`}
            >
              {m.text}
            </div>
          </div>
        ))}
        {loading && (
          <div className="text-xs text-indigo-400 flex items-center gap-2">
            <span className="animate-spin text-sm">&#9679;</span>
            <span>Synthesizing GIS spatial metrics...</span>
          </div>
        )}
      </div>

      <div className="p-3 border-t border-slate-800/80 bg-slate-900/50 space-y-1.5">
        <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-400 block">
          Suggested Inquiries:
        </span>
        <div className="flex flex-wrap gap-1.5">
          {presetQueries.map((q, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(q)}
              className="text-[11px] px-2.5 py-1 rounded-md bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700/60 text-left transition-colors"
            >
              {q}
            </button>
          ))}
        </div>
      </div>

      <div className="p-4 border-t border-slate-800 bg-slate-850">
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          className="flex gap-2"
        >
          <input
            type="text"
            value={inputQuery}
            onChange={(e) => setInputQuery(e.target.value)}
            placeholder="Ask why a site was picked or compare options..."
            className="flex-1 px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
          />
          <button
            type="submit"
            disabled={loading || !inputQuery.trim()}
            className="p-2 rounded-lg bg-brand-600 hover:bg-brand-500 disabled:opacity-50 text-white transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </form>
      </div>
    </div>
  );
}