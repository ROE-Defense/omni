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
      },
      keyframes: {
        scanline: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' }
        }
      }
    },
  },
  plugins: [],
}