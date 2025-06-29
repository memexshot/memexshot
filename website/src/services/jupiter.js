const JUPITER_API_URL = 'https://lite-api.jup.ag/price/v2'

// Token mint addresses
export const TOKEN_MINTS = {
  SOL: 'So11111111111111111111111111111111111111112', // Wrapped SOL
  MXS: 'hxcxN81ma8m5PMzPuCyysaMJ9wqJenBr811DbX4moon'
}

// Cache for token prices
const priceCache = new Map()
const CACHE_DURATION = 10000 // 10 seconds

// Total supply for marketcap calculation (1 billion for all SPL tokens)
const TOTAL_SUPPLY = 1_000_000_000

export async function getTokenPrice(mintAddress) {
  try {
    // Check cache first
    const cached = priceCache.get(mintAddress)
    if (cached && Date.now() - cached.timestamp < CACHE_DURATION) {
      return cached.price
    }

    // Fetch from Jupiter API
    const response = await fetch(`${JUPITER_API_URL}?ids=${mintAddress}`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    
    // Extract price from response
    let price = 0
    if (data && data.data && data.data[mintAddress]) {
      price = data.data[mintAddress].price || 0
    }

    priceCache.set(mintAddress, { price, timestamp: Date.now() })
    return price
  } catch (error) {
    console.error('Error fetching token price from Jupiter:', error)
    // Return fallback prices
    if (mintAddress === TOKEN_MINTS.SOL) return 150.00
    if (mintAddress === TOKEN_MINTS.MXS) return 0.0234
    return 0
  }
}

export async function getTokenPrices(mintAddresses) {
  try {
    // Join mint addresses with comma
    const ids = mintAddresses.join(',')
    
    // Check cache for all tokens
    const cached = {}
    const uncached = []
    
    for (const mint of mintAddresses) {
      const cachedData = priceCache.get(mint)
      if (cachedData && Date.now() - cachedData.timestamp < CACHE_DURATION) {
        cached[mint] = cachedData.price
      } else {
        uncached.push(mint)
      }
    }
    
    // If all are cached, return cached data
    if (uncached.length === 0) {
      return cached
    }
    
    // Fetch uncached prices from Jupiter API
    const response = await fetch(`${JUPITER_API_URL}?ids=${uncached.join(',')}`)
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    const data = await response.json()
    
    // Extract prices and update cache
    const prices = { ...cached }
    
    if (data && data.data) {
      for (const mint of uncached) {
        const price = data.data[mint]?.price || 0
        prices[mint] = price
        priceCache.set(mint, { price, timestamp: Date.now() })
      }
    }
    
    return prices
  } catch (error) {
    console.error('Error fetching token prices from Jupiter:', error)
    // Return fallback prices
    const fallback = {}
    for (const mint of mintAddresses) {
      if (mint === TOKEN_MINTS.SOL) fallback[mint] = 150.00
      else if (mint === TOKEN_MINTS.MXS) fallback[mint] = 0.0234
      else fallback[mint] = 0
    }
    return fallback
  }
}

export function formatPrice(price) {
  if (price >= 1) {
    return `$${price.toFixed(2)}`
  } else if (price >= 0.01) {
    return `$${price.toFixed(4)}`
  } else {
    return `$${price.toFixed(6)}`
  }
}

export function formatMarketCap(price) {
  const marketCap = price * TOTAL_SUPPLY
  
  if (marketCap >= 1_000_000_000) {
    return `$${(marketCap / 1_000_000_000).toFixed(2)}B`
  } else if (marketCap >= 1_000_000) {
    return `$${(marketCap / 1_000_000).toFixed(2)}M`
  } else if (marketCap >= 1_000) {
    return `$${(marketCap / 1_000).toFixed(2)}K`
  } else {
    return `$${marketCap.toFixed(2)}`
  }
}

export function shortenAddress(address, chars = 3) {
  if (!address) return ''
  return `${address.slice(0, chars)}...${address.slice(-chars)}`
}