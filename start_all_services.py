#!/usr/bin/env python3
"""
Start All Services - Moonshot Automation System
Launches all required services in separate processes
"""

import os
import sys
import time
import subprocess
import signal
from datetime import datetime

class ServiceManager:
    def __init__(self):
        self.processes = []
        self.services = [
            {
                'name': 'Twitter Bot',
                'command': ['python3', 'services/twitter_bot.py'],
                'color': '\033[94m'  # Blue
            },
            {
                'name': 'Queue Worker',
                'command': ['python3', 'services/queue_worker.py'],
                'color': '\033[93m'  # Yellow
            },
            {
                'name': 'Photo Sync',
                'command': ['python3', 'services/auto_photo_sync.py'],
                'color': '\033[92m'  # Green
            },
            {
                'name': 'Supabase Listener',
                'command': ['python3', 'automation/supabase_listener_polling.py'],
                'color': '\033[95m'  # Magenta
            }
        ]
        
    def log(self, message, color='\033[0m'):
        """Log with timestamp and color"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{color}[{timestamp}] {message}\033[0m")
        
    def start_service(self, service):
        """Start a single service"""
        try:
            # Start process with output piped
            process = subprocess.Popen(
                service['command'],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1,
                preexec_fn=os.setsid  # Create new process group
            )
            
            self.processes.append({
                'name': service['name'],
                'process': process,
                'color': service['color']
            })
            
            self.log(f"✅ Started: {service['name']}", service['color'])
            return True
            
        except Exception as e:
            self.log(f"❌ Failed to start {service['name']}: {e}", '\033[91m')
            return False
    
    def monitor_output(self):
        """Monitor output from all services"""
        import select
        
        # Create a mapping of file descriptors to services
        fd_to_service = {}
        for proc_info in self.processes:
            if proc_info['process'].stdout:
                fd = proc_info['process'].stdout.fileno()
                fd_to_service[fd] = proc_info
        
        self.log("\n📊 Monitoring all services... (Press Ctrl+C to stop all)\n")
        
        try:
            while True:
                # Check which processes have output ready
                readable, _, _ = select.select(list(fd_to_service.keys()), [], [], 0.1)
                
                for fd in readable:
                    service_info = fd_to_service[fd]
                    line = service_info['process'].stdout.readline()
                    
                    if line:
                        # Print with service-specific color
                        print(f"{service_info['color']}[{service_info['name']}] {line.strip()}\033[0m")
                
                # Check if any process has died
                for i, proc_info in enumerate(self.processes):
                    if proc_info['process'].poll() is not None:
                        self.log(f"⚠️  {proc_info['name']} has stopped!", '\033[91m')
                        # Restart the service
                        self.log(f"🔄 Restarting {proc_info['name']}...", proc_info['color'])
                        service = next(s for s in self.services if s['name'] == proc_info['name'])
                        if self.start_service(service):
                            # Update the process list
                            self.processes[i] = self.processes[-1]
                            self.processes.pop()
                            # Update fd mapping
                            fd_to_service = {}
                            for proc_info in self.processes:
                                if proc_info['process'].stdout:
                                    fd = proc_info['process'].stdout.fileno()
                                    fd_to_service[fd] = proc_info
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            self.log("\n🛑 Stopping all services...", '\033[91m')
            self.stop_all()
    
    def stop_all(self):
        """Stop all running services"""
        for proc_info in self.processes:
            try:
                # Send SIGTERM to the process group
                os.killpg(os.getpgid(proc_info['process'].pid), signal.SIGTERM)
                self.log(f"⏹️  Stopped: {proc_info['name']}", proc_info['color'])
            except Exception as e:
                self.log(f"⚠️  Error stopping {proc_info['name']}: {e}", '\033[91m')
        
        # Wait for all processes to terminate
        for proc_info in self.processes:
            try:
                proc_info['process'].wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if needed
                proc_info['process'].kill()
                
        self.log("✅ All services stopped", '\033[92m')
    
    def run(self):
        """Main run method"""
        self.log("🚀 MOONSHOT AUTOMATION SYSTEM", '\033[96m')
        self.log("="*50)
        
        # Check if we're in test mode
        if os.path.exists('tests/TEST_MODE_CHANGES.md'):
            self.log("⚠️  TEST MODE ACTIVE - Using 'Perfecto' pattern", '\033[93m')
            self.log("⚠️  Follower check disabled (0 minimum)", '\033[93m')
            self.log("="*50)
        
        # Start all services
        self.log("\n🔧 Starting services...")
        
        success_count = 0
        for service in self.services:
            if self.start_service(service):
                success_count += 1
            time.sleep(1)  # Small delay between starts
        
        if success_count == len(self.services):
            self.log(f"\n✅ All {success_count} services started successfully!", '\033[92m')
            
            # Show test instructions if in test mode
            if os.path.exists('tests/TEST_MODE_CHANGES.md'):
                self.log("\n📱 TEST INSTRUCTIONS:", '\033[93m')
                self.log("Tweet format: Perfecto $TICKER @memeXshot + image", '\033[93m')
                self.log("Example: Perfecto $TEST @memeXshot", '\033[93m')
            
            # Monitor output
            self.monitor_output()
        else:
            self.log(f"\n❌ Only {success_count}/{len(self.services)} services started", '\033[91m')
            self.log("Stopping all services...", '\033[91m')
            self.stop_all()

if __name__ == "__main__":
    # Change to script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    manager = ServiceManager()
    
    try:
        manager.run()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        manager.stop_all()
    finally:
        sys.exit(0)