/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./prototypes/**/*.{html,js}",
    "./components/**/*.{html,js}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        inqaba: {
          navy: '#0A192F',
          gold: '#C5A059',
          interactive: '#1E3A8A',
          bg: '#F8FAFC',
          surface: '#FFFFFF',
          border: '#E2E8F0',
          darkBg: '#070D14',
          darkSurface: '#0D1724',
          darkSubtle: '#142032',
          darkBorder: '#1E2D42',
        },
        status: {
          success: '#0D9488',
          warning: '#D97706',
          danger: '#DC2626',
          info: '#0284C7',
        }
      },
      fontFamily: {
        interface: ['Inter', 'sans-serif'],
        editorial: ['Merriweather', 'serif'],
        mono: ['JetBrains Mono', 'monospace'],
      }
    },
  },
  plugins: [],
}
