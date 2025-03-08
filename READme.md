# World No.1 Google Dorker

## Overview

The World No.1 Google Dorker is a powerful and customizable tool designed to generate, manage, and automate Google dork queries. This tool assists in ethical hacking, penetration testing, and open-source intelligence gathering by providing a comprehensive suite of features for advanced Google search queries.

## Features

- Custom Dork Query Generator: Generate Google dorks for various categories like login portals, sensitive files, subdomains, and vulnerabilities.
- Real-time Search Monitoring: Automate searches and fetch live results.
- Proxy Integration: Supports proxies to avoid IP bans.
- Captcha Handling: Uses AI-based techniques to bypass captchas.
- Result Filtering: Advanced filtering for domains, file types, and date ranges.
- Search Result Export: Export dork results to CSV or JSON.
- Vulnerability Scanning: Integrates with Shodan for additional intelligence gathering.
- File Type Search: Find specific file types using dorks.
- Database Management: Store and retrieve generated dorks efficiently.
- Interactive Tutorials: Learn how to effectively use Google Dorks.

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- Required Python libraries:
  ```sh
  pip install -r requirements.txt
  ```

### Clone the Repository

```sh
https://github.com/samiXploits/Google-Dorker.git
cd google-dorker
```

## Usage

Run the tool using:

```sh
python generating_google_dorks.py
```

Follow the on-screen instructions to generate and manage Google dorks.

## API Configuration

- Google Gemini API: Configure your `GEMINI_API_KEY` in the script.
- Shodan API: Set `SHODAN_API_KEY` to enable vulnerability searches.

## Exporting Results

You can export generated dorks to:

- CSV: `dorks.csv`
- JSON: `dorks.json`

## Disclaimer

This tool is intended for ethical use only. Misuse of this tool for unauthorized access to data or systems is strictly prohibited.

## Contributing

Feel free to contribute by submitting pull requests or reporting issues.

## License

MIT License. See `LICENSE` file for more details.

