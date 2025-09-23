#!/usr/bin/env python3
"""
🔄 REAL PENETRATION TEST OPERATION
================================
Runs a real penetration testing operation with the framework.
"""

import logging
import time
from datetime import datetime
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_real_operation():
    """Run a real operation using the full framework capabilities"""
    logger.info("🚀 Starting real penetration test operation...")
    
    # Import main framework controller
    from main import UnifiedCybersecurityFramework
    
    # Initialize the framework
    framework = UnifiedCybersecurityFramework()
    
    # Define target for the real operation
    target = {
        "name": "RealOperationTarget",
        "ip_range": ["192.168.1.0/24"], 
        "social_engineering_target": {
            "full_name": "Target Executive",
            "email": "executive@target.com",
            "position": "IT Administrator",
            "interests": ["cybersecurity", "cloud computing", "AI"]
        }
    }
    
    # PHASE 1: Full Framework Attack Chain
    logger.info("PHASE 1: Executing full attack chain...")
    print("\n" + "="*70)
    print("🚀 EXECUTING FULL ATTACK CHAIN")
    print("="*70)
    
    result = framework.run_full_attack_chain(target)
    
    print(f"Attack status: {result['status']}")
    print(f"Start time: {result['start_time']}")
    print(f"End time: {result['end_time']}")
    
    # Calculate duration manually
    start_time = datetime.fromisoformat(result['start_time'])
    end_time = datetime.fromisoformat(result['end_time'])
    duration = (end_time - start_time).total_seconds()
    print(f"Duration: {duration:.2f} seconds")
    
    # PHASE 2: Display Attack Summary
    print("\n" + "="*70)
    print("📊 ATTACK SUMMARY")
    print("="*70)
    
    for key, value in result['summary'].items():
        print(f"- {key}: {value}")
    
    # PHASE 3: Generate Comprehensive Report
    logger.info("PHASE 3: Generating comprehensive report...")
    report = framework.get_framework_status_report()
    report_file = framework.export_report(report)
    
    print("\n" + "="*70)
    print("📝 OPERATION REPORT GENERATED")
    print("="*70)
    print(f"Full report exported to: {report_file}")
    
    # Display final statistics
    print("\n" + "="*70)
    print("📈 FRAMEWORK CAPABILITIES")
    print("="*70)
    print(f"Total value: {report['framework_capabilities']['total_value_estimate']}")
    print(f"Sophistication: {report['framework_capabilities']['sophistication_level']}")
    
    # Handle evasion rate - might be a string or a number
    evasion_rate = report['framework_capabilities']['max_evasion_rate']
    if isinstance(evasion_rate, str):
        print(f"Max evasion rate: {evasion_rate}")
    else:
        print(f"Max evasion rate: {evasion_rate*100:.2f}%")
        
    print(f"Threat level: {report['framework_capabilities']['threat_level']}")
    
    logger.info(f"Real operation completed. Report generated: {report_file}")
    return report_file

if __name__ == "__main__":
    try:
        result = run_real_operation()
        print(f"\n✅ Real operation complete. Report available at: {result}")
    except Exception as e:
        logger.error(f"Error during real operation: {str(e)}")
        raise