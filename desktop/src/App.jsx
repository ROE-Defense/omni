import React, { useState, useEffect, useRef } from 'react';
import { Terminal, Brain, Layers, Activity, Send, Play, FileCode, CheckCircle, Download, RefreshCw, BarChart2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import NeuralBrain from './components/NeuralBrain';

const API_URL = "http://127.0.0.1:8000";

const HighlightCode = ({ code }) => {
    // NEON OVERDRIVE PALETTE
    const html = code
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/(#.*)/g, '<span style="color:#7F8C8D; font-style:italic;">$1</span>')
        .replace(/('.*?'|".*?")/g, '<span style="color:#FFFF00;">$1</span>')
        .replace(/(@\w+)/g, '<span style="color:#BF00FF;">$1</span>')
        .replace(/\b(import|from|def|class|return|if|else|elif|while|for|in|try|except|with|as|pass|break|continue|global|lambda|yield|await|async)\b/g, '<span style="color:#FF00FF; font-weight:bold; text-shadow: 0 0 5px #FF00FFaa;">$1</span>')
        .replace(/(\w+)(?=\()/g, '<span style="color:#00FFFF; text-shadow: 0 0 2px #00FFFFaa;">$1</span>')
        .replace(/\b(self|print|len|range|open|int|str|float|list|dict|set|tuple|super)\b/g, '<span style="color:#FF9900;">$1</span>')
        .replace(/\b(\d+)\b/g, '<span style="color:#FF3333;">$1</span>')
        .replace(/([=+\-*/%<>!&|^]+)/g, '<span style="color:#00FF9D;">$1</span>')
        .replace(/\b([A-Z_][A-Z0-9_]+)\b/g, '<span style="color:#FFD700;">$1</span>');
        
    return <div dangerouslySetInnerHTML={{ __html: html }} />;
};

function App() {
  const [activeTab, setActiveTab] = useState('chat');
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [artifacts, setArtifacts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('Idle');
  const [activeBrain, setActiveBrain] = useState('Base Brain');
  const [brains, setBrains] = useState({ installed: [], available: [] });
  
  const [locSession, setLocSession] = useState(0);
  const [locTotal, setLocTotal] = useState(12430); 
  const [streamingCode, setStreamingCode] = useState('');
  const [isCodeMode, setIsCodeMode] = useState(false);

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const refreshBrains = () => {
    fetch(`${API_URL}/brains`)
      .then(res => res.json())
      .then(data => setBrains(data))
      .catch(err => console.error("API Offline", err));
  };

  useEffect(() => { refreshBrains(); }, []);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = { role: 'user', content: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);
    setStatus('Thinking...');
    
    setStreamingCode('');
    setIsCodeMode(false);
    let codeMode = false;

    // Brain Routing (Visual Placeholder, backend handles real routing now)
    // if (input.toLowerCase().includes('snake')) setActiveBrain('@roe/backend');

    setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

    const ws = new WebSocket(`ws://127.0.0.1:8000/ws/chat`);
    
    ws.onopen = () => {
        ws.send(JSON.stringify({ message: userMsg.content, brain: activeBrain }));
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.type === 'token') {
            const token = data.content;
            if (token.includes('```')) {
                codeMode = !codeMode;
                setIsCodeMode(codeMode);
                return; 
            }

            if (codeMode) {
                setStreamingCode(prev => prev + token);
                setLocSession(prev => prev + (token.match(/\n/g) || []).length);
            } else {
                setMessages(prev => {
                    const newHistory = [...prev];
                    const lastIndex = newHistory.length - 1;
                    const lastMsg = { ...newHistory[lastIndex] };
                    lastMsg.content += token;
                    newHistory[lastIndex] = lastMsg;
                    return newHistory;
                });
            }
        }
        else if (data.type === 'brain_update') {
            // BACKEND ROUTING EVENT
            setActiveBrain(`@roe/${data.brain}`);
        }
        else if (data.type === 'artifacts') {
            setArtifacts(prev => [...prev, ...data.data]);
            setStreamingCode(''); 
            setIsCodeMode(false);
        }
        else if (data.type === 'done') {
            setLoading(false);
            setStatus('Idle');
            ws.close();
        }
    };
  };

  const runArtifact = async (art) => {
      setStatus(`Running ${art.filename}...`);
      try {
          const res = await fetch(`${API_URL}/execute`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ filename: art.path, language: art.lang })
          });
          const data = await res.json();
          setMessages(prev => [...prev, { role: 'system', content: `>> ${data.log}` }]);
          setStatus('Idle');
      } catch (e) {
          setStatus('Execution Failed');
      }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleBrainSwitch = (brainName) => setActiveBrain(brainName);

  const entryPoint = artifacts.find(a => a.lang === 'bash' || a.lang === 'sh') 
                  || artifacts.find(a => a.lang === 'python' || a.lang === 'py')
                  || artifacts.find(a => a.lang === 'html');

  return (
    <div className="flex h-screen bg-[#050505] text-gray-200 font-mono overflow-hidden">
      {/* Sidebar Navigation */}
      <div className="w-16 flex flex-col items-center py-4 border-r border-[#1a1a1a] bg-[#0a0a0a] z-10 flex-shrink-0">
        <div className="mb-8 text-[#00ff9d] font-bold text-xl">O</div>
        <NavIcon icon={Terminal} label="Chat" active={activeTab === 'chat'} onClick={() => setActiveTab('chat')} />
        <NavIcon icon={Brain} label="Brains" active={activeTab === 'brains'} onClick={() => setActiveTab('brains')} />
        <div className="mt-auto text-[10px] text-gray-600">{brains.installed?.length || 0}</div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col relative border-r border-[#1a1a1a] min-w-0">
        {/* Chat UI */}
        {activeTab === 'chat' && (
            <>
                <div className="h-8 flex justify-between items-center px-4 bg-[#0a0a0a] border-b border-[#1a1a1a] select-none flex-shrink-0" style={{WebkitAppRegion: 'drag'}}>
                <span className="text-xs text-gray-500">OMNI DESKTOP v1.2.0</span>
                <span className="text-xs text-[#00ff9d] animate-pulse">{status}</span>
                </div>

                <div className="flex-1 overflow-y-auto p-4 space-y-6 pb-20 w-full">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                    <div className={`max-w-[90%] p-4 rounded-lg break-words whitespace-pre-wrap ${
                        msg.role === 'user' 
                        ? 'bg-[#1a1a1a] text-white border border-gray-800' 
                        : msg.role === 'system'
                        ? 'text-yellow-500 text-xs font-bold'
                        : 'text-[#00ff9d]'
                    }`}>
                        <ReactMarkdown 
                            className="prose prose-invert prose-sm max-w-none break-words overflow-hidden"
                            components={{
                                // HIDE ALL CODE BLOCKS IN CHAT (They are in Sidebar now)
                                pre: () => <div className="hidden" />, 
                                code: ({node, inline, className, children, ...props}) => {
                                    return inline 
                                        ? <code className="bg-[#111] px-1 rounded text-[#00ff9d]" {...props}>{children}</code>
                                        : null; // Hide block code
                                }
                            }}
                        >
                        {msg.content}
                        </ReactMarkdown>
                    </div>
                    </div>
                ))}
                <div ref={messagesEndRef} />
                </div>

                <div className="p-4 bg-[#0a0a0a] border-t border-[#1a1a1a] flex-shrink-0">
                <div className="flex gap-2 items-center bg-black border border-[#333] rounded-md p-3 focus-within:border-[#00ff9d] transition-colors">
                    <span className="text-[#00ff9d]">{'>'}</span>
                    <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Command the Swarm..."
                    className="flex-1 bg-transparent outline-none text-white placeholder-gray-700 min-w-0"
                    autoFocus
                    />
                    <button onClick={sendMessage} disabled={loading} className="text-gray-500 hover:text-[#00ff9d]">
                    <Send size={18} />
                    </button>
                </div>
                </div>
            </>
        )}
        
        {activeTab === 'brains' && (
            <div className="flex-1 p-8 text-center text-gray-500">Brain Manager (Active)</div>
        )}
      </div>

      {/* Right Sidebar: Cortex */}
      <div className="w-80 bg-[#080808] flex flex-col border-l border-[#1a1a1a] flex-shrink-0">
        
        <NeuralBrain thinking={loading} loc={locSession} />
        
        <div className="p-4 border-b border-[#1a1a1a] grid grid-cols-2 gap-4">
            <div>
                <div className="text-[9px] uppercase text-gray-600 mb-1">Session LOC</div>
                <div className="text-xl font-bold text-white font-mono">{locSession}</div>
            </div>
            <div>
                <div className="text-[9px] uppercase text-gray-600 mb-1">Total LOC</div>
                <div className="text-xl font-bold text-gray-400 font-mono">{locTotal}</div>
            </div>
        </div>

        <div className="p-4 border-b border-[#1a1a1a] bg-[#0c0c0c]">
            <div className="text-[10px] uppercase text-gray-600 mb-1">Active Persona</div>
            <div className="flex items-center gap-2 text-[#00ff9d]">
                <Brain size={16} />
                <span className="font-bold text-sm truncate">{activeBrain}</span>
            </div>
        </div>

        {streamingCode && (
            <div className="p-4 border-b border-[#1a1a1a] bg-[#0a0a0a] animate-pulse flex-1 overflow-hidden flex flex-col">
                <div className="text-[9px] uppercase text-[#00ff9d] mb-2 flex items-center gap-2">
                    <Activity size={10} className="animate-spin" />
                    Incoming Transmission...
                </div>
                <pre className="text-[10px] text-gray-300 font-mono overflow-y-auto flex-1 opacity-90 whitespace-pre-wrap break-all p-2 bg-[#111] rounded border border-[#222]">
                    <HighlightCode code={streamingCode} />
                </pre>
            </div>
        )}

        {!streamingCode && artifacts.length > 0 && (
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                <div className="text-[10px] uppercase text-gray-600 mb-2 flex justify-between items-center">
                    <span>Generated Artifacts</span>
                    <span className="text-[#00ff9d]">{artifacts.length} Files</span>
                </div>
                
                {entryPoint && !loading && (
                    <button 
                        onClick={() => runArtifact(entryPoint)}
                        className="w-full flex items-center justify-center gap-2 bg-[#00ff9d] text-black text-sm py-3 rounded font-bold hover:bg-white transition-all shadow-[0_0_20px_#00ff9d40] mb-4"
                    >
                        <Play size={16} fill="black" />
                        LAUNCH APP
                    </button>
                )}
                
                {artifacts.map((art, idx) => (
                    <div key={idx} className="bg-[#111] border border-[#222] rounded p-3 hover:border-[#333] transition-colors group">
                        <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                                <FileCode size={14} className="text-blue-400" />
                                <span className="text-xs text-white font-mono truncate w-40">{art.filename}</span>
                            </div>
                            <span className="text-[9px] text-gray-500 uppercase">{art.lang}</span>
                        </div>
                    </div>
                ))}
            </div>
        )}
      </div>
    </div>
  )
}

function NavIcon({ icon: Icon, label, active, onClick }) {
  return (
    <div 
      onClick={onClick}
      className={`p-3 mb-2 rounded-lg cursor-pointer transition-all duration-200 group relative ${
        active ? 'bg-[#00ff9d]/10 text-[#00ff9d]' : 'text-gray-600 hover:text-gray-300'
      }`}
    >
      <Icon size={24} />
    </div>
  )
}

export default App
