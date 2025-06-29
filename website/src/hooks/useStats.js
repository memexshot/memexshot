import { useEffect, useState } from 'react'
import { supabase } from '../utils/supabase'

export const useStats = () => {
  const [stats, setStats] = useState({
    totalCoins: 0,
    dailyCoins: 0,
    activeUsers: 0,
    successRate: 0
  })
  const [loading, setLoading] = useState(true)

  const fetchStats = async () => {
    try {
      // Get total coins
      const { count: totalCoins } = await supabase
        .from('coins')
        .select('*', { count: 'exact', head: true })

      // Get 24h coins
      const yesterday = new Date()
      yesterday.setHours(yesterday.getHours() - 24)
      
      const { count: dailyCoins } = await supabase
        .from('coins')
        .select('*', { count: 'exact', head: true })
        .gte('created_at', yesterday.toISOString())

      // Get active users (unique users in last 24h)
      const { data: activeUsersData } = await supabase
        .from('coins')
        .select('twitter_user')
        .gte('created_at', yesterday.toISOString())
      
      const uniqueUsers = new Set(activeUsersData?.map(d => d.twitter_user) || [])
      const activeUsers = uniqueUsers.size

      // Calculate success rate
      const { count: successCount } = await supabase
        .from('coins')
        .select('*', { count: 'exact', head: true })
        .eq('status', 'completed')

      const successRate = totalCoins > 0 ? (successCount / totalCoins) * 100 : 0

      setStats({
        totalCoins: totalCoins || 0,
        dailyCoins: dailyCoins || 0,
        activeUsers,
        successRate
      })
    } catch (error) {
      console.error('Error fetching stats:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchStats()
    
    // Refresh stats every 30 seconds
    const interval = setInterval(fetchStats, 30000)
    
    return () => clearInterval(interval)
  }, [])

  return { stats, loading }
}