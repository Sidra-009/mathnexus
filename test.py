import pandas as pd
from cleancore import CleanEngine, print_audit_report

data = {
    "CustomerID": ["A111", "B456", "C789", "D222"],
    "Age": [25, None, None, 30],
    "Salary": [3000, 3000, 3000, 3000]
}

df = pd.DataFrame(data)

engine = CleanEngine(df)
cleaned_df, audit_log = engine.run()

print_audit_report(audit_log)
