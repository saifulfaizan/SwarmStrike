#!/usr/bin/env python3
"""
🔍 SHODAN INTELLIGENCE MODULE
============================
Integration with Shodan API for target intelligence gathering
"""

import shodan
import logging
import json
import os
import random
import ipaddress
import time
from typing import List, Dict, Any, Union
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ShodanIntelligence:
    """Shodan API integration for target discovery and intelligence gathering"""
    
    def __init__(self, api_key=None):
        """Initialize the Shodan intelligence module"""
        # Try to load API key from environment or config file
        if api_key is None:
            # Check for API key in environment
            api_key = os.environ.get('SHODAN_API_KEY')
            
            # If not in environment, check secure config
            if api_key is None:
                try:
                    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                             "secure_config.json")
                    if os.path.exists(config_path):
                        with open(config_path, 'r') as f:
                            config = json.load(f)
                            # Try to get API key from different possible locations
                            if 'shodan_api_key' in config:
                                api_key = config.get('shodan_api_key')
                            elif 'api_keys' in config and 'shodan' in config['api_keys']:
                                api_key = config['api_keys']['shodan']
                except Exception as e:
                    logger.error(f"Error loading config: {str(e)}")
        
        if api_key:
            self.api = shodan.Shodan(api_key)
            self.api_key = api_key
            logger.info("Shodan Intelligence Module initialized")
        else:
            self.api = None
            self.api_key = None
            logger.warning("No Shodan API key provided. Module initialized in limited mode.")
            logger.warning("Set SHODAN_API_KEY in environment or in secure_config.json")
    
    def search_targets(self, query: str, limit: int = 100, 
                       filters: Dict = None) -> Dict[str, Any]:
        """
        Search for targets matching query on Shodan
        
        Args:
            query: Shodan search query
            limit: Maximum number of results to return
            filters: Additional filters for the search
            
        Returns:
            Dictionary containing search results and metadata
        """
        if self.api is None:
            logger.error("Shodan API not initialized. Please provide API key.")
            return self._generate_simulated_results(query, limit)
        
        try:
            logger.info(f"Searching Shodan for: {query}")
            
            # Perform search
            results = self.api.search(query, limit=limit)
            
            # Process and format results
            formatted_results = {
                'search_id': f"shodan-{int(time.time())}",
                'timestamp': time.time(),
                'query': query,
                'total_results': results['total'],
                'returned_results': len(results['matches']),
                'targets': []
            }
            
            # Process each target
            for item in results['matches']:
                # Apply additional filters if specified
                if filters and not self._apply_filters(item, filters):
                    continue
                    
                # Extract and format target data
                target = {
                    'ip': item['ip_str'],
                    'hostnames': item.get('hostnames', []),
                    'domains': item.get('domains', []),
                    'org': item.get('org', 'Unknown'),
                    'isp': item.get('isp', 'Unknown'),
                    'country': item.get('location', {}).get('country_name', 'Unknown'),
                    'city': item.get('location', {}).get('city', 'Unknown'),
                    'latitude': item.get('location', {}).get('latitude'),
                    'longitude': item.get('location', {}).get('longitude'),
                    'os': item.get('os', 'Unknown'),
                    'ports': [item['port']] if 'port' in item else [],
                    'vulns': item.get('vulns', []),
                    'last_updated': item.get('last_update'),
                    'services': self._extract_services(item),
                    'shodan_data': item
                }
                
                formatted_results['targets'].append(target)
            
            logger.info(f"Found {formatted_results['returned_results']} targets on Shodan")
            return formatted_results
            
        except shodan.APIError as e:
            logger.error(f"Shodan API error: {str(e)}")
            return self._generate_simulated_results(query, limit)
    
    def lookup_host(self, ip: str) -> Dict[str, Any]:
        """
        Look up detailed information about a specific host
        
        Args:
            ip: IP address to lookup
            
        Returns:
            Dictionary containing host information
        """
        if self.api is None:
            logger.error("Shodan API not initialized. Please provide API key.")
            return self._generate_simulated_host(ip)
            
        try:
            logger.info(f"Looking up host: {ip}")
            host = self.api.host(ip)
            
            # Format host information
            formatted_host = {
                'ip': host.get('ip_str'),
                'hostnames': host.get('hostnames', []),
                'domains': host.get('domains', []),
                'country': host.get('country_name', 'Unknown'),
                'city': host.get('city', 'Unknown'),
                'org': host.get('org', 'Unknown'),
                'isp': host.get('isp', 'Unknown'),
                'asn': host.get('asn', 'Unknown'),
                'os': host.get('os', 'Unknown'),
                'ports': host.get('ports', []),
                'vulns': host.get('vulns', []),
                'tags': host.get('tags', []),
                'last_update': host.get('last_update'),
                'services': []
            }
            
            # Process services/banners
            for data in host.get('data', []):
                service = {
                    'port': data.get('port'),
                    'protocol': data.get('transport', 'tcp'),
                    'service': data.get('product', ''),
                    'version': data.get('version', ''),
                    'cpe': data.get('cpe', []),
                    'banner': data.get('data', '')
                }
                formatted_host['services'].append(service)
            
            return formatted_host
            
        except shodan.APIError as e:
            logger.error(f"Shodan API error: {str(e)}")
            return self._generate_simulated_host(ip)
    
    def scan_target(self, target: str) -> Dict[str, Any]:
        """
        Initiate a Shodan scan against a target
        
        Args:
            target: IP/hostname to scan
            
        Returns:
            Dictionary containing scan information
        """
        if self.api is None:
            logger.error("Shodan API not initialized. Please provide API key.")
            return {'error': 'No API key provided', 'scan_id': None}
            
        try:
            # Note: Requires Shodan corporate plan or credits
            scan = self.api.scan(target)
            return {
                'scan_id': scan['id'],
                'count': scan['count'],
                'status': 'submitted',
                'target': target
            }
        except shodan.APIError as e:
            logger.error(f"Shodan API error (likely requires upgrade): {str(e)}")
            return {'error': str(e), 'scan_id': None}
    
    def get_exploits(self, query: str, limit: int = 100) -> Dict[str, Any]:
        """
        Search for exploits matching query
        
        Args:
            query: Search query for exploits
            limit: Maximum number of results
            
        Returns:
            Dictionary containing exploit information
        """
        if self.api is None:
            logger.error("Shodan API not initialized. Please provide API key.")
            return self._generate_simulated_exploits(query, limit)
            
        try:
            logger.info(f"Searching exploits for: {query}")
            exploits = self.api.exploits.search(query, limit=limit)
            
            # Format results
            formatted_results = {
                'search_id': f"exploits-{int(time.time())}",
                'timestamp': time.time(),
                'query': query,
                'total_results': exploits['total'],
                'returned_results': len(exploits['matches']),
                'exploits': []
            }
            
            # Process each exploit
            for item in exploits['matches']:
                exploit = {
                    'id': item.get('_id'),
                    'title': item.get('title', 'Unknown'),
                    'description': item.get('description', ''),
                    'date': item.get('date'),
                    'type': item.get('type'),
                    'platform': item.get('platform'),
                    'port': item.get('port'),
                    'source': item.get('source'),
                    'cve': item.get('cve'),
                    'bid': item.get('bid'),
                    'msb': item.get('msb'),
                    'osvdb': item.get('osvdb'),
                    'edb': item.get('edb-id'),
                    'raw_data': item
                }
                formatted_results['exploits'].append(exploit)
                
            logger.info(f"Found {formatted_results['returned_results']} exploits")
            return formatted_results
            
        except shodan.APIError as e:
            logger.error(f"Shodan API error: {str(e)}")
            return self._generate_simulated_exploits(query, limit)
    
    def discover_vulnerable_targets(self, vulnerability: str, 
                                   limit: int = 100) -> Dict[str, Any]:
        """
        Find targets vulnerable to a specific vulnerability
        
        Args:
            vulnerability: CVE ID or vulnerability name
            limit: Maximum number of results
            
        Returns:
            Dictionary containing vulnerable targets
        """
        # For CVE, use 'vuln:' prefix
        if vulnerability.lower().startswith('cve-'):
            query = f"vuln:{vulnerability}"
        else:
            query = vulnerability
            
        return self.search_targets(query, limit)
    
    def get_shodan_intelligence_report(self, target: str) -> Dict[str, Any]:
        """
        Generate a comprehensive intelligence report on a target
        
        Args:
            target: IP address or domain
            
        Returns:
            Dictionary containing intelligence report
        """
        logger.info(f"Generating intelligence report for: {target}")
        
        report = {
            'report_id': f"shodan-intel-{int(time.time())}",
            'timestamp': time.time(),
            'target': target,
            'host_info': None,
            'ssl_info': None,
            'dns_info': None,
            'exploit_info': None,
            'port_info': None,
            'vuln_info': None
        }
        
        # Get host information
        try:
            if self._is_ip_address(target):
                report['host_info'] = self.lookup_host(target)
            else:
                # Try to resolve domain to IP first
                import socket
                try:
                    ip = socket.gethostbyname(target)
                    report['host_info'] = self.lookup_host(ip)
                    report['host_info']['resolved_from_domain'] = target
                except:
                    logger.error(f"Could not resolve domain: {target}")
                    report['host_info'] = self._generate_simulated_host(target)
            
            # Add exploits if we have vulnerabilities
            vulns = report['host_info'].get('vulns', [])
            if vulns:
                # Get exploits for the first vulnerability
                if len(vulns) > 0:
                    report['exploit_info'] = self.get_exploits(vulns[0])
        except Exception as e:
            logger.error(f"Error generating intelligence report: {str(e)}")
            
        return report
    
    def _apply_filters(self, item: Dict, filters: Dict) -> bool:
        """Apply additional filters to a search result"""
        for key, value in filters.items():
            # Handle nested keys
            if '.' in key:
                parts = key.split('.')
                current = item
                for part in parts[:-1]:
                    if part not in current:
                        return False
                    current = current[part]
                if parts[-1] not in current or current[parts[-1]] != value:
                    return False
            # Handle direct keys
            elif key not in item or item[key] != value:
                return False
        return True
    
    def _extract_services(self, item: Dict) -> List[Dict]:
        """Extract service information from a Shodan item"""
        services = []
        
        # Add the main service
        service = {
            'port': item.get('port'),
            'protocol': item.get('transport', 'tcp'),
            'service': item.get('product', ''),
            'version': item.get('version', ''),
        }
        services.append(service)
        
        return services
    
    def _is_ip_address(self, value: str) -> bool:
        """Check if a string is an IP address"""
        try:
            ipaddress.ip_address(value)
            return True
        except ValueError:
            return False
    
    def _generate_simulated_results(self, query: str, limit: int) -> Dict[str, Any]:
        """Generate simulated search results when API is not available"""
        logger.warning("Generating simulated Shodan results - NO API KEY AVAILABLE")
        
        formatted_results = {
            'search_id': f"simulated-{int(time.time())}",
            'timestamp': time.time(),
            'query': query,
            'total_results': random.randint(100, 1000),
            'returned_results': min(limit, random.randint(50, 200)),
            'targets': [],
            'simulated': True  # Flag to indicate these are simulated results
        }
        
        # Generate random targets
        for i in range(min(limit, random.randint(10, 50))):
            # Generate a random IP
            ip = f"{random.randint(1, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
            
            # Create a simulated target
            target = {
                'ip': ip,
                'hostnames': [f"server-{random.randint(1, 999)}.example.com"] if random.random() > 0.5 else [],
                'domains': ["example.com"] if random.random() > 0.7 else [],
                'org': random.choice(["Amazon AWS", "Microsoft Azure", "Google Cloud", "OVH", "Digital Ocean", "Self-hosted"]),
                'isp': random.choice(["Amazon", "Microsoft", "Google", "OVH", "Level3", "Comcast"]),
                'country': random.choice(["United States", "Germany", "France", "Netherlands", "Japan", "Brazil"]),
                'city': random.choice(["New York", "Berlin", "Paris", "Amsterdam", "Tokyo", "Sao Paulo"]),
                'latitude': round(random.uniform(-90, 90), 6),
                'longitude': round(random.uniform(-180, 180), 6),
                'os': random.choice(["Windows Server 2022", "Ubuntu 24.04", "CentOS 9", "Debian 12", None]),
                'ports': sorted(random.sample(range(1, 65536), random.randint(1, 10))),
                'vulns': [f"CVE-2025-{random.randint(1000, 9999)}"] if random.random() > 0.7 else [],
                'last_updated': time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime(time.time() - random.randint(0, 30*24*3600))),
                'services': []
            }
            
            # Add services
            for port in target['ports']:
                service = ""
                version = ""
                
                if port == 80 or port == 443:
                    service = "Apache" if random.random() > 0.5 else "Nginx"
                    version = f"{random.randint(1, 3)}.{random.randint(0, 20)}.{random.randint(0, 20)}"
                elif port == 22:
                    service = "OpenSSH"
                    version = f"{random.randint(5, 9)}.{random.randint(0, 9)}p{random.randint(1, 5)}"
                elif port == 21:
                    service = "vsftpd"
                    version = f"{random.randint(2, 3)}.{random.randint(0, 3)}.{random.randint(0, 5)}"
                elif port == 3389:
                    service = "Microsoft RDP"
                    version = f"{random.randint(5, 10)}.{random.randint(0, 5)}"
                
                target['services'].append({
                    'port': port,
                    'protocol': 'tcp',
                    'service': service,
                    'version': version
                })
            
            formatted_results['targets'].append(target)
        
        return formatted_results
    
    def _generate_simulated_host(self, ip: str) -> Dict[str, Any]:
        """Generate simulated host information when API is not available"""
        logger.warning(f"Generating simulated host information for {ip} - NO API KEY AVAILABLE")
        
        # Determine if this should be a vulnerable host (50% chance)
        is_vulnerable = random.random() > 0.5
        
        # Generate ports (between 3-15 open ports)
        num_ports = random.randint(3, 15)
        ports = sorted(random.sample(range(1, 65536), num_ports))
        
        # Generate services based on common ports
        services = []
        for port in ports:
            protocol = "tcp"
            service_name = ""
            version = ""
            banner = ""
            
            if port == 80:
                service_name = random.choice(["Apache", "Nginx", "IIS"])
                version = f"{random.randint(1, 3)}.{random.randint(0, 20)}.{random.randint(0, 20)}"
                banner = f"HTTP/1.1 200 OK\r\nServer: {service_name}/{version}\r\nContent-Type: text/html"
            elif port == 443:
                service_name = random.choice(["Apache", "Nginx", "IIS"])
                version = f"{random.randint(1, 3)}.{random.randint(0, 20)}.{random.randint(0, 20)}"
                banner = f"HTTP/1.1 200 OK\r\nServer: {service_name}/{version}\r\nContent-Type: text/html"
            elif port == 22:
                service_name = "OpenSSH"
                version = f"{random.randint(5, 9)}.{random.randint(0, 9)}p{random.randint(1, 5)}"
                banner = f"SSH-2.0-{service_name}_{version}"
            elif port == 21:
                service_name = "vsftpd"
                version = f"{random.randint(2, 3)}.{random.randint(0, 3)}.{random.randint(0, 5)}"
                banner = f"220 FTP Server ready.\r\n"
            elif port == 3389:
                service_name = "Microsoft RDP"
                version = f"{random.randint(5, 10)}.{random.randint(0, 5)}"
                banner = "Binary data"
            elif port == 8080:
                service_name = "Tomcat"
                version = f"{random.randint(7, 10)}.{random.randint(0, 5)}.{random.randint(10, 80)}"
                banner = f"HTTP/1.1 200 OK\r\nServer: Apache-Coyote/{version}"
            elif port == 1433:
                service_name = "Microsoft SQL Server"
                version = f"{random.randint(2014, 2025)}"
                banner = "Binary data"
            elif port == 3306:
                service_name = "MySQL"
                version = f"{random.randint(5, 8)}.{random.randint(0, 9)}.{random.randint(10, 40)}"
                banner = f"Binary data"
            
            services.append({
                'port': port,
                'protocol': protocol,
                'service': service_name,
                'version': version,
                'banner': banner
            })
        
        # Generate vulnerabilities
        vulns = []
        if is_vulnerable:
            # Generate 1-5 vulnerabilities
            num_vulns = random.randint(1, 5)
            for _ in range(num_vulns):
                vulns.append(f"CVE-2025-{random.randint(1000, 9999)}")
        
        return {
            'ip': ip,
            'hostnames': [f"server-{random.randint(1, 999)}.example.com"] if random.random() > 0.5 else [],
            'domains': ["example.com"] if random.random() > 0.7 else [],
            'country': random.choice(["United States", "Germany", "France", "Netherlands", "Japan", "Brazil"]),
            'city': random.choice(["New York", "Berlin", "Paris", "Amsterdam", "Tokyo", "Sao Paulo"]),
            'org': random.choice(["Amazon AWS", "Microsoft Azure", "Google Cloud", "OVH", "Digital Ocean", "Self-hosted"]),
            'isp': random.choice(["Amazon", "Microsoft", "Google", "OVH", "Level3", "Comcast"]),
            'asn': f"AS{random.randint(1, 64000)}",
            'os': random.choice(["Windows Server 2022", "Ubuntu 24.04", "CentOS 9", "Debian 12", None]),
            'ports': ports,
            'vulns': vulns,
            'tags': ["cloud"] if random.random() > 0.7 else [],
            'last_update': time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime(time.time() - random.randint(0, 30*24*3600))),
            'services': services,
            'simulated': True  # Flag to indicate this is simulated data
        }
        
    def _generate_simulated_exploits(self, query: str, limit: int) -> Dict[str, Any]:
        """Generate simulated exploit information when API is not available"""
        logger.warning(f"Generating simulated exploits for {query} - NO API KEY AVAILABLE")
        
        formatted_results = {
            'search_id': f"exploits-sim-{int(time.time())}",
            'timestamp': time.time(),
            'query': query,
            'total_results': random.randint(5, 50),
            'returned_results': min(limit, random.randint(3, 30)),
            'exploits': [],
            'simulated': True  # Flag to indicate these are simulated results
        }
        
        # Generate random exploits
        exploit_types = ["dos", "remote", "webapps", "local", "shellcode"]
        platforms = ["windows", "linux", "multi", "hardware", "cgi"]
        
        for i in range(min(limit, random.randint(3, 20))):
            year = random.randint(2022, 2025)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            
            cve_id = f"CVE-{year}-{random.randint(1000, 9999)}"
            
            exploit = {
                'id': f"{random.randint(10000, 99999)}",
                'title': f"Exploit for {query.capitalize()} Vulnerability in {random.choice(['Windows', 'Linux', 'Apache', 'Nginx', 'MySQL'])}",
                'description': f"This exploit takes advantage of a vulnerability in {query}...",
                'date': f"{year}-{month:02d}-{day:02d}T00:00:00.000Z",
                'type': random.choice(exploit_types),
                'platform': random.choice(platforms),
                'port': random.choice([22, 80, 443, 8080, 3389]) if random.random() > 0.3 else None,
                'source': random.choice(["ExploitDB", "Metasploit", "PacketStorm"]),
                'cve': [cve_id],
                'bid': str(random.randint(10000, 99999)) if random.random() > 0.5 else None,
                'msb': f"MS{year}-{random.randint(10, 99)}" if random.random() > 0.7 else None,
                'osvdb': str(random.randint(10000, 99999)) if random.random() > 0.5 else None,
                'edb': random.randint(40000, 50000) if random.random() > 0.5 else None
            }
            
            formatted_results['exploits'].append(exploit)
            
        return formatted_results

