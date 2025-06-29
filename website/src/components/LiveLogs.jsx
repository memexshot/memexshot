import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { ClockIcon, CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline'
import { useSupabaseRealtime } from '../hooks/useSupabaseRealtime'

const InfoBox = ({ successful, queued, failed }) => (
  <div className="absolute top-3 sm:top-4 right-3 sm:right-4 flex gap-1 sm:gap-2 text-xs sm:text-sm">
    <div className="flex items-center gap-1 sm:gap-2 px-2 sm:px-3 py-1 sm:py-1.5 rounded-full bg-moonshot-success/10 dark:bg-moonshot-success/20 backdrop-blur-sm border border-moonshot-success/20">
      <CheckCircleIcon className="w-3 h-3 sm:w-4 sm:h-4 text-moonshot-success" />
      <span className="hidden xs:inline text-[10px] sm:text-xs text-moonshot-primary/70 dark:text-white/70">Success</span>
      <span className="text-moonshot-primary dark:text-white">{successful}</span>
    </div>
    <div className="flex items-center gap-1 sm:gap-2 px-2 sm:px-3 py-1 sm:py-1.5 rounded-full bg-moonshot-secondary/10 border border-moonshot-secondary/20">
      <ClockIcon className="w-3 h-3 sm:w-4 sm:h-4 text-moonshot-accent" />
      <span className="hidden xs:inline text-[10px] sm:text-xs text-moonshot-primary/70 dark:text-white/70">Queue</span>
      <span className="text-moonshot-primary dark:text-white">{queued}</span>
    </div>
    <div className="flex items-center gap-1 sm:gap-2 px-2 sm:px-3 py-1 sm:py-1.5 rounded-full bg-red-500/10 dark:bg-red-500/20 backdrop-blur-sm border border-red-500/20">
      <XCircleIcon className="w-3 h-3 sm:w-4 sm:h-4 text-red-500" />
      <span className="hidden xs:inline text-[10px] sm:text-xs text-moonshot-primary/70 dark:text-white/70">Failed</span>
      <span className="text-moonshot-primary dark:text-white">{failed}</span>
    </div>
  </div>
)

const ProcessingToken = ({ token }) => {
  if (!token) {
    return (
      <div className="flex items-center justify-center h-full text-moonshot-primary/50 dark:text-white/50">
        <p className="text-sm sm:text-base">No token processing...</p>
      </div>
    )
  }

  const tweetUrl = `https://twitter.com/${token.twitter_user}/status/${token.tweet_id}`
  const profileUrl = `https://twitter.com/${token.twitter_user}`

  // Format follower count
  const formatFollowers = (count) => {
    if (count >= 1000000) return `${(count / 1000000).toFixed(1)}M`
    if (count >= 1000) return `${(count / 1000).toFixed(1)}K`
    return count.toString()
  }

  return (
    <div className="p-6">
      <div className="space-y-4">
        <div>
          <h4 className="text-sm text-moonshot-primary/70 dark:text-white/70 mb-3">
            Processing Token
          </h4>
          
          {/* User Info */}
          <div className="flex items-start gap-3 mb-4">
            {/* Profile Picture */}
            <a
              href={profileUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-shrink-0"
            >
              {token.profile_image_url ? (
                <img
                  src={token.profile_image_url}
                  alt={token.twitter_user}
                  className="w-14 h-14 rounded-full hover:ring-2 hover:ring-moonshot-accent transition-all"
                />
              ) : (
                <div className="w-14 h-14 rounded-full bg-moonshot-accent flex items-center justify-center">
                  <span className="text-white text-xl">
                    {token.twitter_user.charAt(0).toUpperCase()}
                  </span>
                </div>
              )}
            </a>

            {/* User Details */}
            <div className="flex-1">
              <a
                href={profileUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="text-moonshot-primary dark:text-white hover:text-moonshot-accent transition-colors"
              >
                {token.name || token.twitter_user}
              </a>
              <p className="text-sm text-moonshot-primary/70 dark:text-white/70">
                @{token.twitter_user} • {formatFollowers(token.followers_count || 0)} followers
              </p>
            </div>
          </div>

          {/* Token Info */}
          <div className="bg-moonshot-accent/10 rounded-xl p-4">
            <p className="text-3xl font-mono text-moonshot-primary dark:text-white">
              ${token.ticker}
            </p>
            <a
              href={tweetUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="text-sm text-moonshot-accent hover:text-moonshot-accent-hover hover:underline mt-1 inline-block transition-colors"
            >
              View Tweet →
            </a>
          </div>
        </div>
        
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-moonshot-primary/70 dark:text-white/70">Status</span>
            <span className="text-moonshot-accent">Processing...</span>
          </div>
        </div>

        <div className="relative pt-4">
          <div className="h-2 bg-moonshot-primary/10 dark:bg-moonshot-secondary/10 rounded-full overflow-hidden">
            <motion.div
              className="h-full bg-moonshot-accent"
              initial={{ width: 0 }}
              animate={{ width: '100%' }}
              transition={{ duration: 1.45, ease: "linear" }}
            />
          </div>
        </div>
      </div>
    </div>
  )
}

const QueueItem = ({ item, index, totalInQueue }) => {
  const estimatedTime = (index + 1) * 1.45 // 1.45 seconds per token
  const formatTime = (seconds) => {
    if (seconds < 60) return `${seconds.toFixed(0)}s`
    return `${(seconds / 60).toFixed(1)}m`
  }

  const tweetUrl = `https://twitter.com/${item.twitter_user}/status/${item.tweet_id}`
  const profileUrl = `https://twitter.com/${item.twitter_user}`

  // Format follower count
  const formatFollowers = (count) => {
    if (count >= 1000000) return `${(count / 1000000).toFixed(1)}M`
    if (count >= 1000) return `${(count / 1000).toFixed(1)}K`
    return count.toString()
  }

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      className="p-4 border-b border-moonshot-primary/5 dark:border-moonshot-secondary/5 hover:bg-moonshot-primary/5 dark:hover:bg-moonshot-secondary/5 transition-colors cursor-pointer"
      onClick={() => window.open(tweetUrl, '_blank')}
    >
      <div className="flex items-center justify-between gap-4">
        <div className="flex items-center gap-3 flex-1">
          <span className="text-sm text-moonshot-primary/50 dark:text-white/50 font-mono">
            #{index + 1}
          </span>
          
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
                className="w-10 h-10 rounded-full hover:ring-2 hover:ring-moonshot-accent transition-all"
              />
            ) : (
              <div className="w-10 h-10 rounded-full bg-moonshot-accent flex items-center justify-center">
                <span className="text-white text-sm">
                  {item.twitter_user.charAt(0).toUpperCase()}
                </span>
              </div>
            )}
          </a>
          
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <p className="font-mono text-moonshot-primary dark:text-white">
                ${item.ticker}
              </p>
              <span className="text-sm text-moonshot-primary/70 dark:text-white/70">
                by @{item.twitter_user}
              </span>
            </div>
            <p className="text-xs text-moonshot-primary/70 dark:text-white/70">
              {formatFollowers(item.followers_count || 0)} followers
            </p>
          </div>
        </div>
        
        <div className="text-right flex-shrink-0">
          <p className="text-sm text-moonshot-primary dark:text-white">
            ~{formatTime(estimatedTime)}
          </p>
          <p className="text-xs text-moonshot-primary/70 dark:text-white/70">
            estimated
          </p>
        </div>
      </div>
    </motion.div>
  )
}

const LiveLogs = () => {
  // Fetch queue data
  const { data: queueData } = useSupabaseRealtime('tweet_queue', {
    orderBy: { column: 'created_at', ascending: true }
  })

  // Filter queue items
  const queueItems = queueData.filter(item => item.status === 'queued')
  const processingItem = queueData.find(item => item.status === 'processing')
  
  // Calculate stats
  const stats = {
    successful: queueData.filter(item => item.status === 'completed').length,
    queued: queueItems.length,
    failed: queueData.filter(item => item.status === 'failed').length
  }

  return (
    <div className="bg-white dark:bg-moonshot-primary rounded-2xl sm:rounded-3xl overflow-hidden h-[400px] sm:h-[600px] relative border-2 border-moonshot-primary/20 dark:border-moonshot-secondary/20">
      <div className="bg-white dark:bg-moonshot-primary rounded-2xl sm:rounded-3xl overflow-hidden h-full">
        <InfoBox {...stats} />
        
        <div className="px-4 sm:px-6 py-3 sm:py-5 border-b border-moonshot-primary/10 dark:border-moonshot-secondary/10">
          <h2 className="text-lg sm:text-xl text-moonshot-primary dark:text-white">Live Activity</h2>
        </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 h-[calc(100%-73px)]">
        {/* Processing Section */}
        <div className="sm:border-r border-b sm:border-b-0 border-moonshot-primary/10 dark:border-moonshot-secondary/10">
          <ProcessingToken token={processingItem} />
        </div>

        {/* Queue Section */}
        <div className="overflow-y-auto">
          <div className="p-3 sm:p-4 border-b border-moonshot-primary/10 dark:border-moonshot-secondary/10 sticky top-0 bg-white dark:bg-moonshot-primary">
            <h3 className="text-sm sm:text-base text-moonshot-primary dark:text-white">
              Queue ({queueItems.length})
            </h3>
          </div>
          
          {queueItems.length === 0 ? (
            <div className="flex items-center justify-center h-64 text-moonshot-primary/50 dark:text-white/50">
              <p>Queue is empty</p>
            </div>
          ) : (
            queueItems.map((item, index) => (
              <QueueItem 
                key={item.id} 
                item={item} 
                index={index} 
                totalInQueue={queueItems.length} 
              />
            ))
          )}
        </div>
      </div>
      </div>
    </div>
  )
}

export default LiveLogs