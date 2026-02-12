#!/usr/bin/env python3
"""
CyberArk SCA and SIA Policy Retriever
======================================
Retrieves all Secure Cloud Access (SCA) and Secure Infrastructure Access (SIA) policies
from CyberArk using the platform API. Authenticates via OAuth 2.0 client credentials
and prompts securely for the client secret at runtime (no plaintext credentials in code).

Usage: python3 get_sca_sia_policies.py
"""

import os
import getpass
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration from environment variables
IDENTITY_TENANT_ID = os.getenv("CYBERARK_IDENTITY_TENANT_ID")
SUBDOMAIN = os.getenv("CYBERARK_SUBDOMAIN")
CLIENT_ID = os.getenv("CYBERARK_CLIENT_ID")


def get_token(client_secret: str) -> str:
    """Authenticate via OAuth 2.0 client credentials and return a bearer token."""
    url = f"https://{IDENTITY_TENANT_ID}.id.cyberark.cloud/oauth2/platformtoken"
    data = {
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": client_secret,
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()["access_token"]


def get_sca_policies(token: str) -> dict:
    """Retrieve all Secure Cloud Access (SCA) policies."""
    url = f"https://{SUBDOMAIN}.sca.cyberark.cloud/api/policies"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    response.raise_for_status()
    return response.json()


def get_sia_policies(token: str) -> dict:
    """Retrieve all Secure Infrastructure Access (SIA) policies."""
    url = f"https://{SUBDOMAIN}.uap.cyberark.cloud/api/policies"
    response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
    response.raise_for_status()
    return response.json()


def display_sca_policies(sca_data: dict):
    """Format and display SCA policy results."""
    print("\n" + "=" * 60)
    print("SCA POLICIES (sca.cyberark.cloud)")
    print("=" * 60)
    for policy in sca_data.get("hits", []):
        print(f"\n  Name:        {policy.get('name')}")
        print(f"  Description: {policy.get('description')}")
        print(f"  Status:      {'Active' if policy.get('status') == 1 else 'Inactive'}")
        print(f"  Policy ID:   {policy.get('policyId')}")


def display_sia_policies(sia_data: dict):
    """Format and display SIA policy results."""
    print("\n" + "=" * 60)
    print("SIA POLICIES (uap.cyberark.cloud)")
    print("=" * 60)
    for policy in sia_data.get("results", []):
        metadata = policy.get("metadata", {})
        print(f"\n  Name:        {metadata.get('name')}")
        print(f"  Description: {metadata.get('description')}")
        print(f"  Status:      {metadata.get('status', {}).get('status')}")
        print(f"  Policy ID:   {metadata.get('policyId')}")


def main():
    print("=" * 60)
    print("CyberArk SCA & SIA Policy Retriever")
    print("=" * 60)

    # Validate environment variables
    if not all([IDENTITY_TENANT_ID, SUBDOMAIN, CLIENT_ID]):
        print("\n[ERROR] Missing environment variables.")
        print("Set CYBERARK_IDENTITY_TENANT_ID, CYBERARK_SUBDOMAIN, and CYBERARK_CLIENT_ID")
        print("in your .env file or environment. See .env.example for reference.")
        return

    # Prompt for client secret at runtime
    client_secret = getpass.getpass("\nEnter client secret: ")

    # Authenticate
    print("\n[1/3] Authenticating via OAuth 2.0...")
    token = get_token(client_secret)
    print("      ✓ Bearer token acquired")

    # Retrieve SCA policies
    print("[2/3] Retrieving SCA policies...")
    sca_data = get_sca_policies(token)
    print("      ✓ Done")

    # Retrieve SIA policies
    print("[3/3] Retrieving SIA policies...")
    sia_data = get_sia_policies(token)
    print("      ✓ Done")

    # Display results
    display_sca_policies(sca_data)
    display_sia_policies(sia_data)

    # Summary
    sca_total = sca_data.get("total", 0)
    sia_total = sia_data.get("total", 0)
    print("\n" + "=" * 60)
    print(f"TOTAL: {sca_total} SCA + {sia_total} SIA = {sca_total + sia_total} policies")
    print("=" * 60)


if __name__ == "__main__":
    main()
