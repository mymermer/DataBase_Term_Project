import './globals.css'

export const metadata = {
  title: 'European Basketball Statistics',
  description: 'Statistics for Euroleague and Eurocup',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}