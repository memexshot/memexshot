export const formatNumber = (num) => {
  return new Intl.NumberFormat('en-US').format(num)
}

export const formatTime = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleTimeString('en-US', { 
    hour: '2-digit', 
    minute: '2-digit',
    hour12: false 
  })
}

export const formatDate = (timestamp) => {
  const date = new Date(timestamp)
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric',
    year: 'numeric'
  })
}

export const formatPercentage = (value) => {
  return `${value.toFixed(1)}%`
}

export const truncateAddress = (address, length = 6) => {
  if (!address) return ''
  return `${address.slice(0, length)}...${address.slice(-length)}`
}