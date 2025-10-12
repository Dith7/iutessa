/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../templates/**/*.html',
    '../../**/*.html',
    '../../**/*.py',
  ],
  theme: {
    extend: {
      colors: {
        'iut-green': '#3db166',
        'iut-blue': '#192f59',
      },
    },
  },
  plugins: [],
}