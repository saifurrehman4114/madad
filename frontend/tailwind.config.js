/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        urdu: ['"Noto Nastaliq Urdu"', "serif"],
      },
      colors: {
        madad: {
          gold: "#F5B700",
          ink: "#0B0F1A",
          pine: "#054A29",
        },
      },
    },
  },
  plugins: [],
};
