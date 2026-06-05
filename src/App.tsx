import { FC } from 'react'
import { ThemeProvider } from './context/ThemeContext'
import Hero from './components/Hero.tsx'
import About from './components/About.tsx'
import Certificates from './components/Certificates.tsx'
import Projects from './components/Projects.tsx'
import Contact from './components/Contact.tsx'
import Footer from './components/Footer.tsx'
import Navigation from './components/Navigation.tsx'
import WhatsAppButton from './components/WhatsAppButton.tsx'

const App: FC = () => {
  return (
    <ThemeProvider>
      <div className="min-h-screen bg-white dark:bg-black text-gray-900 dark:text-white transition-colors duration-300">
        <Navigation />
        <Hero />
        <About />
        <Certificates />
        <Projects />
        <Contact />
        <Footer />
        <WhatsAppButton />
      </div>
    </ThemeProvider>
  )
}

export default App
