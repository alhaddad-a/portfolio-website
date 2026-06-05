import { motion } from 'framer-motion'
import { useInView } from 'react-intersection-observer'

const Hero: React.FC = () => {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  })

  return (
    <section id="home" className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-100 via-white to-blue-50 dark:from-gray-900 dark:via-black dark:to-gray-800 relative overflow-hidden py-16 xs:py-20 sm:py-24 transition-colors duration-300">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-primary-200 rounded-full mix-blend-multiply filter blur-xl opacity-50 dark:opacity-70 animate-bounce-slow"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-primary-300 rounded-full mix-blend-multiply filter blur-xl opacity-50 dark:opacity-70 animate-bounce-slow" style={{ animationDelay: '1s' }}></div>
      </div>

      <div className="container-max section-padding relative z-10">
        <div className="text-center">
          <motion.div
            ref={ref}
            initial={{ opacity: 0, y: 30 }}
            animate={inView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8 }}
            className="space-y-8"
          >
            {/* Profile Image */}
            <motion.div
              initial={{ scale: 0 }}
              animate={inView ? { scale: 1 } : {}}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="flex justify-center"
            >
              <div className="relative">
                <img
                  src="/profile-photo.jpg"
                  alt="Abdullah Alhaddad"
                  className="w-24 h-24 xs:w-28 xs:h-28 sm:w-36 sm:h-36 md:w-40 md:h-40 lg:w-44 lg:h-44 xl:w-48 xl:h-48 rounded-full object-cover shadow-2xl border-4 border-primary-400"
                />
                <div className="absolute inset-0 rounded-full border-2 border-primary-300 opacity-50 animate-pulse"></div>
              </div>
            </motion.div>

            {/* Name and Title */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="space-y-4"
            >
              <h1 className="text-3xl xs:text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 dark:text-white leading-tight">
                Abdullah Alhaddad
              </h1>
              <h2 className="text-lg xs:text-xl sm:text-2xl md:text-3xl lg:text-4xl text-primary-600 dark:text-primary-400 font-semibold">
                Data Engineer
              </h2>
              <p className="text-base xs:text-lg sm:text-xl md:text-2xl text-gray-600 dark:text-gray-300 max-w-xs xs:max-w-sm sm:max-w-2xl md:max-w-3xl mx-auto leading-relaxed px-4">
                Building scalable data pipelines, warehouses, and big data solutions using
                Python, SQL Server, Apache Spark, and Databricks.
              </p>
            </motion.div>

            {/* CTA Buttons */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.8, delay: 0.6 }}
              className="flex flex-col xs:flex-row gap-3 xs:gap-4 justify-center items-center px-4"
            >
              <motion.a
                href="#contact"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="btn-primary text-sm xs:text-base px-4 xs:px-6 py-2 xs:py-3 w-full xs:w-auto text-center"
              >
                Get In Touch
              </motion.a>

              <motion.a
                href="#about"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="text-sm xs:text-base text-gray-500 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-colors duration-200 w-full xs:w-auto text-center"
              >
                Learn More ↓
              </motion.a>
            </motion.div>




          </motion.div>
        </div>
      </div>
    </section>
  )
}

export default Hero
