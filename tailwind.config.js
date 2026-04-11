/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/sphinx_hextra/theme/**/*.html",
    "./assets/**/*.{css,js}",
    "./src/sphinx_hextra/directives/**/*.py",
  ],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        hextra: {
          primary: "#6366f1",
          "primary-dark": "#818cf8",
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "-apple-system", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "monospace"],
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};
