- name: Generate Audit Report
  run: |
    python generate_audit_report.py --log-dir ./logs/ --output ./report.json

- name: Upload Audit Report to Artifacts
  uses: actions/upload-artifact@v3
  with:
    name: audit-report
    path: ./report.json