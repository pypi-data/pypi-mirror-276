# Subspy

Subspy is a powerful subdomain enumeration tool designed to help you discover subdomains for a given base URL. It provides a comprehensive set of features and options to enhance your subdomain reconnaissance process.

## Benefits
- **Efficiency** : Quickly identify potential attack surfaces and gather information about a target's infrastructure.
- **Flexibility** : Customize subdomain tests using custom subdomain lists or default lists included in the tool.
- **Ease of Use** : Simple command-line interface with clear options and informative output.
- **Versatility** : Save results to files for further analysis or reporting.

## Installation

Install Subspy using pip:

```bash
pip install subspy
```
## Usage

```bash
subspy --url https://example.com
```
### Command Line Options
- **--url** : The base URL to test subdomains against (e.g., https://example.com).
- **--sub-list** : The file containing a list of subdomains to test.
- **--save** : Save the output to a file.
- **--version** : Show the version of the tool.

### Examples
- Test subdomains for a specific URL:
```bash
subspy --url https://example.com
```
- Specify a custom subdomain list file:
```bash
subspy --url https://example.com --sub-list subdomains.txt
```
- Save the output to a file:
```bash
subspy --url https://example.com --save output.txt
```
- Show the version of the tool:
```bash
subspy --version
```
### Disclaimer

This tool is provided for educational and informational purposes only. The author and contributors of Subspy are not responsible for any misuse or illegal activities performed using this tool.
#### Thanks
Thank you ❤ for using Subspy and supporting open-source tools!
