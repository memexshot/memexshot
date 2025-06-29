import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { ArrowTopRightOnSquareIcon, ChevronLeftIcon, ChevronRightIcon } from '@heroicons/react/24/outline'
import { formatDistanceToNow } from 'date-fns'
import { useSupabaseRealtime } from '../hooks/useSupabaseRealtime'
import TokenPrice from './TokenPrice'

const CoinCard = ({ coin, index }) => {
  const tweetUrl = `https://twitter.com/${coin.twitter_user}/status/${coin.tweet_id}`
  
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: index * 0.05 }}
      className="bg-white dark:bg-moonshot-primary border border-moonshot-primary/10 dark:border-moonshot-secondary/10 rounded-xl overflow-hidden hover:shadow-lg dark:hover:shadow-none transition-all"
    >
      {/* Token Image */}
      <div className="aspect-square relative overflow-hidden bg-moonshot-accent/10">
        {coin.image_url ? (
          <img 
            src={coin.image_url} 
            alt={coin.ticker}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="flex items-center justify-center h-full">
            <span className="text-4xl text-moonshot-primary/30">
              ${coin.ticker}
            </span>
          </div>
        )}
      </div>
      
      <div className="p-3 sm:p-4">
        {/* Ticker */}
        <h3 className="font-mono text-lg sm:text-2xl text-moonshot-primary dark:text-white mb-1 sm:mb-2">
          ${coin.ticker}
        </h3>
        
        {/* Creator */}
        <a
          href={tweetUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="text-xs sm:text-sm text-moonshot-primary/70 dark:text-white/70 hover:text-moonshot-accent transition-colors inline-block mb-2 sm:mb-3 truncate w-full"
        >
          by @{coin.twitter_user}
        </a>
        
        {/* Price */}
        <div className="text-center mb-1.5 sm:mb-2">
          <TokenPrice mintAddress={coin.mint_address} size="sm" />
        </div>
        
        {/* Buy Button */}
        <a
          href="https://moonshot.money/"
          target="_blank"
          rel="noopener noreferrer"
          className="block w-full py-1.5 sm:py-2 px-3 sm:px-4 rounded-lg bg-moonshot-success text-white hover:bg-moonshot-success/90 transition-colors text-center text-sm sm:text-base"
        >
          Buy
        </a>
      </div>
    </motion.div>
  )
}

const Pagination = ({ currentPage, totalPages, onPageChange }) => {
  return (
    <div className="flex items-center justify-center gap-2 mt-8">
      <button
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        className="p-2 rounded-lg bg-white dark:bg-moonshot-primary border border-moonshot-primary/10 dark:border-moonshot-secondary/10 hover:bg-moonshot-primary/5 dark:hover:bg-moonshot-secondary/5 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <ChevronLeftIcon className="w-5 h-5 text-moonshot-primary dark:text-white" />
      </button>

      <div className="flex items-center gap-1">
        {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
          <button
            key={page}
            onClick={() => onPageChange(page)}
            className={`w-10 h-10 rounded-lg transition-all ${
              page === currentPage
                ? 'bg-moonshot-accent text-white'
                : 'bg-white dark:bg-moonshot-primary border border-moonshot-primary/10 dark:border-moonshot-secondary/10 hover:bg-moonshot-primary/5 dark:hover:bg-moonshot-secondary/5 text-moonshot-primary dark:text-white'
            }`}
          >
            {page}
          </button>
        ))}
      </div>

      <button
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        className="p-2 rounded-lg bg-white dark:bg-moonshot-primary border border-moonshot-primary/10 dark:border-moonshot-secondary/10 hover:bg-moonshot-primary/5 dark:hover:bg-moonshot-secondary/5 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <ChevronRightIcon className="w-5 h-5 text-moonshot-primary dark:text-white" />
      </button>
    </div>
  )
}

const LiveCoins = () => {
  const [currentPage, setCurrentPage] = useState(1)
  const itemsPerPage = 20

  // Fetch completed coins
  const { data: coinsData } = useSupabaseRealtime('coins', {
    orderBy: { column: 'created_at', ascending: false }
  })

  // Filter only completed coins
  const completedCoins = coinsData.filter(coin => coin.status === 'completed')
  
  // Pagination logic
  const totalPages = Math.ceil(completedCoins.length / itemsPerPage)
  const startIndex = (currentPage - 1) * itemsPerPage
  const endIndex = startIndex + itemsPerPage
  const currentCoins = completedCoins.slice(startIndex, endIndex)

  return (
    <div className="bg-white dark:bg-moonshot-primary rounded-2xl sm:rounded-3xl overflow-hidden border-2 border-moonshot-primary/20 dark:border-moonshot-secondary/20">
      <div className="bg-white dark:bg-moonshot-primary rounded-2xl sm:rounded-3xl overflow-hidden h-full">
        <div className="px-4 sm:px-6 py-3 sm:py-5 border-b border-moonshot-primary/10 dark:border-moonshot-secondary/10">
          <div className="flex items-center justify-between">
            <h2 className="text-lg sm:text-xl text-moonshot-primary dark:text-white">Live Coins</h2>
            <p className="text-xs sm:text-sm text-moonshot-primary/70 dark:text-white/70">
              {completedCoins.length} coins created
            </p>
          </div>
        </div>

      <div className="p-3 sm:p-6">
        {completedCoins.length === 0 ? (
          <div className="flex items-center justify-center h-64 text-moonshot-primary/50 dark:text-white/50">
            <p className="text-sm sm:text-base">No coins created yet...</p>
          </div>
        ) : (
          <>
            {/* Mobile horizontal scroll */}
            <div className="sm:hidden overflow-x-auto -mx-3 px-3">
              <div className="flex gap-2 pb-2">
                {currentCoins.map((coin, index) => (
                  <div key={coin.id} className="flex-shrink-0 w-40">
                    <CoinCard coin={coin} index={index} />
                  </div>
                ))}
              </div>
            </div>
            
            {/* Desktop grid */}
            <div className="hidden sm:grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-3">
              {currentCoins.map((coin, index) => (
                <CoinCard key={coin.id} coin={coin} index={index} />
              ))}
            </div>

            {totalPages > 1 && (
              <Pagination
                currentPage={currentPage}
                totalPages={totalPages}
                onPageChange={setCurrentPage}
              />
            )}
          </>
        )}
      </div>
      </div>
    </div>
  )
}

export default LiveCoins