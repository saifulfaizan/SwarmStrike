#!/usr/bin/env python3
"""
🔐 SECURE ENVIRONMENT SETUP
=========================
Sets up a secure environment for the Unified Cybersecurity Framework.

Options:
    --secure: Apply enhanced security measures
    --env=<environment>: Set environment type (development, testing, production)
"""

import sys
import os
import argparse
import logging
import json
import secrets
import hashlib
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_argument_parser():
    """Set up command line argument parser"""
    parser = argparse.ArgumentParser(description='Set up a secure environment for the Unified Cybersecurity Framework')
    parser.add_argument('--secure', action='store_true', help='Apply enhanced security measures')
    parser.add_argument('--env', choices=['development', 'testing', 'production'], 
                        default='development', help='Set environment type')
    return parser

def create_secure_config(environment: str):
    """Create a secure configuration file"""
    config = {
        "environment": environment,
        "api_keys": {
            "primary": secrets.token_hex(32),
            "secondary": secrets.token_hex(32)
        },
        "security": {
            "encryption_key": secrets.token_hex(32),
            "signing_key": secrets.token_hex(32),
            "api_rate_limit": 1000 if environment == "production" else 5000,
            "max_connections": 100 if environment == "production" else 500,
            "secure_mode": True if environment == "production" else False
        },
        "logging": {
            "level": "INFO" if environment == "production" else "DEBUG",
            "file": "framework.log",
            "rotate_size_mb": 10,
            "keep_logs_days": 30
        },
        "timestamps": {
            "created": datetime.now().isoformat(),
            "expires": None
        }
    }
    
    # Write config to file
    with open("secure_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    logger.info(f"Secure configuration created for {environment} environment")
    return config

def setup_security_measures():
    """Set up additional security measures"""
    # Create secure directories
    os.makedirs("secure_logs", exist_ok=True)
    os.makedirs("secure_keys", exist_ok=True)
    os.makedirs("secure_data", exist_ok=True)
    
    # Generate a sample secure key
    with open("secure_keys/master.key", "w") as f:
        f.write(secrets.token_hex(32))
    
    logger.info("Security measures implemented")

def setup_environment(args):
    """Set up the environment based on command line arguments"""
    logger.info(f"Setting up {args.env} environment with {'enhanced' if args.secure else 'standard'} security...")
    
    # Create configuration
    config = create_secure_config(args.env)
    
    # Apply enhanced security if requested
    if args.secure:
        setup_security_measures()
    
    print("\n" + "="*70)
    print("🔐 SECURE ENVIRONMENT SETUP COMPLETE")
    print("="*70)
    print(f"Environment: {args.env.upper()}")
    print(f"Security level: {'ENHANCED' if args.secure else 'STANDARD'}")
    print(f"Configuration: secure_config.json")
    print("="*70 + "\n")
    
    return config

if __name__ == "__main__":
    parser = setup_argument_parser()
    args = parser.parse_args()
    config = setup_environment(args)