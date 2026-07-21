#!/usr/bin/env python3
"""
CRA Protocol v2.1 Genesis Anchor Tool
Designated Script Name: cra_genesis_anchor.py
Target Environment: Pythonista 3 / Standard Python 3.8+ stdlib
"""

import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import sys
import time

PROTOCOL_VERSION = "CRA_PROTOCOL_v2.1"
DEFAULT_DB = "sel_local.db"

# Exact IRS EIN 42-3967241 Details (Confirmation Date: 2026-07-21)
ENTITY_DATA = {
    "legal_name": "QUICKPROMPT SOLUTIONS",
    "ein": "42-3967241",
    "entity_type": "Single Member LLC",
    "state": "PA",
    "name_control": "QUIC",
    "county": "DAUPHIN",
    "start_date": "2026-07-01",
    "physical_address": "244 E MAIN ST, MIDDLETOWN PA 17025",
    "phone": "717-342-1880",
    "responsible_party": "CORY MICHAEL MILLER SOLE MBR",
    "principal_activity": "Software Intellectual Property Licensing"
}

def init_db(db_path: str) -> sqlite3.Connection:
    """Initializes local SQLite database for offline entity and audit logging."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS entities (
        id TEXT PRIMARY KEY,
        ein TEXT UNIQUE NOT NULL,
        legal_name TEXT NOT NULL,
        metadata_json TEXT NOT NULL,
        created_at INTEGER NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ein TEXT NOT NULL,
        action TEXT NOT NULL,
        details TEXT NOT NULL,
        timestamp INTEGER NOT NULL,
        reflexion_hash TEXT NOT NULL
    )
    """)
    
    conn.commit()
    return conn

def compute_sha256(file_path: str) -> str:
    """Computes SHA-256 digest of target file."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def calculate_canonical_reflexion_hash(prev_hash: str, action: str, timestamp: int, payload: dict) -> str:
    """
    Computes a deterministic reflexion hash using sorted canonical JSON
    to prevent key ordering variance across platforms.
    """
    canonical_payload = json.dumps(payload, sort_keys=True)
    raw_data = f"{prev_hash}:{action}:{timestamp}:{canonical_payload}"
    return hashlib.sha256(raw_data.encode("utf-8")).hexdigest()

def execute_genesis_anchor(pdf_path: str, db_path: str) -> None:
    if not os.path.exists(pdf_path):
        print(f"[ERROR] Specified PDF confirmation file does not exist: {pdf_path}", file=sys.stderr)
        sys.exit(1)

    ein = ENTITY_DATA["ein"]
    bundle_dir = os.path.abspath(f"anchor_bundle_ein_{ein.replace('-', '')}")
    
    # 1. Database Connection & Chain Inspection
    conn = init_db(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT reflexion_hash FROM audit_logs WHERE ein = ? ORDER BY id DESC LIMIT 1", (ein,))
    row = cursor.fetchone()
    prev_hash = row[0] if row else "0000000000000000000000000000000000000000000000000000000000000000"
    
    # 2. Compute PDF Hash
    pdf_sha256 = compute_sha256(pdf_path)
    timestamp = int(time.time())
    entity_id = hashlib.sha256(f"{ein}:{timestamp}".encode("utf-8")).hexdigest()[:16]
    
    # 3. Formulate Payload & Canonical Reflexion Hash
    action = "GENESIS_ENTITY_REGISTRATION"
    audit_payload = {
        "ein": ein,
        "legal_name": ENTITY_DATA["legal_name"],
        "pdf_sha256": pdf_sha256,
        "protocol": PROTOCOL_VERSION
    }
    
    current_reflexion_hash = calculate_canonical_reflexion_hash(
        prev_hash=prev_hash,
        action=action,
        timestamp=timestamp,
        payload=audit_payload
    )
    
    # 4. Commit to Local Database
    cursor.execute(
        "INSERT OR REPLACE INTO entities (id, ein, legal_name, metadata_json, created_at) VALUES (?, ?, ?, ?, ?)",
        (entity_id, ein, ENTITY_DATA["legal_name"], json.dumps(ENTITY_DATA), timestamp)
    )
    cursor.execute(
        "INSERT INTO audit_logs (ein, action, details, timestamp, reflexion_hash) VALUES (?, ?, ?, ?, ?)",
        (ein, action, json.dumps(audit_payload), timestamp, current_reflexion_hash)
    )
    conn.commit()
    conn.close()
    
    # 5. Assemble Bundle Directory
    os.makedirs(bundle_dir, exist_ok=True)
    
    # Copy PDF directly into bundle
    dest_pdf_path = os.path.join(bundle_dir, "ein_confirmation.pdf")
    shutil.copy2(pdf_path, dest_pdf_path)
    
    metadata_payload = {
        "protocol": PROTOCOL_VERSION,
        "entity_id": entity_id,
        "timestamp": timestamp,
        "entity_data": ENTITY_DATA,
        "pdf_sha256": pdf_sha256,
        "reflexion_hash": current_reflexion_hash,
        "previous_hash": prev_hash
    }
    
    metadata_file = os.path.join(bundle_dir, "metadata.json")
    with open(metadata_file, "w") as f:
        json.dump(metadata_payload, f, indent=2, sort_keys=True)
        
    audit_note_file = os.path.join(bundle_dir, "CRA_AUDIT_NOTE.txt")
    with open(audit_note_file, "w") as f:
        f.write(f"=== SOVEREIGN ENTITY LEDGER AUDIT NOTE ===\n")
        f.write(f"PROTOCOL:       {PROTOCOL_VERSION}\n")
        f.write(f"ACTION:         {action}\n")
        f.write(f"ENTITY ID:      {entity_id}\n")
        f.write(f"EIN:            {ein}\n")
        f.write(f"LEGAL NAME:     {ENTITY_DATA['legal_name']}\n")
        f.write(f"PDF SHA-256:    {pdf_sha256}\n")
        f.write(f"REFLEXION HASH: {current_reflexion_hash}\n")
        f.write(f"PREVIOUS HASH:  {prev_hash}\n")
        f.write(f"TIMESTAMP:      {timestamp}\n")

    print("[SUCCESS] Local Genesis Registration Executed.")
    print(f"  └─ Entity ID:       {entity_id}")
    print(f"  └─ Reflexion Hash:  {current_reflexion_hash}")
    print(f"  └─ Bundle Path:     {bundle_dir}")
    print("\n--- Next Step: Permanent Arweave Anchor ---")
    print("Execute the following command to permanently store the bundle via ArDrive CLI:")
    print(f"\nardrive upload-folder --local-path \"{bundle_dir}\" --parent-folder-id <YOUR_ARDRIVE_FOLDER_ID>\n")

def main():
    parser = argparse.ArgumentParser(description="CRA Protocol v2.1 Genesis Anchor Tool")
    parser.add_argument("--pdf", required=True, help="Absolute or relative path to ein_confirmation.pdf")
    parser.add_argument("--db", default=DEFAULT_DB, help=f"Path to local SQLite DB (default: {DEFAULT_DB})")
    
    args = parser.parse_args()
    execute_genesis_anchor(pdf_path=args.pdf, db_path=args.db)

if __name__ == "__main__":
    main()