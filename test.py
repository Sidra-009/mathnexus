import csv
import copy
from provena import audit_trail, ProvenaLogger, generate_terminal_report

def load_csv_sample(filepath, n=20):
    """Load first n rows from CSV."""
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return [row for _, row in zip(range(n), reader)]

@audit_trail(rule_id="PRODUCT_CLEAN_V1")
def clean_product_names_proper(data):
    """
    Proper implementation: Return NEW list, don't modify in-place.
    This is how your library expects transformations to work.
    """
    result = []
    for row in data:
        # Create a new dictionary for each row
        new_row = row.copy()
        
        if 'itemDescription' in new_row and new_row['itemDescription']:
            original = new_row['itemDescription']
            cleaned = original.strip().lower()
            if original != cleaned:
                new_row['itemDescription'] = cleaned
        
        result.append(new_row)
    return result

# Test 1: Simple manual test first
print("=" * 60)
print("TEST 1: Manual Data (Should show changes)")
print("=" * 60)

test_data = [
    {"Member_number": "1000", "Date": "01-01-2015", "itemDescription": "  WHOLE MILK  "},
    {"Member_number": "1001", "Date": "01-01-2015", "itemDescription": "tropical fruit"},
    {"Member_number": "1002", "Date": "01-01-2015", "itemDescription": "PIP FRUIT  "},
]

logger1 = ProvenaLogger("Manual_Test")
result1 = clean_product_names_proper(test_data, provena_logger=logger1)

# Manually verify
print("Row 0 BEFORE:", test_data[0]['itemDescription'])
print("Row 0 AFTER: ", result1[0]['itemDescription'])
print("Changed?", test_data[0]['itemDescription'] != result1[0]['itemDescription'])

print("\n" + generate_terminal_report(logger1))
logger1.export_json("manual_test_audit.json")

# Test 2: CSV Data
print("\n" + "=" * 60)
print("TEST 2: CSV Data")
print("=" * 60)

try:
    csv_data = load_csv_sample('Groceries_dataset.csv', 20)
    
    # Check what the data looks like
    print(f"Loaded {len(csv_data)} rows")
    if csv_data:
        print("Sample rows:")
        for i in range(min(3, len(csv_data))):
            desc = csv_data[i].get('itemDescription', 'NO COLUMN')
            print(f"  Row {i}: '{desc}'")
    
    # Run transformation with audit
    logger2 = ProvenaLogger("CSV_Cleaning")
    cleaned_csv = clean_product_names_proper(csv_data, provena_logger=logger2)
    
    # Generate report
    report = generate_terminal_report(logger2)
    print("\n" + report)
    
    # Save audit
    logger2.export_json("csv_audit_final.json")
    print(f"\n📁 Audit saved: csv_audit_final.json")
    
except FileNotFoundError:
    print("⚠️  File not found. Creating sample CSV to test...")
    
    # Create a sample CSV for testing
    with open('test_sample.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Member_number', 'Date', 'itemDescription'])
        writer.writeheader()
        writer.writerows([
            {'Member_number': '1000', 'Date': '01-01-2015', 'itemDescription': '  WHOLE MILK  '},
            {'Member_number': '1001', 'Date': '01-01-2015', 'itemDescription': 'tropical fruit'},
            {'Member_number': '1002', 'Date': '01-01-2015', 'itemDescription': 'PIP FRUIT  '},
            {'Member_number': '1003', 'Date': '01-01-2015', 'itemDescription': 'other vegetables'},
            {'Member_number': '1004', 'Date': '01-01-2015', 'itemDescription': '  ROLLS/BUNS  '},
        ])
    
    print("✅ Created test_sample.csv. Run the test again.")