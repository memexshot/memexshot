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
import logging
from logging.handlers import RotatingFileHandler
import json
import threading

class ServiceManager:
    def __init__(self):
        self.processes = []
        self.setup_logging()
        self.services = [
            {
                'name': 'Twitter Bot',
                'command': ['python3', 'scripts/services/twitter_bot.py'],
                'color': '\033[94m'  # Blue
            },
            {
                'name': 'Queue Worker',
                'command': ['python3', 'scripts/services/queue_worker.py'],
                'color': '\033[93m'  # Yellow
            },
            {
                'name': 'Photo Sync',
                'command': ['python3', 'scripts/services/auto_photo_sync.py'],
                'color': '\033[92m'  # Green
            },
            {
                'name': 'Supabase Listener',
                'command': ['python3', 'scripts/automation/supabase_listener_polling.py'],
                'color': '\033[95m'  # Magenta
            }
        ]
        
    def setup_logging(self):
        """Setup comprehensive logging system"""
        # Create logs directory
        self.log_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'logs'
        )
        os.makedirs(self.log_dir, exist_ok=True)
        
        # Setup main logger
        self.logger = logging.getLogger('ServiceManager')
        self.logger.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%H:%M:%S')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # Master log file - All important events
        master_handler = RotatingFileHandler(
            os.path.join(self.log_dir, 'master.log'),
            maxBytes=50*1024*1024,  # 50MB
            backupCount=10
        )
        master_handler.setLevel(logging.INFO)
        master_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        master_handler.setFormatter(master_formatter)
        self.logger.addHandler(master_handler)
        
        # Detailed log file - Everything including debug
        detailed_handler = RotatingFileHandler(
            os.path.join(self.log_dir, 'detailed.log'),
            maxBytes=100*1024*1024,  # 100MB
            backupCount=5
        )
        detailed_handler.setLevel(logging.DEBUG)
        detailed_handler.setFormatter(master_formatter)
        self.logger.addHandler(detailed_handler)
        
        # JSON log for structured data
        json_handler = RotatingFileHandler(
            os.path.join(self.log_dir, 'events.json'),
            maxBytes=100*1024*1024,  # 100MB
            backupCount=5
        )
        json_handler.setLevel(logging.DEBUG)
        self.json_handler = json_handler
        self.logger.addHandler(json_handler)
        
        # Service-specific log files
        self.service_loggers = {}
        
    def log(self, message, color='\033[0m', level=logging.INFO, service=None, data=None):
        """Enhanced logging with multiple outputs"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Console output with color
        print(f"{color}[{timestamp}] {message}\033[0m")
        
        # File logging
        if service:
            full_message = f"[{service}] {message}"
        else:
            full_message = message
            
        self.logger.log(level, full_message)
        
        # JSON logging for structured data
        if data or service:
            json_event = {
                'timestamp': timestamp,
                'level': logging.getLevelName(level),
                'message': message,
                'service': service,
                'data': data
            }
            self.json_handler.emit(logging.LogRecord(
                name='ServiceManager',
                level=level,
                pathname='',
                lineno=0,
                msg=json.dumps(json_event, ensure_ascii=False),
                args=(),
                exc_info=None
            ))
        
    def start_service(self, service):
        """Start a single service"""
        try:
            # Create service-specific log file
            service_log_path = os.path.join(self.log_dir, f"{service['name'].lower().replace(' ', '_')}.log")
            service_log = open(service_log_path, 'a')
            
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
                'color': service['color'],
                'log_file': service_log
            })
            
            self.log(f"✅ Started: {service['name']}", service['color'], 
                    service=service['name'], data={'pid': process.pid, 'command': ' '.join(service['command'])})
            return True
            
        except Exception as e:
            self.log(f"❌ Failed to start {service['name']}: {e}", '\033[91m',
                    level=logging.ERROR, service=service['name'], data={'error': str(e)})
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
                        
                        # Write to service-specific log file
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        service_info['log_file'].write(f"[{timestamp}] {line}")
                        service_info['log_file'].flush()
                        
                        # Log important events to master log
                        self.parse_and_log_event(service_info['name'], line.strip())
                
                # Check if any process has died
                for i, proc_info in enumerate(self.processes):
                    if proc_info['process'].poll() is not None:
                        exit_code = proc_info['process'].returncode
                        self.log(f"⚠️  {proc_info['name']} has stopped! Exit code: {exit_code}", '\033[91m',
                                level=logging.WARNING, service=proc_info['name'], 
                                data={'exit_code': exit_code})
                        # Restart the service
                        self.log(f"🔄 Restarting {proc_info['name']}...", proc_info['color'],
                                service=proc_info['name'])
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
            self.log("\n🛑 Stopping all services...", '\033[91m', 
                    level=logging.INFO, data={'reason': 'user_interrupt'})
            self.stop_all()
    
    def parse_and_log_event(self, service_name, line):
        """Parse service output and log important events"""
        # Define important event patterns
        events = {
            'Twitter Bot': {
                '🔍 Found': ('tweet_found', logging.INFO),
                '✅ Added to queue': ('tweet_queued', logging.INFO),
                '❌ Rate limit reached': ('rate_limit', logging.WARNING),
                '❌ Error': ('error', logging.ERROR),
                'Rate limit exceeded': ('api_rate_limit', logging.WARNING),
                '⚠️  Invalid format': ('invalid_tweet', logging.DEBUG)
            },
            'Queue Worker': {
                '✅ Moved to processing': ('coin_created', logging.INFO),
                '⚠️  Coin already exists': ('duplicate_coin', logging.WARNING),
                '📭 No tweets in queue': ('queue_empty', logging.DEBUG),
                '❌ Error': ('error', logging.ERROR)
            },
            'Photo Sync': {
                '✅ Successfully synced': ('photo_synced', logging.INFO),
                '📥 Downloading image': ('photo_download', logging.DEBUG),
                '❌ Error': ('error', logging.ERROR),
                '⚠️': ('warning', logging.WARNING)
            },
            'Supabase Listener': {
                '🆕 Found': ('new_coin_detected', logging.INFO),
                '🔄 Processing coin': ('automation_start', logging.INFO),
                '✅ Successfully processed': ('automation_success', logging.INFO),
                '❌ Failed to process': ('automation_failed', logging.ERROR),
                '⏱️  Starting in': ('automation_countdown', logging.DEBUG)
            }
        }
        
        # Check for important events
        if service_name in events:
            for pattern, (event_type, level) in events[service_name].items():
                if pattern in line:
                    # Extract relevant data from the line
                    data = {'raw_line': line}
                    
                    # Try to extract specific data based on event type
                    if event_type == 'tweet_found' and 'Found' in line:
                        try:
                            count = line.split('Found ')[1].split(' ')[0]
                            data['tweet_count'] = int(count)
                        except:
                            pass
                    
                    elif event_type == 'tweet_queued' and 'Added to queue:' in line:
                        try:
                            ticker = line.split('Added to queue: ')[1].split(' ')[0]
                            data['ticker'] = ticker
                        except:
                            pass
                    
                    elif event_type == 'coin_created' and 'Moved to processing:' in line:
                        try:
                            parts = line.split('Moved to processing: ')[1]
                            ticker = parts.split(' from @')[0]
                            user = parts.split(' from @')[1]
                            data['ticker'] = ticker
                            data['user'] = user
                        except:
                            pass
                    
                    # Log the event
                    self.log(f"[EVENT] {event_type}: {line}", self.services[0]['color'],
                            level=level, service=service_name, data=data)
                    break
    
    def stop_all(self):
        """Stop all running services"""
        for proc_info in self.processes:
            try:
                # Send SIGTERM to the process group
                os.killpg(os.getpgid(proc_info['process'].pid), signal.SIGTERM)
                self.log(f"⏹️  Stopped: {proc_info['name']}", proc_info['color'],
                        service=proc_info['name'], data={'pid': proc_info['process'].pid})
                # Close log file
                proc_info['log_file'].close()
            except Exception as e:
                self.log(f"⚠️  Error stopping {proc_info['name']}: {e}", '\033[91m',
                        level=logging.WARNING, service=proc_info['name'])
        
        # Wait for all processes to terminate
        for proc_info in self.processes:
            try:
                proc_info['process'].wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if needed
                proc_info['process'].kill()
                
        self.log("✅ All services stopped", '\033[92m', 
                data={'total_services': len(self.processes)})
        
        # Log summary
        self.log_summary()
    
    def log_summary(self):
        """Log a summary of the session"""
        self.log("\n📊 SESSION SUMMARY", '\033[96m')
        self.log("="*50)
        self.log(f"Log files created in: {self.log_dir}")
        self.log("- master.log: Important events only")
        self.log("- detailed.log: All debug information")
        self.log("- events.json: Structured event data")
        self.log("- [service_name].log: Individual service logs")
        
    def run(self):
        """Main run method"""
        self.log("🚀 MOONSHOT AUTOMATION SYSTEM", '\033[96m')
        self.log("="*50)
        self.log(f"📁 Logs will be saved to: {self.log_dir}", '\033[93m')
        
        # Production mode
        
        # Start all services
        self.log("\n🔧 Starting services...")
        
        success_count = 0
        for service in self.services:
            if self.start_service(service):
                success_count += 1
            time.sleep(1)  # Small delay between starts
        
        if success_count == len(self.services):
            self.log(f"\n✅ All {success_count} services started successfully!", '\033[92m',
                    data={'services_started': success_count})
            
            # Production mode - no special instructions
            
            # Monitor output
            self.monitor_output()
        else:
            self.log(f"\n❌ Only {success_count}/{len(self.services)} services started", '\033[91m')
            self.log("Stopping all services...", '\033[91m')
            self.stop_all()

if __name__ == "__main__":
    # Change to moonshot_automation directory (parent of scripts)
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(script_dir)
    
    manager = ServiceManager()
    
    try:
        manager.run()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        manager.stop_all()
    finally:
        sys.exit(0)