# Example usage when run directly
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Shodan Intelligence Module')
    parser.add_argument('--search', help='Search query')
    parser.add_argument('--host', help='Look up host information')
    parser.add_argument('--exploits', help='Search for exploits')
    parser.add_argument('--vulnerable', help='Find targets vulnerable to a CVE')
    parser.add_argument('--report', help='Generate intelligence report for target')
    parser.add_argument('--api-key', help='Shodan API key')
    parser.add_argument('--limit', type=int, default=100, help='Result limit')
    
    args = parser.parse_args()
    
    # Initialize module
    shodan_intel = ShodanIntelligence(args.api_key)
    
    if args.search:
        results = shodan_intel.search_targets(args.search, args.limit)
        print(f"Found {results['returned_results']} results for '{args.search}'")
        for i, target in enumerate(results['targets'][:10]):
            print(f"{i+1}. {target['ip']} - {target['org']} - Ports: {', '.join(map(str, target['ports']))}")
            
    elif args.host:
        host = shodan_intel.lookup_host(args.host)
        print(f"Host: {args.host}")
        print(f"Organization: {host['org']}")
        print(f"Country: {host['country']}")
        print(f"Open ports: {', '.join(map(str, host['ports']))}")
        if host.get('vulns'):
            print(f"Vulnerabilities: {', '.join(host['vulns'])}")
            
    elif args.exploits:
        exploits = shodan_intel.get_exploits(args.exploits, args.limit)
        print(f"Found {exploits['returned_results']} exploits for '{args.exploits}'")
        for i, exploit in enumerate(exploits['exploits'][:10]):
            print(f"{i+1}. {exploit['title']} - {exploit.get('cve', ['N/A'])[0] if isinstance(exploit.get('cve'), list) else exploit.get('cve', 'N/A')}")
            
    elif args.vulnerable:
        results = shodan_intel.discover_vulnerable_targets(args.vulnerable, args.limit)
        print(f"Found {results['returned_results']} targets vulnerable to '{args.vulnerable}'")
        for i, target in enumerate(results['targets'][:10]):
            print(f"{i+1}. {target['ip']} - {target['org']}")
            
    elif args.report:
        report = shodan_intel.get_shodan_intelligence_report(args.report)
        host = report['host_info']
        print(f"Intelligence Report for {args.report}")
        print(f"IP: {host['ip']}")
        print(f"Organization: {host['org']}")
        print(f"Country: {host['country']}, City: {host['city']}")
        print(f"Open ports: {', '.join(map(str, host['ports']))}")
        if host.get('vulns'):
            print(f"Vulnerabilities: {', '.join(host['vulns'])}")
    else:
        print("No action specified. Use --search, --host, --exploits, --vulnerable, or --report.")