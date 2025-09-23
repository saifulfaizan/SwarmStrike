# Shodan Integration Module for Unified Cybersecurity Framework

## Overview

The Shodan Integration Module adds external target reconnaissance capabilities to the Unified Cybersecurity Framework, allowing you to perform penetration tests against targets discovered through Shodan - "the search engine for Internet-connected devices".

## Features

- **Target Discovery**: Find potential targets based on search queries
- **Vulnerability Identification**: Discover systems vulnerable to specific CVEs
- **Exploit Matching**: Find applicable exploits for discovered systems
- **Intelligence Reports**: Generate comprehensive intelligence reports on targets
- **Automated Penetration Testing**: Use discovered targets for penetration testing

## Setup

1. **Install Required Dependencies**:
   ```
   pip install -r requirements.txt
   ```

2. **Configure Shodan API Key**:
   - Edit `secure_config.json` and add your Shodan API key:
   ```json
   {
     "api_keys": {
       "shodan": "YOUR_SHODAN_API_KEY_HERE"
     }
   }
   ```
   - Or set the environment variable:
   ```
   set SHODAN_API_KEY=your_api_key_here
   ```

3. **Verify Installation**:
   ```
   python -c "from ai_modules.shodan_intelligence import ShodanIntelligence; print('Shodan module installed successfully')"
   ```

## Usage Examples

### Basic Search

```python
from ai_modules.shodan_intelligence import ShodanIntelligence

# Initialize Shodan intelligence module
shodan = ShodanIntelligence()

# Search for targets with a query
results = shodan.search_targets("apache country:US", limit=10)

# Process results
for target in results['targets']:
    print(f"IP: {target['ip']}")
    print(f"Organization: {target.get('org', 'Unknown')}")
    print(f"Open ports: {', '.join(map(str, target['ports']))}")
```

### Finding Vulnerable Targets

```python
# Find systems vulnerable to a specific CVE
vulnerable = shodan.discover_vulnerable_targets("CVE-2023-23397", limit=5)

for target in vulnerable['targets']:
    print(f"Vulnerable system: {target['ip']} ({target.get('org', 'Unknown')})")
    print(f"Vulnerabilities: {', '.join(target.get('vulns', []))}")
```

### Generating Intelligence Reports

```python
# Generate a comprehensive intelligence report for a target
report = shodan.get_shodan_intelligence_report("93.184.216.34")

print(f"Target: {report['target']}")
print(f"Organization: {report['host_info'].get('org', 'Unknown')}")
print(f"Country: {report['host_info'].get('country', 'Unknown')}")
print(f"Open ports: {', '.join(map(str, report['host_info'].get('ports', [])))}")
```

## Running Penetration Tests with Shodan Targeting

The framework includes a specialized script for running penetration tests against targets discovered via Shodan.

### Basic Usage

```bash
# Run a penetration test with Shodan targeting
python shodan_pentest.py --query "apache country:US" --limit 10
```

### Testing Specific IP Addresses

```bash
# Target a specific IP address
python shodan_pentest.py --target "93.184.216.34"
```

### Finding and Testing Vulnerable Systems

```bash
# Find and target systems vulnerable to a specific CVE
python shodan_pentest.py --cve "CVE-2023-23397" --limit 5
```

### Advanced Options

```bash
# Adjust intensity and stealth mode
python shodan_pentest.py --query "apache country:US" --intensity 10 --stealth
```

## Advanced Integration

The Shodan Intelligence module can be integrated with other framework components:

1. **Combine with Autonomous Agents**:
   ```python
   targets = shodan.search_targets("apache country:US")
   agent_framework.deploy_agents_to_targets(targets['targets'])
   ```

2. **Target Discovery for Zero-Day Research**:
   ```python
   targets = shodan.search_targets("specific_vulnerable_software")
   for target in targets['targets']:
       zero_day_arsenal.analyze_target(target['ip'], target['ports'])
   ```

3. **DeepFake Social Engineering Based on Discovered Organizations**:
   ```python
   targets = shodan.search_targets("organization:\"Target Corp\"")
   for target in targets['targets']:
       if target.get('org') == "Target Corp":
           deepfake_platform.create_campaign_for_organization(target['org'])
   ```

## Security Considerations

- Always ensure you have proper authorization before scanning or testing any systems
- Use the stealth mode option when appropriate to minimize detection
- Be aware of legal restrictions regarding scanning in different jurisdictions
- The simulated mode will work without a Shodan API key but will only provide fictional data

## Troubleshooting

- **API Key Issues**: Ensure your Shodan API key is correctly configured
- **Rate Limiting**: Shodan imposes rate limits on API requests
- **Missing Results**: Some searches may require a Shodan membership

For more information, see the [full documentation](ADVANCED_USAGE_GUIDE.md#8-shodan-intelligence).