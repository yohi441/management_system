/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/**/*.js",
    "./management_system/forms.py"
  ],
  theme: {
    extend: {
      colors: {
        pagblue: '#20317f'
      }
    },
  },
  plugins: [],
}
