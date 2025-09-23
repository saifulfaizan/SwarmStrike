#!/usr/bin/env python3
"""
🚀 SIMPLIFIED FRAMEWORK DEMO
==========================
Demonstrates key features without long-running operations.
"""

import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_quick_demo():
    """Run a quick demonstration of the framework's capabilities"""
    logger.info("Starting quick framework demo...")
    
    # Import main framework controller
    from main import UnifiedCybersecurityFramework
    
    # Initialize the framework
    framework = UnifiedCybersecurityFramework()
    
    # Define a target for demo purposes
    target = {
        "name": "QuickDemoTarget",
        "ip_range": ["192.168.1.0/24"],
        "social_engineering_target": {
            "full_name": "Demo User",
            "email": "demo@example.com",
            "interests": ["security", "AI"]
        }
    }
    
    # Display demo information
    print("\n" + "="*70)
    print("🚀 QUICK FRAMEWORK DEMO")
    print("="*70)
    
    # Demo 1: AI Module Reconnaissance
    print("\n🔍 AI-POWERED RECONNAISSANCE")
    print("-" * 40)
    recon_results = framework.ai_module.run_reconnaissance(target["ip_range"])
    print(f"Scan ID: {recon_results['scan_id']}")
    print(f"Vulnerabilities found: {len(recon_results['vulnerabilities'])}")
    
    # Demo 2: Generate a quantum key
    print("\n🔐 QUANTUM-RESISTANT CRYPTOGRAPHY")
    print("-" * 40)
    kyber_key = framework.quantum_crypto.generate_quantum_key(algorithm="kyber")
    print(f"Generated Kyber key: {kyber_key.key_id} ({kyber_key.bit_strength} bits)")
    
    # Demo 3: Neural Payload
    print("\n🧠 NEURAL PAYLOAD GENERATION")
    print("-" * 40)
    payload = framework.neural_payloads.generate_advanced_payload(
        payload_type="reverse_shell",
        target_os="windows",
        evasion_level=10
    )
    print(f"Payload ID: {payload['config'].payload_id}")
    print(f"Fitness score: {payload['config'].fitness_score * 100:.1f}%")
    
    # Demo 4: Generate framework report
    print("\nGenerating framework status report...")
    report = framework.get_framework_status_report()
    report_file = framework.export_report(report)
    print(f"Report exported to: {report_file}")
    
    # Display conclusion
    print("\n" + "="*70)
    print("✅ QUICK DEMO COMPLETE")
    print("="*70)
    print(f"Framework sophistication level: {report['framework_capabilities']['sophistication_level']}")
    print(f"Maximum evasion rate: {report['framework_capabilities']['max_evasion_rate']}")
    print("="*70)

if __name__ == "__main__":
    run_quick_demo()