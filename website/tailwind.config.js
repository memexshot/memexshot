/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      screens: {
        'xs': '475px',
      },
      fontFamily: {
        'sans': ['Rabone', 'sans-serif'],
        'mono': ['Rabone', 'monospace'],
      },
      colors: {
        moonshot: {
          primary: '#131324', // rgb(19, 19, 36)
          secondary: '#ffffff', // rgb(255, 255, 255)
          accent: '#e049e0', // rgb(224, 73, 224)
          'accent-hover': '#d633d6',
          'primary-light': '#1a1a32', // slightly lighter for borders
          'primary-lighter': '#212140', // for hover states
          gray: '#6b7280',
          'gray-light': '#9ca3af',
          'gray-dark': '#4b5563',
          success: '#45b255', // rgb(69, 178, 85)
          error: '#ef4444',
        }
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'moonshot-gradient': 'linear-gradient(135deg, #e049e0 0%, #d633d6 100%)',
        'moonshot-gradient-reverse': 'linear-gradient(135deg, #d633d6 0%, #e049e0 100%)',
        'moonshot-mesh': 'radial-gradient(at 20% 80%, #e049e033 0, transparent 50%), radial-gradient(at 80% 20%, #e049e033 0, transparent 50%), radial-gradient(at 40% 40%, #e049e022 0, transparent 50%)'
      },
      animation: {
        'pulse-slow': 'pulse 4s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'gradient': 'gradient 8s ease infinite',
        'float': 'float 6s ease-in-out infinite',
        'glow': 'glow 2s ease-in-out infinite alternate',
      },
      keyframes: {
        gradient: {
          '0%, 100%': {
            'background-size': '200% 200%',
            'background-position': 'left center'
          },
          '50%': {
            'background-size': '200% 200%',
            'background-position': 'right center'
          }
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-20px)' }
        },
        glow: {
          from: { boxShadow: '0 0 10px #fe80fe, 0 0 20px #fe80fe, 0 0 30px #fe80fe' },
          to: { boxShadow: '0 0 20px #fe80fe, 0 0 30px #fe80fe, 0 0 40px #fe80fe' }
        }
      },
      backdropBlur: {
        xs: '2px',
      }
    },
  },
  plugins: [],
}