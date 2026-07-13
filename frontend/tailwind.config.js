/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        darkBg: '#090D16',
        darkCard: '#0E131F',
        darkBorder: '#161D2B',
        darkText: '#94A3B8',
        accentCritical: '#EF4444',
        accentHigh: '#F59E0B',
        accentMedium: '#3B82F6',
        accentLow: '#10B981',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['Fira Code', 'JetBrains Mono', 'monospace'],
      }
    },
  },
  plugins: [],
}
