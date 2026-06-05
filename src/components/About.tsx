import { motion } from 'framer-motion'
import { useInView } from 'react-intersection-observer'

const About: React.FC = () => {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  })

  const skills = [
    { name: 'Python', level: 80, color: 'bg-yellow-500' },
    { name: 'SQL / SQL Server', level: 80, color: 'bg-blue-500' },
    { name: 'PySpark / Apache Spark', level: 70, color: 'bg-orange-500' },
    { name: 'Databricks / Delta Lake', level: 70, color: 'bg-red-500' },
    { name: 'ETL & Data Modeling', level: 75, color: 'bg-purple-500' },
    { name: 'Data Warehousing', level: 75, color: 'bg-green-500' },
  ]

  return (
    <section id="about" className="section-padding bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
      <div className="container-max">
        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 30 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white mb-4">
            About Me
          </h2>
          <div className="w-24 h-1 bg-primary-400 mx-auto mb-8"></div>
          <p className="text-lg text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            Aspiring Data Engineer with hands-on experience building modern data warehouses, ETL pipelines, and big data solutions. Skilled in Python, SQL Server, Apache Spark, and Databricks, with a strong foundation in dimensional data modeling and the Medallion Architecture. Passionate about transforming raw data into reliable, analysis-ready datasets.
          </p>
        </motion.div>

        {/* Skills centered */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="max-w-2xl mx-auto"
        >
          <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6 text-center">Technical Skills</h3>
          <div className="space-y-4">
            {skills.map((skill, index) => (
              <motion.div
                key={skill.name}
                initial={{ opacity: 0, x: 20 }}
                animate={inView ? { opacity: 1, x: 0 } : {}}
                transition={{ duration: 0.5, delay: 0.4 + index * 0.1 }}
                className="space-y-2"
              >
                <div className="flex justify-between items-center">
                  <span className="font-medium text-gray-700 dark:text-gray-300">{skill.name}</span>
                  <span className="text-sm text-gray-500 dark:text-gray-400">{skill.level}%</span>
                </div>
                <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                  <motion.div
                    initial={{ width: 0 }}
                    animate={inView ? { width: `${skill.level}%` } : {}}
                    transition={{ duration: 1, delay: 0.6 + index * 0.1 }}
                    className={`h-2 rounded-full ${skill.color}`}
                  />
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  )
}

export default About
