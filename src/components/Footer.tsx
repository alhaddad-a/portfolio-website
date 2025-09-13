import { motion } from 'framer-motion'

const Footer: React.FC = () => {
  return (
    <footer className="bg-dark-900 text-white">
      <div className="container-max">
        <div className="py-12 px-4 sm:px-6 lg:px-8">

          {/* Bottom Section */}
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="border-t border-dark-800 mt-12 pt-8"
          >
            <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
              <p className="text-gray-400 text-sm">
                © 2025  Abdullah alhaddad . All rights reserved.
              </p>
            </div>
          </motion.div>
        </div>
      </div>
    </footer>
  )
}

export default Footer
