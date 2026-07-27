/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Colores corporativos CENERH
        'cenerh-blue': '#0050A0',
        'cenerh-blue-dark': '#003d7a',
        'cenerh-red': '#D62828',
        'cenerh-gold': '#C9A14A',
        'cenerh-black': '#0D0D0D',
        'cenerh-gray': '#B8BFC7',
      },
      fontFamily: {
        'montserrat': ['Montserrat', 'sans-serif'],
        'garamond': ['Cormorant Garamond', 'serif'],
      },
      boxShadow: {
        'lg-blue': '0 20px 25px -5px rgba(0, 80, 160, 0.1)',
      },
    },
  },
  plugins: [],
}
