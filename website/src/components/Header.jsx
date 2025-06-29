import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { SparklesIcon, ClipboardDocumentIcon, Bars3Icon } from '@heroicons/react/24/outline'
import { CheckCircleIcon, CheckIcon } from '@heroicons/react/24/solid'
import ThemeToggle from './ThemeToggle'
import CreateCoinModal from './CreateCoinModal'
import MobileMenu from './MobileMenu'
import PriceDisplay from './PriceDisplay'
import { shortenAddress } from '../services/jupiter'

// Temporary contract address
const MXS_CONTRACT = '7GCihgDB8fe6KNjn2MYtkzZcRjQy3t9GHdC8MXS6moon'

const CompactStatus = ({ statuses }) => {
  const statusLabels = {
    server: 'Server',
    xBot: 'X Bot',
    moonshot: 'Moonshot',
    web: 'Web'
  }
  
  return (
    <div className="flex flex-col gap-0.5">
      {Object.entries(statuses).map(([key, status]) => (
        <div key={key} className="flex items-center gap-1">
          <div className={`w-1.5 h-1.5 rounded-full ${status ? 'bg-moonshot-success' : 'bg-red-400'}`} />
          <span className="text-[10px] text-moonshot-primary/60 dark:text-white/60">
            {statusLabels[key]}
          </span>
        </div>
      ))}
    </div>
  )
}

const Header = () => {
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const [copied, setCopied] = useState(false)
  
  // Mock status data - replace with real data
  const [statuses] = useState({
    server: true,
    xBot: true,
    moonshot: true,
    web: true
  })

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(MXS_CONTRACT)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('Failed to copy:', err)
    }
  }

  return (
    <>
      <header className="bg-white dark:bg-moonshot-primary relative z-40 border-b border-moonshot-primary/10 dark:border-moonshot-secondary/10">
        <div className="px-4 sm:px-6 py-3 sm:py-4">
          <div className="flex items-center justify-between">
            {/* Left Section - Logo, FAQs, BUY MXS */}
            <div className="flex items-center gap-3 sm:gap-6">
              {/* Logo */}
              <div className="flex items-center gap-2 sm:gap-3">
                <motion.div
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="p-1.5 sm:p-2 rounded-xl sm:rounded-2xl bg-moonshot-gradient shadow-lg shadow-moonshot-pink/25"
                >
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                  >
                    <SparklesIcon className="w-5 h-5 sm:w-6 sm:h-6 text-white" />
                  </motion.div>
                </motion.div>
                <div>
                  <h1 className="text-lg sm:text-2xl text-moonshot-primary dark:text-white">
                    memeXshot
                  </h1>
                </div>
              </div>

              {/* FAQs Link - Hidden on mobile */}
              <a
                href="/faqs"
                target="_blank"
                rel="noopener noreferrer"
                className="hidden sm:block text-moonshot-primary/70 dark:text-white/70 hover:text-moonshot-accent transition-colors text-sm"
              >
                FAQs
              </a>

              {/* BUY MXS Button with Contract - Hidden on mobile */}
              <div className="hidden sm:flex items-center gap-2">
                <a
                  href="https://moonshot.money/"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="px-4 py-2 rounded-xl bg-moonshot-success text-white text-sm hover:bg-moonshot-success/90 transition-colors"
                >
                  BUY MXS
                </a>
                <button
                  onClick={copyToClipboard}
                  className="flex items-center gap-1 text-xs text-moonshot-primary/50 dark:text-white/50 hover:text-moonshot-accent transition-colors group"
                >
                  {shortenAddress(MXS_CONTRACT)}
                  {copied ? (
                    <CheckIcon className="w-3 h-3 text-moonshot-success" />
                  ) : (
                    <ClipboardDocumentIcon className="w-3 h-3 opacity-0 group-hover:opacity-100 transition-opacity" />
                  )}
                </button>
              </div>
            </div>

            {/* Center - Create Button */}
            <button
              onClick={() => setIsModalOpen(true)}
              className="flex items-center gap-2 sm:gap-3 px-3 sm:px-8 py-2 sm:py-3.5 rounded-xl sm:rounded-2xl bg-moonshot-accent text-white text-sm sm:text-lg hover:bg-moonshot-accent-hover transition-colors"
            >
              <div className="w-5 h-5 sm:w-7 sm:h-7 rounded-full bg-white/20 flex items-center justify-center">
                <span className="text-lg sm:text-2xl leading-none pb-0.5">+</span>
              </div>
              <span className="hidden sm:inline">Create Free Meme Coin</span>
              <span className="sm:hidden">Create</span>
            </button>

            {/* Right Section - Info Panel */}
            <div className="flex items-center gap-2 sm:gap-4">
              {/* Prices - Hidden on small mobile */}
              <div className="hidden xs:flex items-center gap-2 sm:gap-3 px-2 sm:px-4 py-1.5 sm:py-2 rounded-lg sm:rounded-xl bg-moonshot-primary/5 dark:bg-moonshot-secondary/5 border border-moonshot-primary/10 dark:border-moonshot-secondary/10">
                <PriceDisplay token="SOL" symbol="SOL" />
                <div className="w-px h-4 bg-moonshot-primary/20 dark:bg-white/20" />
                <PriceDisplay token="MXS" symbol="MXS" />
              </div>

              {/* Compact Status - Hidden on mobile */}
              <div className="hidden lg:block">
                <CompactStatus statuses={statuses} />
              </div>
              
              {/* Theme Toggle - Hidden on mobile */}
              <div className="hidden lg:block">
                <ThemeToggle />
              </div>
              
              {/* Mobile Menu Button */}
              <button
                onClick={() => setIsMobileMenuOpen(true)}
                className="lg:hidden p-2 rounded-lg hover:bg-moonshot-primary/5 dark:hover:bg-moonshot-secondary/5 transition-colors"
              >
                <Bars3Icon className="w-6 h-6 text-moonshot-primary dark:text-white" />
              </button>
            </div>
          </div>
        </div>
      </header>
      
      {/* Mobile Buy MXS Bar */}
      <div className="sm:hidden bg-white dark:bg-moonshot-primary border-b border-moonshot-primary/10 dark:border-moonshot-secondary/10 px-4 py-2">
        <div className="flex items-center justify-between">
          <a
            href="https://moonshot.money/"
            target="_blank"
            rel="noopener noreferrer"
            className="px-4 py-1.5 rounded-lg bg-moonshot-success text-white text-sm hover:bg-moonshot-success/90 transition-colors"
          >
            BUY MXS
          </a>
          <button
            onClick={copyToClipboard}
            className="flex items-center gap-1 text-xs text-moonshot-primary/50 dark:text-white/50 hover:text-moonshot-accent transition-colors"
          >
            {shortenAddress(MXS_CONTRACT)}
            {copied ? (
              <CheckIcon className="w-3 h-3 text-moonshot-success" />
            ) : (
              <ClipboardDocumentIcon className="w-3 h-3" />
            )}
          </button>
        </div>
      </div>

      {/* Create Coin Modal */}
      <AnimatePresence>
        {isModalOpen && (
          <CreateCoinModal onClose={() => setIsModalOpen(false)} />
        )}
      </AnimatePresence>
      
      {/* Mobile Menu */}
      <MobileMenu 
        isOpen={isMobileMenuOpen} 
        onClose={() => setIsMobileMenuOpen(false)} 
        statuses={statuses}
      />
    </>
  )
}

export default Header