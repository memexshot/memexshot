import React from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { XMarkIcon } from '@heroicons/react/24/outline'
import ThemeToggle from './ThemeToggle'

const MobileMenu = ({ isOpen, onClose, statuses }) => {
  const statusLabels = {
    server: 'Server',
    xBot: 'X Bot',
    moonshot: 'Moonshot',
    web: 'Web'
  }

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 z-50 lg:hidden"
            onClick={onClose}
          />
          
          {/* Menu Panel */}
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className="fixed right-0 top-0 h-full w-80 max-w-[85vw] bg-white dark:bg-moonshot-primary shadow-xl z-50 lg:hidden"
          >
            <div className="flex flex-col h-full">
              {/* Header */}
              <div className="flex items-center justify-between p-4 border-b border-moonshot-primary/10 dark:border-moonshot-secondary/10">
                <h2 className="text-lg text-moonshot-primary dark:text-white">Menu</h2>
                <button
                  onClick={onClose}
                  className="p-2 rounded-lg hover:bg-moonshot-primary/5 dark:hover:bg-moonshot-secondary/5 transition-colors"
                >
                  <XMarkIcon className="w-6 h-6 text-moonshot-primary dark:text-white" />
                </button>
              </div>
              
              {/* Content */}
              <div className="flex-1 overflow-y-auto p-4">
                {/* Navigation Links */}
                <div className="space-y-2 mb-6">
                  <a
                    href="/faqs"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="block px-4 py-3 rounded-lg bg-moonshot-primary/5 dark:bg-moonshot-secondary/5 text-moonshot-primary dark:text-white hover:bg-moonshot-primary/10 dark:hover:bg-moonshot-secondary/10 transition-colors"
                    onClick={onClose}
                  >
                    FAQs
                  </a>
                </div>
                
                {/* System Status */}
                <div className="mb-6">
                  <h3 className="text-sm text-moonshot-primary/60 dark:text-white/60 mb-3">System Status</h3>
                  <div className="space-y-2">
                    {Object.entries(statuses).map(([key, status]) => (
                      <div key={key} className="flex items-center justify-between px-4 py-2 rounded-lg bg-moonshot-primary/5 dark:bg-moonshot-secondary/5">
                        <span className="text-sm text-moonshot-primary dark:text-white">
                          {statusLabels[key]}
                        </span>
                        <div className={`w-2 h-2 rounded-full ${status ? 'bg-moonshot-success' : 'bg-red-400'}`} />
                      </div>
                    ))}
                  </div>
                </div>
                
                {/* Theme Toggle */}
                <div className="flex items-center justify-between px-4 py-3 rounded-lg bg-moonshot-primary/5 dark:bg-moonshot-secondary/5">
                  <span className="text-sm text-moonshot-primary dark:text-white">Dark Mode</span>
                  <ThemeToggle />
                </div>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}

export default MobileMenu