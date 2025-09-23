#!/usr/bin/env python3
"""
🔑 QUANTUM KEY GENERATOR
======================
Generates quantum-resistant cryptographic keys for secure communications.

Options:
    --count=<number>: Number of keys to generate
    --algorithm=<algorithm>: Algorithm to use (kyber, dilithium, dna)
"""

import sys
import argparse
import logging
from datetime import datetime, timedelta
from typing import Dict, List
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_argument_parser():
    """Set up command line argument parser"""
    parser = argparse.ArgumentParser(description='Generate quantum-resistant cryptographic keys')
    parser.add_argument('--count', type=int, default=5, help='Number of keys to generate')
    parser.add_argument('--algorithm', choices=['kyber', 'dilithium', 'dna', 'all'], 
                        default='all', help='Algorithm to use')
    return parser

def generate_keys(args):
    """Generate quantum-resistant keys"""
    from quantum_crypto.quantum_resistant_crypto import QuantumResistantCrypto
    
    logger.info(f"Initializing quantum-resistant cryptography system...")
    qcrypto = QuantumResistantCrypto()
    
    generated_keys = []
    algorithms = []
    
    if args.algorithm == 'all':
        algorithms = ['kyber', 'dilithium', 'dna']
    else:
        algorithms = [args.algorithm]
    
    # Calculate key distribution
    key_counts = {}
    if args.algorithm == 'all':
        # Distribute keys among algorithms
        key_counts = {
            'kyber': args.count // 2,
            'dilithium': args.count // 4,
            'dna': args.count - (args.count // 2) - (args.count // 4)
        }
    else:
        key_counts = {args.algorithm: args.count}
    
    # Generate keys for each algorithm
    logger.info(f"Generating {args.count} quantum-resistant keys...")
    for algo, count in key_counts.items():
        for i in range(count):
            key = qcrypto.generate_quantum_key(algorithm=algo)
            generated_keys.append({
                'key_id': key.key_id,
                'algorithm': key.algorithm,
                'bit_strength': key.bit_strength,
                'created_at': key.created_at.isoformat(),
                'expires_at': key.expires_at.isoformat()
            })
    
    # Export keys to file
    os.makedirs("secure_keys", exist_ok=True)
    keys_file = f"secure_keys/quantum_keys_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(keys_file, "w") as f:
        json.dump(generated_keys, f, indent=2)
    
    print("\n" + "="*70)
    print("🔑 QUANTUM KEY GENERATION COMPLETE")
    print("="*70)
    print(f"Generated {len(generated_keys)} quantum-resistant keys:")
    
    # Group by algorithm
    by_algorithm = {}
    for key in generated_keys:
        if key['algorithm'] not in by_algorithm:
            by_algorithm[key['algorithm']] = 0
        by_algorithm[key['algorithm']] += 1
    
    for algo, count in by_algorithm.items():
        bit_strength = next((k['bit_strength'] for k in generated_keys if k['algorithm'] == algo), 0)
        print(f"- {count} {algo.upper()} keys ({bit_strength} bits)")
    
    print(f"\nKeys exported to: {keys_file}")
    print("="*70 + "\n")
    
    return generated_keys

if __name__ == "__main__":
    parser = setup_argument_parser()
    args = parser.parse_args()
    keys = generate_keys(args)