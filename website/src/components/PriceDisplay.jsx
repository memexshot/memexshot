import React, { useState, useEffect } from 'react'
import { getTokenPrice, formatMarketCap, TOKEN_MINTS } from '../services/jupiter'

const PriceDisplay = ({ token, symbol }) => {
  const [price, setPrice] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let interval

    const fetchPrice = async () => {
      try {
        const tokenPrice = await getTokenPrice(TOKEN_MINTS[token])
        setPrice(tokenPrice)
        setLoading(false)
      } catch (error) {
        console.error(`Error fetching ${token} price:`, error)
        setLoading(false)
      }
    }

    // Initial fetch
    fetchPrice()

    // Set up interval for updates
    interval = setInterval(fetchPrice, 10000) // 10 seconds

    return () => {
      if (interval) clearInterval(interval)
    }
  }, [token])

  return (
    <div className="flex items-center gap-1.5">
      <span className="text-xs text-moonshot-primary/70 dark:text-white/70">
        {symbol}:
      </span>
      <span className="text-xs text-moonshot-primary dark:text-white">
        {loading ? '...' : formatMarketCap(price || 0)}
      </span>
    </div>
  )
}

export default PriceDisplay