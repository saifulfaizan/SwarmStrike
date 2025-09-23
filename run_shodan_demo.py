#!/usr/bin/env python3
"""
🎯 SHODAN DEMONSTRATION SCRIPT
=============================
Demonstrates the usage of enhanced Shodan penetration testing framework
with different phases of testing
"""

import os
import sys
import json
import argparse
import logging
from shodan_pentest_enhanced import run_shodan_pentest

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_parser():
    """Set up the command line argument parser"""
    parser = argparse.ArgumentParser(description='Demonstrate Shodan penetration testing phases')
    parser.add_argument('--demo-type', choices=['quick', 'full', 'stealth', 'focused', 'real'], 
                        default='quick', help='Type of demo to run')
    parser.add_argument('--target', help='Optional specific target IP for focused demo')
    parser.add_argument('--query', help='Custom Shodan query to use for real demo')
    return parser

def run_quick_demo():
    """Run a quick demo of all 6 phases with a simulated target"""
    logger.info("=== RUNNING QUICK DEMO ===")
    logger.info("This demo will test all 6 phases with a simulated target")
    
    # Run with medium intensity and test all phases
    result = run_shodan_pentest(
        target=None,  # Will use simulation
        intensity=5,
        stealth_mode=False,
        test_all_phases=True
    )
    return result

def run_full_demo():
    """Run a comprehensive demo with multiple targets and high intensity"""
    logger.info("=== RUNNING FULL DEMO ===")
    logger.info("This demo will test all 6 phases with multiple simulated targets at high intensity")
    
    # Run with high intensity and test all phases
    result = run_shodan_pentest(
        query="apache country:US",  # Will use simulation if API not available
        limit=3,
        intensity=8,
        stealth_mode=False,
        test_all_phases=True
    )
    return result

def run_real_demo():
    """Run a real penetration test using actual Shodan data"""
    logger.info("=== RUNNING REAL SHODAN TEST ===")
    logger.info("This test will use real Shodan data and perform actual port scanning")
    logger.info("IMPORTANT: Ensure you have proper authorization to scan the targets")
    
    # Try to load API key from config to verify it exists
    api_key = None
    try:
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "secure_config.json")
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                config = json.load(f)
                if 'api_keys' in config and 'shodan' in config['api_keys']:
                    api_key = config['api_keys']['shodan']
    except Exception as e:
        logger.error(f"Error loading Shodan API key: {str(e)}")
    
    if not api_key or api_key == "YourShodanAPIKeyHere":
        logger.error("No valid Shodan API key found in secure_config.json")
        logger.error("Please add your Shodan API key to secure_config.json")
        logger.error('Format: {"api_keys": {"shodan": "YOUR_ACTUAL_API_KEY"}}')
        return {"error": "No valid Shodan API key configured"}
    
    logger.info("Shodan API key found. Proceeding with real test.")
    
    # Run with real Shodan data
    result = run_shodan_pentest(
        query="webcam country:US",  # Actual Shodan query - use a less intrusive target
        limit=2,  # Limit to just 2 targets for safety
        intensity=6,  # Medium intensity to avoid aggressive scanning
        stealth_mode=True,  # Use stealth mode to minimize impact
        test_all_phases=True
    )
    return result

def run_stealth_demo():
    """Run a demo in stealth mode with low detection chance"""
    logger.info("=== RUNNING STEALTH DEMO ===")
    logger.info("This demo will test all 6 phases with stealth techniques")
    
    # Run with medium intensity but in stealth mode
    result = run_shodan_pentest(
        query="nginx country:JP",  # Will use simulation if API not available
        limit=2,
        intensity=7,
        stealth_mode=True,
        test_all_phases=True
    )
    return result

def run_focused_demo(target_ip):
    """Run a focused demo against a specific target"""
    logger.info(f"=== RUNNING FOCUSED DEMO AGAINST {target_ip} ===")
    
    if not target_ip:
        logger.error("No target IP provided for focused demo")
        return None
        
    logger.info(f"This demo will test all 6 phases against the target: {target_ip}")
    
    # Run focused test against specific target
    result = run_shodan_pentest(
        target=target_ip,
        intensity=6,
        stealth_mode=True,
        test_all_phases=True
    )
    return result

def main():
    """Main function for demo"""
    parser = setup_parser()
    args = parser.parse_args()
    
    try:
        if args.demo_type == 'quick':
            result = run_quick_demo()
        elif args.demo_type == 'full':
            result = run_full_demo()
        elif args.demo_type == 'real':
            result = run_real_demo()
        elif args.demo_type == 'stealth':
            result = run_stealth_demo()
        elif args.demo_type == 'focused':
            result = run_focused_demo(args.target)
            if not result:
                print("Error: --target argument is required for focused demo")
                sys.exit(1)
        
        print("\n===== DEMO COMPLETE =====")
        print(f"Report ID: {result['report_id']}")
        print(f"Targets tested: {len(result.get('targets', []))}")
        
        # Count successful exploitations
        successful = sum(1 for t in result.get('targets', []) if t.get('exploitation_success', False))
        print(f"Successful exploits: {successful}")
        
    except KeyboardInterrupt:
        print("\nDemo cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error during demo: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()