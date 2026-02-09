import React from 'react';

export default function NeuralBrain({ thinking, loc }) {
  return (
    <div className="w-full h-48 bg-[#050505] relative overflow-hidden border-b border-[#1a1a1a] flex items-center justify-center group">
        {/* X-Ray Grid Background */}
        <div className="absolute inset-0 bg-[linear-gradient(rgba(0,255,157,0.05)_1px,transparent_1px),linear-gradient(90deg,rgba(0,255,157,0.05)_1px,transparent_1px)] bg-[size:40px_40px] [mask-image:radial-gradient(ellipse_at_center,black_40%,transparent_100%)]"></div>
        
        {/* Brain Container */}
        <div className={`relative w-32 h-32 flex items-center justify-center transition-all duration-700 ${thinking ? 'scale-110' : 'opacity-60'}`}>
            
            {/* Outer Skull (X-Ray Shell) */}
            <div className={`absolute inset-0 rounded-full border border-[#00ff9d] opacity-20 animate-pulse-slow ${thinking ? 'border-dashed' : ''}`}></div>
            <div className="absolute inset-2 rounded-full border border-[#00ff9d] opacity-10 animate-spin-slow border-t-transparent border-l-transparent"></div>
            <div className="absolute inset-4 rounded-full border border-[#00ff9d] opacity-10 animate-reverse-spin border-b-transparent border-r-transparent"></div>

            {/* Brain Hemisphere (Wireframe SVG) */}
            <svg viewBox="0 0 100 100" className="w-20 h-20 text-[#00ff9d] opacity-80 drop-shadow-[0_0_8px_rgba(0,255,157,0.5)]">
                <path d="M50 15 C30 15 15 30 15 50 C15 70 30 85 50 85 C70 85 85 70 85 50 C85 30 70 15 50 15 Z M50 15 L50 85 M15 50 L85 50 M30 25 C40 35 60 35 70 25 M30 75 C40 65 60 65 70 75" 
                      fill="none" 
                      stroke="currentColor" 
                      strokeWidth="0.5" 
                      className={thinking ? 'animate-pulse' : ''}
                />
                {/* Synapses */}
                {thinking && (
                    <>
                        <circle cx="50" cy="50" r="2" className="animate-ping" fill="currentColor" />
                        <circle cx="30" cy="35" r="1.5" className="animate-ping animation-delay-200" fill="currentColor" />
                        <circle cx="70" cy="35" r="1.5" className="animate-ping animation-delay-500" fill="currentColor" />
                        <circle cx="50" cy="75" r="1.5" className="animate-ping animation-delay-700" fill="currentColor" />
                    </>
                )}
            </svg>
            
            {/* Data Stream Particles */}
            {thinking && (
                <div className="absolute inset-0">
                    <div className="absolute top-0 left-1/2 w-[1px] h-full bg-gradient-to-b from-transparent via-[#00ff9d] to-transparent animate-scan opacity-50"></div>
                    <div className="absolute top-1/2 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-[#00ff9d] to-transparent animate-scan opacity-50"></div>
                </div>
            )}
        </div>

        {/* HUD Elements */}
        <div className="absolute top-2 right-2 flex flex-col items-end gap-1">
            <div className="flex gap-1">
                <div className={`w-1 h-1 rounded-full ${thinking ? 'bg-[#00ff9d] animate-ping' : 'bg-gray-800'}`}></div>
                <div className={`w-1 h-1 rounded-full ${thinking ? 'bg-[#00ff9d] animate-ping animation-delay-200' : 'bg-gray-800'}`}></div>
                <div className={`w-1 h-1 rounded-full ${thinking ? 'bg-[#00ff9d] animate-ping animation-delay-400' : 'bg-gray-800'}`}></div>
            </div>
        </div>
        
        {/* Status Text */}
        <div className="absolute bottom-2 left-0 right-0 text-center">
            <span className={`text-[9px] font-mono tracking-widest ${thinking ? 'text-[#00ff9d] animate-pulse' : 'text-gray-600'}`}>
                {thinking ? 'CORTEX: ACTIVE' : 'IDLE'}
            </span>
        </div>
    </div>
  );
}
