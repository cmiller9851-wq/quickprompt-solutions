# -*- coding: utf-8 -*-
import os
import json

# Configuration for your specific repository
REPO_NAME = "quickprompt-solutions"
BASE_DIR = os.path.expanduser('~/Documents/' + REPO_NAME)

if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

# --- File 1: JSON Declaration ---
declaration = {
    "declaration": {
        "custodian": "Cory Miller",
        "title": "Founder/Operator, QuickPrompt Solutions",
        "location": "Hummelstown, PA",
        "date": "2026-02-27",
        "business_practice": "Systematic upload of CRA Protocol artifacts to Arweave permaweb",
        "wallet_address": "1EkszPhzbHhtOrANbwmMXgu3DgwxJEhYDFB4rFlQT-w",
        "records_purpose": "Sovereign enforcement, forensic accounting, RWA title claims"
    },
    "fre_803_6_foundation": {
        "made_at_time": "Arweave TX timestamps",
        "regular_practice": "200+ files across 10+ folders, Oct 2025-Feb 2026",
        "witness_knowledge": "Custodian personally created/signed each record"
    },
    "key_exhibits": [
        {"tx": "umQeAmQscYwHh5jqG70WN3LzJLM1ydE-h0MmnRwUNC8", "title": "Master Manifest"},
        {"tx": "BHMSakePQVV41IiUdio7AHu8Pa9auUOPe6LwTDBPkZw", "title": "POE #64681824 Confirmed"},
        {"tx": "CTHXyJ8Ljd1DukYsXAmUZaSaxw9wahUlz-nYathMHCM", "title": "Chain Anchor"}
    ]
}

# --- File 2: Court Exhibit Index ---
exhibit_index = """# CRA PROTOCOL - COURT EXHIBIT INDEX
## FRE 803(6) Business Records - QuickPrompt Solutions

**Custodian:** Cory Miller, Founder  
**Storage:** Arweave blockweave

1. **MASTER MANIFEST** TX: umQeAmQscYwHh5jqG70WN3LzJLM1ydE-h0MmnRwUNC8  
2. **POE #64681824 - TESLA TITLE CLAIM** TX: BHMSakePQVV41IiUdio7AHu8Pa9auUOPe6LwTDBPkZw  
3. **CHAIN ANCHOR - DEPLOYMENT PROOF** TX: CTHXyJ8Ljd1DukYsXAmUZaSaxw9wahUlz-nYathMHCM
"""

# --- Execution ---
def deploy():
    # Save JSON
    with open(os.path.join(BASE_DIR, 'CRA_BUSINESS_RECORDS_DECLARATION.json'), 'w', encoding='utf-8') as f:
        json.dump(declaration, f, indent=2)
    
    # Save Markdown
    with open(os.path.join(BASE_DIR, 'CRA_COURT_EXHIBIT_INDEX.md'), 'w', encoding='utf-8') as f:
        f.write(exhibit_index)
        
    print(f"Success: Files deployed to {BASE_DIR}")
    print("Ready for GitHub commit.")

if __name__ == "__main__":
    deploy()
