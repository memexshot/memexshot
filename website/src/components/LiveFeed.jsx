import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { formatDistanceToNow } from 'date-fns'
import { useSupabaseRealtime } from '../hooks/useSupabaseRealtime'

const FeedItem = ({ item }) => {
  const [timeAgo, setTimeAgo] = useState(formatDistanceToNow(new Date(item.created_at), { addSuffix: true }))

  useEffect(() => {
    const interval = setInterval(() => {
      setTimeAgo(formatDistanceToNow(new Date(item.created_at), { addSuffix: true }))
    }, 1000)

    return () => clearInterval(interval)
  }, [item.created_at])

  const tweetUrl = `https://twitter.com/${item.twitter_user}/status/${item.tweet_id}`
  const profileUrl = `https://twitter.com/${item.twitter_user}`

  // Format follower count
  const formatFollowers = (count) => {
    if (count >= 1000000) return `${(count / 1000000).toFixed(1)}M`
    if (count >= 1000) return `${(count / 1000).toFixed(1)}K`
    return count.toString()
  }

  // Tweet text construction
  const tweetText = `Perfecto $${item.ticker} @memeXshot`

  return (
    <motion.div
      layout
      initial={{ opacity: 0, x: -50, scale: 0.9 }}
      animate={{ opacity: 1, x: 0, scale: 1 }}
      exit={{ opacity: 0, x: 50, scale: 0.9 }}
      transition={{ type: "spring", stiffness: 300, damping: 25 }}
      className="bg-white dark:bg-moonshot-primary border border-moonshot-primary/10 dark:border-moonshot-secondary/10 rounded-lg hover:bg-moonshot-primary/5 dark:hover:bg-moonshot-secondary/5 transition-colors group cursor-pointer relative overflow-hidden"
      onClick={() => window.open(tweetUrl, '_blank')}
    >
      {/* New tweet indicator */}
      <motion.div
        initial={{ scaleX: 0 }}
        animate={{ scaleX: 1 }}
        transition={{ duration: 0.5 }}
        className="absolute top-0 left-0 h-0.5 w-full bg-moonshot-accent"
      />
      
      <div className="p-2">
        <div className="flex items-start gap-2">
          {/* Profile Picture */}
          <a
            href={profileUrl}
            target="_blank"
            rel="noopener noreferrer"
            onClick={(e) => e.stopPropagation()}
            className="flex-shrink-0"
          >
            {item.profile_image_url ? (
              <img
                src={item.profile_image_url}
                alt={item.twitter_user}
                className="w-7 h-7 sm:w-8 sm:h-8 rounded-full hover:ring-2 hover:ring-moonshot-accent transition-all"
              />
            ) : (
              <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-full bg-moonshot-accent flex items-center justify-center">
                <span className="text-white text-[10px] sm:text-xs">
                  {item.twitter_user.charAt(0).toUpperCase()}
                </span>
              </div>
            )}
          </a>

          {/* Content */}
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between mb-0.5 sm:mb-1">
              <div className="flex items-center gap-1 sm:gap-2 flex-1 min-w-0">
                <span className="text-[11px] sm:text-xs text-moonshot-primary dark:text-white truncate">
                  {item.name || item.twitter_user}
                </span>
                <span className="text-[10px] sm:text-xs text-moonshot-primary/70 dark:text-white/70 hidden xs:inline">
                  @{item.twitter_user}
                </span>
              </div>
              <p className="text-[10px] sm:text-xs text-moonshot-primary/70 dark:text-white/70 flex-shrink-0">
                {timeAgo}
              </p>
            </div>
            
            {/* Tweet Text */}
            <p className="text-xs text-moonshot-primary dark:text-white mb-1">
              {tweetText}
            </p>
            
            {/* Bottom Info */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-1 sm:gap-2">
                <p className="font-mono text-xs sm:text-sm text-moonshot-primary dark:text-white">
                  ${item.ticker}
                </p>
                <span className="text-[10px] sm:text-xs text-moonshot-primary/70 dark:text-white/70 hidden xs:inline">
                  • {formatFollowers(item.followers_count || 0)} followers
                </span>
              </div>
              
              {/* Small Image Preview */}
              {item.image_url && (
                <img
                  src={item.image_url}
                  alt={`${item.ticker} token`}
                  className="w-6 h-6 rounded object-cover"
                />
              )}
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  )
}

const LiveFeed = () => {
  const { data: feedData } = useSupabaseRealtime('tweet_queue', {
    orderBy: { column: 'created_at', ascending: false },
    limit: 10
  })

  return (
    <div className="bg-white dark:bg-moonshot-primary rounded-3xl overflow-hidden h-[600px] relative border-2 border-moonshot-primary/20 dark:border-moonshot-secondary/20">
      <div className="bg-white dark:bg-moonshot-primary rounded-3xl overflow-hidden h-full">
        <div className="px-6 py-5 border-b border-moonshot-primary/10 dark:border-moonshot-secondary/10">
          <div className="flex items-center justify-between">
            <h2 className="text-xl text-moonshot-primary dark:text-white">Live Feed</h2>
            <div className="flex items-center gap-2">
              <motion.div
                animate={{
                  scale: [1, 1.5, 1],
                  opacity: [1, 0.5, 1],
                }}
                transition={{
                  duration: 2,
                  ease: "easeInOut",
                  repeat: Infinity,
                }}
                className="w-2 h-2 rounded-full bg-moonshot-success shadow-[0_0_8px_rgba(69,178,85,0.6)]"
              />
              <span className="text-xs text-moonshot-primary/70 dark:text-white/70">Live</span>
            </div>
          </div>
        </div>

      <div className="p-2 overflow-hidden h-[calc(100%-73px)] flex flex-col">
        <AnimatePresence mode="popLayout">
          {feedData.length === 0 ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex items-center justify-center h-full text-moonshot-primary/50 dark:text-white/50"
            >
              <p>No tweets yet...</p>
            </motion.div>
          ) : (
            <div className="space-y-1 flex flex-col">
              {feedData.map((item) => (
                <FeedItem key={item.id} item={item} />
              ))}
            </div>
          )}
        </AnimatePresence>
      </div>
      </div>
    </div>
  )
}

export default LiveFeed