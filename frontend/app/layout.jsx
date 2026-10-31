export const metadata = {
  title: 'Калькулятор Pro',
}

export default function RootLayout({ children }) {
  return (
    <html lang="ru">
      <body style={{ fontFamily: 'sans-serif', margin: 0 }}>{children}</body>
    </html>
  )
}
