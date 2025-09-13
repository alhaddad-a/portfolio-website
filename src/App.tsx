import { FC } from 'react'
import Hero from './components/Hero.tsx'
import About from './components/About.tsx'
import Certificates from './components/Certificates.tsx'
import Contact from './components/Contact.tsx'
import Footer from './components/Footer.tsx'
import Navigation from './components/Navigation.tsx'

const App: FC = () => {
  return (
    <div className="min-h-screen bg-black text-white">
      <Navigation />
      <Hero />
      <About />
      <Certificates />
      <Contact />
      <Footer />
    </div>
  )
}

export default App
