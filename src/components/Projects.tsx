import { motion } from 'framer-motion'
import { useInView } from 'react-intersection-observer'

interface Project {
  id: number
  title: string
  description: string
  tags: string[]
  image: string
  color: string
  githubLink?: string
  liveLink?: string
}

const Projects: React.FC = () => {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  })

  // ─── Add your projects here ───────────────────────────────────────────────
  // To add a project, copy one of the objects below and fill in your details.
  // - title:       Project name
  // - description: Short summary of what the project does
  // - tags:        Technologies / skills used (shown as badges)
  // - image:       URL to a preview image (Unsplash, local file, etc.)
  // - color:       Tailwind gradient classes for the card accent
  // - githubLink:  (optional) URL to the GitHub repo
  // - liveLink:    (optional) URL to the live demo
  const projects: Project[] = [
    {
      id: 1,
      title: 'SQL Data Warehouse Project',
      description:
        'Built a modern data warehouse using SQL Server, covering the full lifecycle: ETL processes, dimensional data modeling (star schema), and analytical reporting. Demonstrates real-world data engineering patterns from staging through to the presentation layer.',
      tags: ['SQL Server', 'ETL', 'Data Modeling', 'Star Schema', 'Analytics'],
      image: 'https://images.unsplash.com/photo-1544383835-bda2bc66a55d?w=600&h=400&fit=crop',
      color: 'from-blue-400 to-cyan-600',
      githubLink: 'https://github.com/alhaddad-a/SQL-DW-Project_1',
      liveLink: undefined,
    },
    {
      id: 2,
      title: 'Databricks Medallion Pipeline',
      description:
        'Implemented a scalable data pipeline on Databricks following the Medallion Architecture (Bronze → Silver → Gold layers). Handles raw data ingestion, cleansing and transformation, and curated output ready for business intelligence and analytics.',
      tags: ['Databricks', 'PySpark', 'Medallion Architecture', 'Delta Lake', 'Python'],
      image: 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600&h=400&fit=crop',
      color: 'from-orange-400 to-red-600',
      githubLink: 'https://github.com/alhaddad-a/databricks-medallion-pipeline',
      liveLink: undefined,
    },
    {
      id: 3,
      title: 'Healthcare Lakehouse on Databricks',
      description:
        'Built an end-to-end healthcare data lakehouse on Databricks using Delta Lake and the Medallion Architecture. Processes and transforms real-world healthcare datasets through Bronze, Silver, and Gold layers, enabling reliable analytics and reporting on patient and clinical data.',
      tags: ['Databricks', 'Delta Lake', 'PySpark', 'Healthcare', 'Medallion Architecture', 'Python'],
      image: 'https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=600&h=400&fit=crop',
      color: 'from-green-400 to-teal-600',
      githubLink: 'https://github.com/alhaddad-a/healthcare-lakehouse-databricks',
      liveLink: undefined,
    },
  ]

  const containerVariants = {
    hidden: {},
    visible: {
      transition: { staggerChildren: 0.15 },
    },
  }

  const cardVariants = {
    hidden: { opacity: 0, y: 40 },
    visible: { opacity: 1, y: 0, transition: { duration: 0.6 } },
  }

  return (
    <section id="projects" className="section-padding bg-gray-50 dark:bg-gray-950 transition-colors duration-300">
      <div className="container-max">

        {/* ── Section header ── */}
        <motion.div
          ref={ref}
          initial={{ opacity: 0, y: 30 }}
          animate={inView ? { opacity: 1, y: 0 } : {}}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Projects
          </h2>
          <div className="w-24 h-1 bg-primary-400 mx-auto mb-8" />
          <p className="text-lg text-gray-600 dark:text-gray-300 max-w-3xl mx-auto">
            A collection of data engineering projects — from SQL data warehouses to
            cloud-based big data pipelines built with Spark and Databricks.
          </p>
        </motion.div>

        {/* ── Project grid ── */}
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate={inView ? 'visible' : 'hidden'}
          className="grid md:grid-cols-2 lg:grid-cols-3 gap-8"
        >
          {projects.map((project) => (
            <motion.div
              key={project.id}
              variants={cardVariants}
              whileHover={{ y: -6 }}
              className="group"
            >
              <div className="bg-white dark:bg-gray-900 rounded-xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden border border-gray-200 dark:border-gray-800 h-full flex flex-col">

                {/* Preview image */}
                <div className="relative h-48 overflow-hidden flex-shrink-0">
                  <img
                    src={project.image}
                    alt={project.title}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
                  />
                  <div
                    className={`absolute inset-0 bg-gradient-to-t ${project.color} opacity-20 group-hover:opacity-35 transition-opacity duration-300`}
                  />
                  {/* Folder icon badge */}
                  <div className="absolute top-4 right-4">
                    <div className="w-8 h-8 bg-white rounded-full flex items-center justify-center shadow-lg">
                      <svg className="w-5 h-5 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                          d="M3 7a2 2 0 012-2h4l2 2h8a2 2 0 012 2v8a2 2 0 01-2 2H5a2 2 0 01-2-2V7z" />
                      </svg>
                    </div>
                  </div>
                </div>

                {/* Content */}
                <div className="p-6 flex flex-col flex-1">
                  <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors duration-300">
                    {project.title}
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300 mb-5 leading-relaxed flex-1">
                    {project.description}
                  </p>

                  {/* Tech tags */}
                  <div className="flex flex-wrap gap-2 mb-6">
                    {project.tags.map((tag) => (
                      <span
                        key={tag}
                        className="px-3 py-1 bg-gray-100 dark:bg-gray-800 text-primary-600 dark:text-primary-400 text-xs font-semibold rounded-full border border-gray-200 dark:border-gray-700"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>

                  {/* Action buttons */}
                  <div className="flex gap-3 mt-auto">
                    {project.githubLink && (
                      <motion.a
                        href={project.githubLink}
                        target="_blank"
                        rel="noopener noreferrer"
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        className="flex-1 inline-flex items-center justify-center gap-2 px-4 py-2.5 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-900 dark:text-white font-semibold rounded-lg transition-all duration-300 border border-gray-300 dark:border-gray-700 hover:border-primary-400 text-sm"
                      >
                        {/* GitHub icon */}
                        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" />
                        </svg>
                        GitHub
                      </motion.a>
                    )}
                    {project.liveLink && (
                      <motion.a
                        href={project.liveLink}
                        target="_blank"
                        rel="noopener noreferrer"
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        className={`flex-1 inline-flex items-center justify-center gap-2 px-4 py-2.5 bg-gradient-to-r ${project.color} text-white font-semibold rounded-lg hover:shadow-lg transition-all duration-300 text-sm`}
                      >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                            d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                        </svg>
                        Live Demo
                      </motion.a>
                    )}
                    {/* If no links are set yet, show a placeholder badge */}
                    {!project.githubLink && !project.liveLink && (
                      <span className="inline-flex items-center gap-2 px-4 py-2.5 bg-gray-100 dark:bg-gray-800 text-gray-400 dark:text-gray-500 text-sm font-medium rounded-lg border border-gray-200 dark:border-gray-700 cursor-default">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2}
                            d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        Coming Soon
                      </span>
                    )}
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>


      </div>
    </section>
  )
}

export default Projects
