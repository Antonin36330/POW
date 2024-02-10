/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit',
  content: ['./**/*.html', './build/**/*.css'],
  theme: {
    extend: {
      fontFamily: {
        'inter': ['Inter', 'sans-serif'],
      },
      backgroundColor: {
        'white-f2': '#F2F2F2',
        'white-fe': '#FFFEFE'
    },
    textColor: {
      'gray-8787': '#878787',
      'mauve': '#8083FF',
      'gray-bc':'#BCBCBC'
    },
  },
  plugins: [],
}
}