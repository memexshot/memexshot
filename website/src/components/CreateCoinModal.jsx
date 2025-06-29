import React, { useState, useRef } from 'react'
import { motion, AnimatePresence, useMotionValue, useTransform } from 'framer-motion'
import { XMarkIcon, PhotoIcon, ArrowRightIcon } from '@heroicons/react/24/outline'
import { SparklesIcon } from '@heroicons/react/24/solid'

const CreateCoinModal = ({ onClose }) => {
  const [ticker, setTicker] = useState('')
  const [showWarning, setShowWarning] = useState(false)
  const [isDragging, setIsDragging] = useState(false)
  
  const constraintsRef = useRef(null)
  const x = useMotionValue(0)
  const background = useTransform(
    x,
    [0, 50, 100],
    ["#e049e0", "#d633d6", "#c927c9"]
  )

  const handleSubmit = (e) => {
    e.preventDefault()
    // Slide to continue handles submission
  }

  const handleInputChange = (e) => {
    const value = e.target.value.toUpperCase()
    if (value.length <= 10) {
      setTicker(value)
    }
  }

  const handleDragEnd = (event, info) => {
    if (info.offset.x > 40 && ticker.length >= 3) {
      setShowWarning(true)
      x.set(0) // Reset position
    } else {
      // Snap back if not dragged far enough
      x.set(0)
    }
    setIsDragging(false)
  }

  const handleContinue = () => {
    const tweetText = `Perfecto $${ticker.toUpperCase()} @memeXshot`
    const tweetUrl = `https://twitter.com/intent/tweet?text=${encodeURIComponent(tweetText)}`
    window.open(tweetUrl, '_blank')
    onClose()
  }

  // Reset x position when going back
  const handleBack = () => {
    x.set(0)
    setShowWarning(false)
  }

  return (
    <div className="fixed inset-0 z-50 flex items-end sm:items-center justify-center sm:p-4">
      {/* Backdrop */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
        className="absolute inset-0 bg-black/60 backdrop-blur-md"
      />

      {/* Modal */}
      <motion.div
        initial={{ y: window.innerWidth < 640 ? "100%" : 20, opacity: window.innerWidth < 640 ? 1 : 0, scale: window.innerWidth < 640 ? 1 : 0.9 }}
        animate={{ y: 0, opacity: 1, scale: 1 }}
        exit={{ y: window.innerWidth < 640 ? "100%" : 20, opacity: window.innerWidth < 640 ? 1 : 0, scale: window.innerWidth < 640 ? 1 : 0.9 }}
        transition={{ type: "spring", damping: 25, stiffness: 300 }}
        className="relative bg-white dark:bg-moonshot-primary rounded-t-3xl sm:rounded-3xl p-6 sm:p-8 max-w-md w-full border border-moonshot-primary/20 dark:border-moonshot-secondary/20 sm:mx-auto"
      >
        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 rounded-xl hover:bg-moonshot-primary/10 dark:hover:bg-moonshot-secondary/10 transition-colors"
        >
          <XMarkIcon className="w-5 h-5 text-moonshot-primary dark:text-white" />
        </button>

        <AnimatePresence mode="wait">
          {!showWarning ? (
            <motion.div
              key="form"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.2 }}
            >
              <div className="flex items-center gap-2 mb-2">
                <SparklesIcon className="w-6 h-6 text-moonshot-accent" />
                <h2 className="text-2xl text-moonshot-primary dark:text-white">
                  Create Free Meme Coin
                </h2>
              </div>
              <p className="text-sm text-moonshot-primary/70 dark:text-white/70 mb-6">
                Free meme coin creation service for Solana community<br />
                <span className="text-xs text-moonshot-accent">Sponsored by Moonshot creator fees</span>
              </p>
              
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <div className="relative">
                    <input
                      type="text"
                      value={ticker}
                      onChange={handleInputChange}
                      placeholder="TICKER"
                      className="w-full px-4 sm:px-6 py-3 sm:py-4 rounded-2xl bg-moonshot-primary/10 dark:bg-moonshot-secondary/10 border border-moonshot-primary/20 dark:border-moonshot-secondary/20 focus:border-moonshot-accent/50 outline-none transition-all text-center text-xl sm:text-2xl tracking-wider text-moonshot-primary dark:text-white placeholder:text-moonshot-primary/50 dark:placeholder:text-white/50"
                      maxLength={10}
                      autoFocus
                    />
                    <div className={`absolute left-0 right-0 -bottom-1 h-0.5 bg-gradient-to-r from-moonshot-accent to-moonshot-accent-hover transition-all duration-300 ${
                      ticker.length >= 3 ? 'opacity-100' : 'opacity-0'
                    }`} />
                  </div>
                  <div className="flex justify-between items-center mt-2 sm:mt-3 px-2">
                    <p className={`text-[10px] sm:text-xs transition-colors ${
                      ticker.length < 3 ? 'text-red-500' : ticker.length === 10 ? 'text-amber-500' : 'text-moonshot-primary/70 dark:text-white/70'
                    }`}>
                      {ticker.length < 3 ? '3-10 characters required' : ticker.length === 10 ? 'Maximum length reached' : 'Valid ticker'}
                    </p>
                    <p className="text-[10px] sm:text-xs text-moonshot-primary/70 dark:text-white/70">
                      {ticker.length}/10
                    </p>
                  </div>
                </div>

                {/* Slide to Continue Button */}
                <div 
                  ref={constraintsRef}
                  className={`relative h-16 rounded-2xl overflow-hidden ${
                    ticker.length >= 3 
                      ? 'bg-moonshot-primary/10 dark:bg-moonshot-secondary/10' 
                      : 'bg-moonshot-primary/5 dark:bg-moonshot-secondary/5 opacity-50'
                  }`}
                >
                  <motion.div
                    className="absolute inset-0 opacity-30"
                    style={{ background }}
                  />
                  
                  {ticker.length >= 3 ? (
                    <>
                      <div className="absolute inset-0 flex items-center justify-end pr-6 pointer-events-none">
                        <motion.span 
                          animate={{ opacity: isDragging ? 0 : 1 }}
                          className="text-sm text-moonshot-primary/70 dark:text-white/70"
                        >
                          Slide to continue →
                        </motion.span>
                      </div>
                      
                      <motion.div
                        drag="x"
                        dragConstraints={constraintsRef}
                        dragElastic={0}
                        dragMomentum={false}
                        onDragStart={() => setIsDragging(true)}
                        onDragEnd={handleDragEnd}
                        style={{ x, touchAction: 'none' }}
                        className="absolute left-0 top-0 bottom-0 w-40"
                      >
                        <motion.div
                          className="h-full w-full rounded-2xl bg-moonshot-accent flex items-center justify-center shadow-lg cursor-grab active:cursor-grabbing"
                          whileHover={{ scale: 1.02 }}
                          whileTap={{ scale: 0.98 }}
                        >
                          <ArrowRightIcon className="w-6 h-6 text-white" />
                        </motion.div>
                      </motion.div>
                    </>
                  ) : (
                    <div className="absolute inset-0 flex items-center justify-center">
                      <span className="text-sm text-moonshot-primary/50 dark:text-white/50">
                        Enter ticker first
                      </span>
                    </div>
                  )}
                </div>
              </form>
            </motion.div>
          ) : (
            <motion.div
              key="warning"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
              transition={{ duration: 0.2 }}
              className="text-center"
            >
              <motion.div 
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ type: "spring", damping: 15 }}
                className="flex justify-center mb-6"
              >
                <div className="p-4 bg-moonshot-accent/10 rounded-full">
                  <PhotoIcon className="w-12 h-12 text-moonshot-accent" />
                </div>
              </motion.div>
              
              <h2 className="text-2xl text-moonshot-primary dark:text-white mb-4">
                Quick Tip for Success
              </h2>
              
              <p className="text-moonshot-primary/70 dark:text-white/70 mb-2">
                For our Twitter bot to detect and create your token,
              </p>
              <p className="text-moonshot-primary dark:text-white mb-6">
                please include an image in your tweet
              </p>

              <div className="bg-moonshot-accent/10 rounded-2xl p-4 mb-8 border border-moonshot-accent/20">
                <p className="text-sm text-moonshot-primary/70 dark:text-white/70 mb-2">Your tweet:</p>
                <p className="text-base font-mono text-moonshot-primary dark:text-white">
                  Perfecto ${ticker} @memeXshot
                </p>
              </div>

              <div className="flex gap-3">
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={handleBack}
                  className="flex-1 py-3 rounded-2xl border border-moonshot-primary/20 dark:border-moonshot-secondary/20 text-moonshot-primary dark:text-white hover:bg-moonshot-primary/5 dark:hover:bg-moonshot-secondary/5 transition-colors"
                >
                  Back
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={handleContinue}
                  className="relative flex-1 py-3 rounded-2xl moonshot-button moonshot-button-default text-white group overflow-hidden"
                >
                  <span className="relative z-10 flex items-center justify-center gap-2">
                    Go Twitter
                    <ArrowRightIcon className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </span>
                  <motion.div
                    className="absolute inset-0 bg-white opacity-0 group-hover:opacity-20 transition-opacity"
                  />
                </motion.button>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>
    </div>
  )
}

export default CreateCoinModal