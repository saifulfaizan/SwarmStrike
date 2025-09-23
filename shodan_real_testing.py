#!/usr/bin/env python3
"""
🎯 SHODAN PENETRATION TESTING TOOL
=================================
Real Shodan intelligence-based penetration testing framework 
with actual phase-by-phase testing
"""

import os
import sys
import json
import time
import argparse
import logging
from shodan_pentest_enhanced import (
    phase1_reconnaissance, 
    phase2_vulnerability_analysis, 
    phase3_exploit_development,
    phase4_exploitation,
    phase5_post_exploitation,
    phase6_data_exfiltration,
    run_shodan_pentest
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_shodan_api_key():
    """Load Shodan API key from secure config"""
    api_key = None
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "secure_config.json")
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                if 'api_keys' in config and 'shodan' in config['api_keys']:
                    api_key = config['api_keys']['shodan']
        except Exception as e:
            logger.error(f"Error loading API key from config: {str(e)}")
    
    # Check environment variable as fallback
    if not api_key:
        api_key = os.environ.get('SHODAN_API_KEY')
    
    return api_key

def verify_api_key():
    """Verify that a valid Shodan API key is available"""
    api_key = load_shodan_api_key()
    
    if not api_key or api_key == "YourShodanAPIKeyHere":
        logger.error("No valid Shodan API key found!")
        logger.error("Please set your Shodan API key in secure_config.json:")
        logger.error('  {"api_keys": {"shodan": "YOUR_ACTUAL_API_KEY"}}')
        logger.error("Or set the SHODAN_API_KEY environment variable")
        return False
    
    return True

def setup_parser():
    """Set up command line argument parser"""
    parser = argparse.ArgumentParser(description='Run real Shodan-based penetration testing')
    
    # Target specification
    target_group = parser.add_argument_group('Target Selection')
    target_group.add_argument('--query', help='Shodan search query (e.g., "apache country:US")')
    target_group.add_argument('--target', help='Specific IP address to target')
    target_group.add_argument('--cve', help='Search for targets vulnerable to a specific CVE')
    target_group.add_argument('--limit', type=int, default=3, help='Maximum number of targets (default: 3)')
    
    # Test parameters
    test_group = parser.add_argument_group('Test Parameters')
    test_group.add_argument('--intensity', type=int, choices=range(1, 11), default=5,
                        help='Test intensity from 1 (minimal) to 10 (aggressive)')
    test_group.add_argument('--stealth', action='store_true', 
                        help='Enable stealth mode to minimize detection')
    test_group.add_argument('--only-phase', type=int, choices=range(1, 7),
                        help='Run only a specific test phase (1-6)')
    test_group.add_argument('--output', help='Output file for detailed results (JSON format)')
    
    return parser

def run_specific_phase(phase_number, targets, intensity, stealth_mode):
    """Run a specific testing phase"""
    logger.info(f"Running only Phase {phase_number}")
    
    if not targets:
        logger.error("No targets available for testing")
        return None
    
    if phase_number == 1:
        return phase1_reconnaissance(targets, intensity, stealth_mode)
    elif phase_number == 2:
        return phase2_vulnerability_analysis(targets, intensity)
    elif phase_number == 3:
        return phase3_exploit_development(targets, intensity)
    elif phase_number == 4:
        return phase4_exploitation(targets, intensity, stealth_mode)
    elif phase_number == 5:
        return phase5_post_exploitation(targets, intensity, stealth_mode)
    elif phase_number == 6:
        return phase6_data_exfiltration(targets, intensity, stealth_mode)
    else:
        logger.error(f"Invalid phase number: {phase_number}")
        return None

def main():
    """Main function for the Shodan penetration testing tool"""
    parser = setup_parser()
    args = parser.parse_args()
    
    # Verify API key is available
    if not verify_api_key():
        sys.exit(1)
    
    # Ensure we have some form of target
    if not args.query and not args.target and not args.cve:
        logger.error("You must specify at least one target using --query, --target, or --cve")
        sys.exit(1)
        
    logger.info("=" * 70)
    logger.info("🎯 SHODAN REAL PENETRATION TESTING")
    logger.info("=" * 70)
    logger.info(f"Target specification: {'Specific IP' if args.target else 'CVE' if args.cve else 'Query'}")
    logger.info(f"Test intensity: {args.intensity}/10")
    logger.info(f"Stealth mode: {'Enabled' if args.stealth else 'Disabled'}")
    logger.info("=" * 70)
    
    # Display legal and ethical warning
    print("\n⚠️  IMPORTANT WARNING ⚠️")
    print("This tool performs REAL penetration testing using Shodan data.")
    print("Only test systems you have EXPLICIT permission to test.")
    print("Unauthorized testing may be ILLEGAL and could result in legal action.")
    print("By continuing, you confirm you have proper authorization.\n")
    
    # Prompt for confirmation
    try:
        if sys.stdin.isatty():  # Only if running interactively
            choice = input("Do you wish to continue? (yes/no): ")
            if choice.lower() not in ["yes", "y"]:
                logger.info("Operation cancelled by user")
                sys.exit(0)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
    
    try:
        start_time = time.time()
        
        if args.only_phase:
            # First get targets, then run only the specified phase
            result = run_shodan_pentest(
                query=args.query,
                target=args.target,
                cve=args.cve,
                limit=args.limit,
                intensity=args.intensity,
                stealth_mode=args.stealth,
                test_all_phases=False  # Don't run any phases yet
            )
            
            # Extract targets and run specific phase
            targets = result.get('targets', [])
            result = run_specific_phase(args.only_phase, targets, args.intensity, args.stealth)
        else:
            # Run the full test
            result = run_shodan_pentest(
                query=args.query,
                target=args.target,
                cve=args.cve,
                limit=args.limit,
                intensity=args.intensity,
                stealth_mode=args.stealth,
                test_all_phases=True  # Run all phases
            )
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Display summary information
        if result:
            logger.info("\n" + "=" * 70)
            logger.info("✅ TEST COMPLETED SUCCESSFULLY")
            logger.info("=" * 70)
            logger.info(f"Total duration: {duration:.2f} seconds")
            
            if 'report_id' in result:
                logger.info(f"Report ID: {result['report_id']}")
            
            # Count successful exploits
            if 'targets' in result:
                successful = sum(1 for t in result['targets'] if t.get('exploitation_success', False))
                logger.info(f"Targets tested: {len(result['targets'])}")
                logger.info(f"Successful exploits: {successful}")
            
            # Save output to file if requested
            if args.output and 'targets' in result:
                try:
                    # Create a clean result for output
                    output_result = {
                        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                        "targets": result['targets'],
                        "parameters": {
                            "query": args.query,
                            "target": args.target,
                            "cve": args.cve,
                            "intensity": args.intensity,
                            "stealth_mode": args.stealth,
                            "phase": args.only_phase if args.only_phase else "all"
                        }
                    }
                    
                    with open(args.output, 'w') as f:
                        json.dump(output_result, f, indent=2)
                    logger.info(f"Detailed results saved to: {args.output}")
                except Exception as e:
                    logger.error(f"Error saving results: {str(e)}")
    
    except KeyboardInterrupt:
        logger.warning("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error during penetration test: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()