import './globals.css'

export const metadata = {
  title: 'Deepfake Detection',
  description: 'AI-powered deepfake detection',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}