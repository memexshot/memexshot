import React, { useState, useEffect } from 'react'
import { getTokenPrice, formatMarketCap, TOKEN_MINTS } from '../services/jupiter'

const TokenPrice = ({ mintAddress, size = 'sm' }) => {
  const [price, setPrice] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let interval

    const fetchPrice = async () => {
      try {
        // For now, all tokens use MXS price
        const tokenPrice = await getTokenPrice(TOKEN_MINTS.MXS)
        setPrice(tokenPrice)
        setLoading(false)
      } catch (error) {
        console.error('Error fetching token price:', error)
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
  }, [mintAddress])

  const textSize = size === 'sm' ? 'text-sm' : 'text-base'

  return (
    <span className={`${textSize} text-moonshot-primary dark:text-white`}>
      {loading ? '...' : formatMarketCap(price || 0)}
    </span>
  )
}

export default TokenPrice