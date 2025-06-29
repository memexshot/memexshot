import React from 'react'
import Header from './components/Header'
import LiveLogs from './components/LiveLogs'
import LiveFeed from './components/LiveFeed'
import LiveCoins from './components/LiveCoins'
import Footer from './components/Footer'

function App() {
  return (
    <div className="min-h-screen flex flex-col bg-white dark:bg-moonshot-primary transition-colors">
      
      <Header />
      
      <main className="relative flex-1 p-3 sm:p-6">
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-3 sm:gap-6 mb-3 sm:mb-6">
          {/* Live Logs - 2 column span */}
          <div className="xl:col-span-2">
            <LiveLogs />
          </div>
          
          {/* Live Feed - 1 column */}
          <div className="xl:col-span-1">
            <LiveFeed />
          </div>
        </div>
        
        {/* Live Coins - Full width */}
        <LiveCoins />
      </main>
      
      <Footer />
    </div>
  )
}

export default App