/** @type {import('tailwindcss').Config} */
const plugin = require('tailwindcss/plugin')

const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  darkMode: 'class',
  content: [
    "./templates/**/*.html",
    "./static/js/**/*.js",
    "./management_system/forms.py",
    
  ],
  theme: {
    
    extend: {
      colors: {
        pablue: '#20317f'
      },
      fontFamily: {
        'sans': ['Inter', ...defaultTheme.fontFamily.sans],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms')
  ],
}
