/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        omni: {
          dark: '#050505',
          panel: '#0a0a0a',
          accent: '#00ff9d', // Cyber Green
          dim: '#1a1a1a',
          text: '#e0e0e0'
        }
      },
      fontFamily: {
        mono: ['SF Mono', 'Menlo', 'monospace'],
      },
      animation: {
        'scanline': 'scanline 2s linear infinite',
        'spin-slow': 'spin 8s linear infinite',
        'reverse-spin': 'spin 6s linear infinite reverse',
        'scan': 'scan 1s ease-in-out infinite',
        'pulse-fast': 'pulse 0.5s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        scanline: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' }
        },
        scan: {
            '0%': { transform: 'translateY(-50px)', opacity: 0 },
            '50%': { opacity: 1 },
            '100%': { transform: 'translateY(50px)', opacity: 0 }
        }
      }
    },
  },
  plugins: [],
}