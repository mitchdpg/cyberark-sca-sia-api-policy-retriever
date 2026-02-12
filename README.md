# CyberArk SCA & SIA Policy API Retriever (Python)

Created a script to authenticate with CyberArk's platform API using OAuth 2.0 client credentials, generate a bearer token, and retrieve all Secure Cloud Access (SCA) and Secure Infrastructure Access (SIA) policies. The client secret is prompted at runtime via `getpass` — no plaintext credentials in code.

## Overview

This project demonstrates Python automation against CyberArk's SCA and SIA policy endpoints. It authenticates via the CyberArk Identity platform token endpoint, then queries two separate API services to retrieve and display all configured access policies.

The goal of this project is not full application development, but practical security automation commonly used in presales evaluations, proof-of-concept work, and security policy auditing.

## Security Note

This project prompts for the client secret at runtime using `getpass`.
No secrets, tokens, or tenant-specific identifiers are stored in the repository.
All examples use placeholder values.

## Configuration & Variables

This project uses environment variables to securely configure authentication and API access.

Required variables:

- `CYBERARK_IDENTITY_TENANT_ID` – CyberArk Identity tenant ID (used in the platform token URL)
- `CYBERARK_SUBDOMAIN` – Tenant subdomain for SCA and SIA API endpoints
- `CYBERARK_CLIENT_ID` – OAuth client ID for API authentication

All configuration values are loaded from a `.env` file or environment variables and are not hard-coded. A concise variable reference is also available in `.env.example` for quick setup.

## What This Project Demonstrates

- OAuth 2.0 client credentials authentication against CyberArk Identity
- Secure bearer token generation
- Secure runtime credential prompting via `getpass`
- Authenticated REST API calls to SCA and SIA endpoints
- Retrieval and formatted display of access policies
- Use of environment variables for configuration management

## Project Structure

```
cyberark-sca-sia-api-policy-retriever/
├── get_sca_sia_policies.py   # Retrieves all SCA and SIA policies
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## API Endpoints Used

The script interacts with three CyberArk cloud API endpoints:

| Endpoint | Purpose |
|----------|---------|
| `https://<tenant>.id.cyberark.cloud/oauth2/platformtoken` | OAuth 2.0 token generation |
| `https://<subdomain>.sca.cyberark.cloud/api/policies` | Secure Cloud Access policy retrieval |
| `https://<subdomain>.uap.cyberark.cloud/api/policies` | Secure Infrastructure Access policy retrieval |

## Example Usage

```bash
# Set up environment variables
cp .env.example .env
# Edit .env with your tenant details

# Install dependencies
pip install -r requirements.txt

# Run the script
python3 get_sca_sia_policies.py
```

Example output:

```
============================================================
CyberArk SCA & SIA Policy Retriever
============================================================

Enter client secret:

[1/3] Authenticating via OAuth 2.0...
      ✓ Bearer token acquired
[2/3] Retrieving SCA policies...
      ✓ Done
[3/3] Retrieving SIA policies...
      ✓ Done

============================================================
SCA POLICIES (sca.cyberark.cloud)
============================================================

  Name:        AWS Admin Access
  Description: Cloud admin policy for AWS workloads
  Status:      Active
  Policy ID:   a1b2c3d4-5678-90ab-cdef-example01

============================================================
TOTAL: 3 SCA + 2 SIA = 5 policies
============================================================
```

## Use Case

This project reflects common real-world security automation scenarios, such as:

- Auditing access policies across SCA and SIA platforms
- Validating policy configurations during security evaluations
- Supporting presales demonstrations and proof of concept
- Automating policy inventory for compliance reviews

## Disclaimer

This project is not affiliated with or officially supported by CyberArk.
It was created for learning and demonstration purposes using a trial environment.
