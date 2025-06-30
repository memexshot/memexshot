#!/usr/bin/env python3
"""
Log Viewer for MemeXshot Automation
View and analyze logs from all services
"""

import os
import sys
import json
from datetime import datetime
import argparse

def view_master_log(log_dir, lines=50):
    """View the master log with important events"""
    master_log = os.path.join(log_dir, 'master.log')
    if not os.path.exists(master_log):
        print("❌ Master log not found. Run the services first.")
        return
    
    print("\n📋 MASTER LOG (Important Events)")
    print("="*80)
    
    with open(master_log, 'r') as f:
        all_lines = f.readlines()
        recent_lines = all_lines[-lines:]
        for line in recent_lines:
            print(line.strip())

def view_service_log(log_dir, service_name, lines=50):
    """View a specific service log"""
    service_log = os.path.join(log_dir, f"{service_name}.log")
    if not os.path.exists(service_log):
        print(f"❌ Log for {service_name} not found.")
        return
    
    print(f"\n📋 {service_name.upper()} LOG")
    print("="*80)
    
    with open(service_log, 'r') as f:
        all_lines = f.readlines()
        recent_lines = all_lines[-lines:]
        for line in recent_lines:
            print(line.strip())

def view_events(log_dir, event_type=None, service=None):
    """View structured events from JSON log"""
    events_log = os.path.join(log_dir, 'events.json')
    if not os.path.exists(events_log):
        print("❌ Events log not found.")
        return
    
    print("\n📊 EVENTS LOG")
    print("="*80)
    
    events = []
    with open(events_log, 'r') as f:
        for line in f:
            try:
                event = json.loads(line)
                events.append(event)
            except:
                pass
    
    # Filter events
    filtered_events = events
    if event_type:
        filtered_events = [e for e in filtered_events if event_type in e.get('message', '')]
    if service:
        filtered_events = [e for e in filtered_events if e.get('service') == service]
    
    # Show recent events
    for event in filtered_events[-50:]:
        timestamp = event.get('timestamp', 'Unknown')
        level = event.get('level', 'INFO')
        service = event.get('service', 'System')
        message = event.get('message', '')
        
        # Color based on level
        color = {
            'ERROR': '\033[91m',
            'WARNING': '\033[93m',
            'INFO': '\033[92m',
            'DEBUG': '\033[90m'
        }.get(level, '\033[0m')
        
        print(f"{color}[{timestamp}] [{service}] {level}: {message}\033[0m")
        
        # Show data if present
        if 'data' in event and event['data']:
            print(f"  Data: {json.dumps(event['data'], indent=2)}")

def analyze_logs(log_dir):
    """Analyze logs and show statistics"""
    events_log = os.path.join(log_dir, 'events.json')
    if not os.path.exists(events_log):
        print("❌ Events log not found.")
        return
    
    print("\n📈 LOG ANALYSIS")
    print("="*80)
    
    # Count events by type
    event_counts = {}
    service_counts = {}
    error_count = 0
    
    with open(events_log, 'r') as f:
        for line in f:
            try:
                event = json.loads(line)
                
                # Count by service
                service = event.get('service', 'Unknown')
                service_counts[service] = service_counts.get(service, 0) + 1
                
                # Count errors
                if event.get('level') == 'ERROR':
                    error_count += 1
                
                # Extract event type from message
                message = event.get('message', '')
                if '[EVENT]' in message:
                    event_type = message.split('[EVENT] ')[1].split(':')[0]
                    event_counts[event_type] = event_counts.get(event_type, 0) + 1
            except:
                pass
    
    print("\n🔢 Event Counts:")
    for event_type, count in sorted(event_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {event_type}: {count}")
    
    print("\n📊 Service Activity:")
    for service, count in sorted(service_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {service}: {count} events")
    
    print(f"\n❌ Total Errors: {error_count}")

def main():
    parser = argparse.ArgumentParser(description='View MemeXshot logs')
    parser.add_argument('--master', action='store_true', help='View master log')
    parser.add_argument('--service', type=str, help='View specific service log')
    parser.add_argument('--events', action='store_true', help='View events log')
    parser.add_argument('--analyze', action='store_true', help='Analyze logs')
    parser.add_argument('--lines', type=int, default=50, help='Number of lines to show')
    parser.add_argument('--filter', type=str, help='Filter events by keyword')
    
    args = parser.parse_args()
    
    # Get log directory
    log_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'logs'
    )
    
    if not os.path.exists(log_dir):
        print("❌ No logs directory found. Run the services first.")
        return
    
    if args.master:
        view_master_log(log_dir, args.lines)
    elif args.service:
        view_service_log(log_dir, args.service, args.lines)
    elif args.events:
        view_events(log_dir, event_type=args.filter)
    elif args.analyze:
        analyze_logs(log_dir)
    else:
        # Default: show summary
        print("\n🗂️  Available Logs:")
        print("="*50)
        for log_file in os.listdir(log_dir):
            if log_file.endswith('.log') or log_file.endswith('.json'):
                file_path = os.path.join(log_dir, log_file)
                size = os.path.getsize(file_path) / 1024  # KB
                print(f"  {log_file}: {size:.1f} KB")
        
        print("\n💡 Usage:")
        print("  python3 scripts/view_logs.py --master        # View important events")
        print("  python3 scripts/view_logs.py --events        # View structured events")
        print("  python3 scripts/view_logs.py --analyze       # Analyze logs")
        print("  python3 scripts/view_logs.py --service twitter_bot  # View service log")

if __name__ == "__main__":
    main()