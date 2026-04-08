/** @type {import('tailwindcss').Config} */
// module.exports = {
//   content: ["./blogapp/templates/**/*.html"],
//   theme: {
//     extend: {},
//   },
//   plugins: [],
// }


module.exports = {
  content: [
    './templates/**/*.html',
    './blogapp/templates/**/*.html',
    './dashboard/templates/**/*.html',
    './**/templates/**/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}