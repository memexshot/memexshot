#!/usr/bin/env python3
"""
Centralized Logging System for MemeXshot Automation
"""

import os
import sys
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
import json

class ColorFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    grey = "\x1b[38;20m"
    green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    blue = "\x1b[34;20m"
    magenta = "\x1b[35;20m"
    cyan = "\x1b[36;20m"
    reset = "\x1b[0m"
    
    FORMATS = {
        logging.DEBUG: grey + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset,
        logging.INFO: blue + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset,
        logging.WARNING: yellow + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset,
        logging.ERROR: red + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset,
        logging.CRITICAL: bold_red + "%(asctime)s - %(name)s - %(levelname)s - %(message)s" + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt='%Y-%m-%d %H:%M:%S')
        return formatter.format(record)

class JsonFormatter(logging.Formatter):
    """JSON formatter for structured logging"""
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'service': record.name,
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add extra fields if present
        if hasattr(record, 'extra_data'):
            log_data['data'] = record.extra_data
            
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
            
        return json.dumps(log_data)

def setup_logger(service_name, log_level=logging.INFO):
    """
    Setup logger for a service with both console and file output
    
    Args:
        service_name: Name of the service (e.g., 'twitter_bot', 'queue_worker')
        log_level: Logging level (default: INFO)
    
    Returns:
        Logger instance
    """
    # Create logger
    logger = logging.getLogger(service_name)
    logger.setLevel(log_level)
    
    # Remove existing handlers
    logger.handlers = []
    
    # Create logs directory
    log_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'logs'
    )
    os.makedirs(log_dir, exist_ok=True)
    
    # Console handler with color
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(ColorFormatter())
    logger.addHandler(console_handler)
    
    # File handler for service-specific log
    service_log_file = os.path.join(log_dir, f'{service_name}.log')
    file_handler = RotatingFileHandler(
        service_log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    logger.addHandler(file_handler)
    
    # Combined JSON log for all services
    combined_log_file = os.path.join(log_dir, 'combined.json')
    json_handler = RotatingFileHandler(
        combined_log_file,
        maxBytes=50*1024*1024,  # 50MB
        backupCount=10
    )
    json_handler.setLevel(logging.DEBUG)
    json_handler.setFormatter(JsonFormatter())
    logger.addHandler(json_handler)
    
    # Master log for important events
    master_log_file = os.path.join(log_dir, 'master.log')
    master_handler = RotatingFileHandler(
        master_log_file,
        maxBytes=20*1024*1024,  # 20MB
        backupCount=5
    )
    master_handler.setLevel(logging.INFO)
    master_handler.setFormatter(logging.Formatter(
        '%(asctime)s - [%(name)s] %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))
    logger.addHandler(master_handler)
    
    return logger

def log_event(logger, event_type, data=None, level=logging.INFO):
    """
    Log a structured event
    
    Args:
        logger: Logger instance
        event_type: Type of event (e.g., 'tweet_found', 'coin_created')
        data: Additional data to log
        level: Log level
    """
    message = f"[{event_type}] "
    if data:
        if isinstance(data, dict):
            message += json.dumps(data, ensure_ascii=False)
        else:
            message += str(data)
    
    # Add extra data for JSON formatter
    extra = {'extra_data': data} if data else {}
    
    logger.log(level, message, extra=extra)

# Service-specific log categories
LOG_EVENTS = {
    # Twitter Bot events
    'TWEET_SEARCH': 'tweet_search',
    'TWEET_FOUND': 'tweet_found',
    'TWEET_INVALID': 'tweet_invalid',
    'RATE_LIMIT_CHECK': 'rate_limit_check',
    'RATE_LIMIT_EXCEEDED': 'rate_limit_exceeded',
    'TWEET_QUEUED': 'tweet_queued',
    
    # Queue Worker events
    'QUEUE_CHECK': 'queue_check',
    'QUEUE_PROCESSING': 'queue_processing',
    'COIN_CREATED': 'coin_created',
    'COIN_EXISTS': 'coin_exists',
    'QUEUE_EMPTY': 'queue_empty',
    
    # Photo Sync events
    'PHOTO_SYNC_CHECK': 'photo_sync_check',
    'PHOTO_DOWNLOADING': 'photo_downloading',
    'PHOTO_IMPORTED': 'photo_imported',
    'PHOTO_SYNC_FAILED': 'photo_sync_failed',
    
    # Supabase Listener events
    'LISTENER_CHECK': 'listener_check',
    'AUTOMATION_START': 'automation_start',
    'AUTOMATION_SUCCESS': 'automation_success',
    'AUTOMATION_FAILED': 'automation_failed',
    
    # Wallet Monitor events
    'WALLET_CHECK': 'wallet_check',
    'SWAP_DETECTED': 'swap_detected',
    'REPLY_SENT': 'reply_sent',
    'REPLY_FAILED': 'reply_failed',
    
    # System events
    'SERVICE_START': 'service_start',
    'SERVICE_STOP': 'service_stop',
    'ERROR': 'error',
    'DATABASE_ERROR': 'database_error',
    'API_ERROR': 'api_error'
}

# Example usage
if __name__ == "__main__":
    # Test logger
    logger = setup_logger('test_service')
    
    logger.info("Test info message")
    logger.warning("Test warning message")
    logger.error("Test error message")
    
    # Test structured logging
    log_event(logger, LOG_EVENTS['TWEET_FOUND'], {
        'ticker': 'PEPE',
        'user': 'testuser',
        'followers': 1000
    })