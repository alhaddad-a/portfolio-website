import { motion } from 'framer-motion'
import { useInView } from 'react-intersection-observer'

const Certificates: React.FC = () => {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  })

  const certificates = [
    {
      id: 1,
      title: 'Python Project for Data Engineering',
      issuer: 'Coursera',
      date: '2025',
      description: 'Hands-on project experience in Python for data engineering tasks and workflows.',
      link: 'https://www.coursera.org/account/accomplishments/verify/60ZS3IUWIADG',
      image: 'https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=400&h=300&fit=crop',
      color: 'from-blue-400 to-blue-600',
    },
    {
      id: 2,
      title: 'Introduction to Relational Databases',
      issuer: 'Coursera',
      date: '2025',
      description: 'Fundamental concepts of relational database design and SQL querying.',
      link: 'https://www.coursera.org/account/accomplishments/verify/07IJTT5M0YTK',
      image: 'https://images.unsplash.com/photo-1544383835-bda2bc66a55d?w=400&h=300&fit=crop',
      color: 'from-green-400 to-green-600',
    },
    {
      id: 3,
      title: 'Introduction to Data Engineering',
      issuer: 'Coursera',
      date: '2025',
      description: 'Comprehensive introduction to data engineering principles and practices.',
      link: 'https://www.coursera.org/account/accomplishments/verify/ISM8KESVTK0T',
      image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=300&fit=crop',
      color: 'from-purple-400 to-purple-600',
    },
    {
      id: 4,
      title: 'Python for Data Science, AI & Development',
      issuer: 'Coursera',
      date: '2025',
      description: 'Python programming skills for data science, artificial intelligence, and development.',
      link: 'https://www.coursera.org/account/accomplishments/verify/DHVEAMC5054Q',
      image: 'https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=400&h=300&fit=crop',
      color: 'from-yellow-400 to-orange-600',
    },
    {
      id: 5,
      title: 'Generative AI: Prompt Engineering Basics',
      issuer: 'Coursera',
      date: '2025',
      description: 'Fundamentals of prompt engineering for generative AI applications.',
      link: 'https://www.coursera.org/account/accomplishments/verify/10Y6ITKVRB60',
      image: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?w=400&h=300&fit=crop',
      color: 'from-pink-400 to-rose-600',
    },
    {
      id: 6,
      title: 'Data Warehouse Fundamentals for Beginners',
      issuer: 'Udemy',
      date: '2024',
      description: 'Essential concepts and practices for data warehouse design and implementation.',
      link: 'https://www.udemy.com/certificate/UC-fec6d173-8a9e-466a-a877-3788f7db48db/',
      image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=300&fit=crop',
      color: 'from-indigo-400 to-indigo-600',
    },
    {
      id: 7,
      title: 'Big Data with Apache Spark on Python',
      issuer: 'Udemy',
      date: '2025',
      description: 'Hands-on experience with Apache Spark for big data processing using Python.',
      link: 'https://www.udemy.com/certificate/UC-28a1517c-fdd3-4f7e-8059-a2295e7efa4d/',
      image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=400&h=300&fit=crop',
      color: 'from-red-400 to-red-600',
    },
  ]

  return (
    <section id="certificates" className="section-padding bg-black">
      <div className="container-max">
        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 30 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Certificates 
          </h2>
          <div className="w-24 h-1 bg-primary-400 mx-auto mb-8"></div>
          <p className="text-lg text-gray-300 max-w-3xl mx-auto">
            Continuous learning is key to staying current in technology. Here are some of my
            professional certifications that validate my expertise in various technologies.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {certificates.map((cert, index) => (
            <motion.div
              key={cert.id}
              initial={{ opacity: 0, y: 30 }}
              animate={inView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.6, delay: index * 0.2 }}
              whileHover={{ y: -5 }}
              className="group"
            >
              <div className="bg-gray-900 rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden border border-gray-800">
                {/* Certificate Image */}
                <div className="relative h-48 overflow-hidden">
                  <img
                    src={cert.image}
                    alt={cert.title}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                  />
                  <div className={`absolute inset-0 bg-gradient-to-t ${cert.color} opacity-20 group-hover:opacity-30 transition-opacity duration-300`}></div>
                  <div className="absolute top-4 right-4">
                    <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center shadow-lg">
                      <svg className="w-5 h-5 text-primary-600" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                    </div>
                  </div>
                </div>

                {/* Certificate Content */}
                <div className="p-6">
                  <div className="mb-4">
                    <h3 className="text-xl font-bold text-white mb-2 group-hover:text-primary-400 transition-colors duration-300">
                      {cert.title}
                    </h3>
                    <p className="text-primary-400 font-semibold mb-1">{cert.issuer}</p>
                    <p className="text-sm text-gray-400">{cert.date}</p>
                  </div>

                  <p className="text-gray-300 mb-6 leading-relaxed">
                    {cert.description}
                  </p>

                  <motion.a
                    href={cert.link}
                    target="_blank"
                    rel="noopener noreferrer"
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className={`inline-flex items-center px-6 py-3 bg-gradient-to-r ${cert.color} text-white font-semibold rounded-lg hover:shadow-lg transition-all duration-300 group-hover:shadow-xl`}
                  >
                    View Certificate
                    <svg className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                  </motion.a>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        {/* Additional Info */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8, delay: 0.8 }}
          className="text-center mt-12"
        >
            <div className="bg-gray-800 rounded-xl p-8 max-w-4xl mx-auto">
              <h3 className="text-2xl font-bold text-white mb-4">
                Continuous Learning
              </h3>
              <p className="text-gray-300 mb-6">
              I believe in staying up-to-date with the latest technologies and best practices.
              These certifications represent my commitment to professional growth and expertise
              in modern web development technologies.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <span className="px-4 py-2 bg-primary-100 text-primary-800 rounded-full text-sm font-medium">
                Data Engineering
              </span>
              <span className="px-4 py-2 bg-primary-100 text-primary-800 rounded-full text-sm font-medium">
                Python Programming
              </span>
              <span className="px-4 py-2 bg-primary-100 text-primary-800 rounded-full text-sm font-medium">
                Big Data Processing
              </span>
              <span className="px-4 py-2 bg-primary-100 text-primary-800 rounded-full text-sm font-medium">
                Full Stack Development
              </span>
              <span className="px-4 py-2 bg-primary-100 text-primary-800 rounded-full text-sm font-medium">
                Machine Learning
              </span>
              <span className="px-4 py-2 bg-primary-100 text-primary-800 rounded-full text-sm font-medium">
                Database Design
              </span>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}

export default Certificates
