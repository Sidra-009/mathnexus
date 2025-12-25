def print_audit_report(audit_log):
    if not audit_log:
        print("No transformations applied.")
        return

    audit_id = audit_log[0].audit_id

    print(f"\nAUDIT TRAIL #{audit_id}")
    print("=" * 40)

    for i, event in enumerate(audit_log, 1):
        print(f"\nTRANSFORMATION {i}: {event.transformation}")
        print(f"• Problem: {event.problem}")
        print(f"• Solution: {event.solution}")
        print(f"• Business Rule: {event.rule_id}")

        if event.affected_rows:
            print("• Affected Records:")
            for r in event.affected_rows:
                print(
                    f"   - Row {r['row_index']} "
                    f"(Customer: {r['customer_id']}): "
                    f"{r['before']} → {r['after']}"
                )

        print(
            f"• Validation Hash: "
            f"sha256:{event.before_hash[:6]} → sha256:{event.after_hash[:6]}"
        )

        if event.status == "AUTO_FIXED":
            print("• Status: Auto-fixed")
        else:
            print("• Status: Pending review")

    print("\nSUMMARY:")
    total = len(audit_log)
    auto_fixed = sum(e.status == "AUTO_FIXED" for e in audit_log)
    pending = sum(e.status == "PENDING_REVIEW" for e in audit_log)

    print(f"• Total problems: {total}")
    print(f"• Auto-fixed: {auto_fixed}")
    print(f"• Manual review: {pending}")
    print(f"• Audit ID: {audit_id} (save for compliance)")
