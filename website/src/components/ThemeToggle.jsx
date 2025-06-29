import React from 'react'
import { motion } from 'framer-motion'
import { SunIcon, MoonIcon } from '@heroicons/react/24/outline'
import { useTheme } from '../context/ThemeContext'

const ThemeToggle = () => {
  const { theme, toggleTheme } = useTheme()

  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={toggleTheme}
      className="relative p-2.5 rounded-xl bg-moonshot-primary/10 dark:bg-moonshot-secondary/10 border border-moonshot-primary/20 dark:border-moonshot-secondary/20 hover:bg-moonshot-primary/20 dark:hover:bg-moonshot-secondary/20 transition-all"
      aria-label="Toggle theme"
    >
      <div className="relative w-6 h-6">
        <motion.div
          initial={false}
          animate={{
            scale: theme === 'light' ? 1 : 0,
            opacity: theme === 'light' ? 1 : 0,
            rotate: theme === 'light' ? 0 : 180
          }}
          transition={{ duration: 0.3 }}
          className="absolute inset-0"
        >
          <SunIcon className="w-6 h-6 text-moonshot-accent" />
        </motion.div>
        
        <motion.div
          initial={false}
          animate={{
            scale: theme === 'dark' ? 1 : 0,
            opacity: theme === 'dark' ? 1 : 0,
            rotate: theme === 'dark' ? 0 : -180
          }}
          transition={{ duration: 0.3 }}
          className="absolute inset-0"
        >
          <MoonIcon className="w-6 h-6 text-moonshot-accent" />
        </motion.div>
      </div>
    </motion.button>
  )
}

export default ThemeToggle