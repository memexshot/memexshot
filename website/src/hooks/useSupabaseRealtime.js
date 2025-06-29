import { useEffect, useState } from 'react'
import { supabase } from '../utils/supabase'

export const useSupabaseRealtime = (table, options = {}) => {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        let query = supabase.from(table).select('*')
        
        if (options.orderBy) {
          query = query.order(options.orderBy.column, { 
            ascending: options.orderBy.ascending || false 
          })
        }
        
        if (options.limit) {
          query = query.limit(options.limit)
        }

        const { data: initialData, error } = await query
        
        if (error) throw error
        setData(initialData || [])
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchInitialData()

    // Setup realtime subscription
    const channel = supabase
      .channel(`${table}-channel`)
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table },
        (payload) => {
          if (payload.eventType === 'INSERT') {
            setData(prev => [payload.new, ...prev].slice(0, options.limit || 50))
          } else if (payload.eventType === 'UPDATE') {
            setData(prev => prev.map(item => 
              item.id === payload.new.id ? payload.new : item
            ))
          } else if (payload.eventType === 'DELETE') {
            setData(prev => prev.filter(item => item.id !== payload.old.id))
          }
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [table, options.orderBy, options.limit])

  return { data, loading, error }
}