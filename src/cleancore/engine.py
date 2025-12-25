from datetime import datetime
from .audit import AuditEvent
from .transform import dataframe_hash

class CleanEngine:
    def __init__(self, df, id_column="CustomerID"):
        self.df = df
        self.id_column = id_column
        self.audit_log = []
        self.audit_id = "AUD20241219001"

    def run(self):
        self._impute_missing_age()
        self._detect_constant_salary()
        return self.df, self.audit_log

    def _impute_missing_age(self):
        if self.df["Age"].isna().sum() == 0:
            return

        before_hash = dataframe_hash(self.df)
        median_age = self.df["Age"].median()

        affected = []

        for idx, row in self.df[self.df["Age"].isna()].iterrows():
            affected.append({
                "row_index": int(idx),
                "customer_id": row[self.id_column],
                "column": "Age",
                "before": None,
                "after": median_age
            })
            self.df.at[idx, "Age"] = median_age

        after_hash = dataframe_hash(self.df)

        event = AuditEvent(
            audit_id=self.audit_id,
            timestamp=datetime.utcnow().isoformat(),
            transformation="Missing values imputation",
            problem=f"Age has missing values ({len(affected)} rows)",
            solution=f"Filled with median ({median_age})",
            rule_id="GDPR_COMPLIANT_IMPUTATION_v2",
            affected_rows=affected,
            before_hash=before_hash,
            after_hash=after_hash,
            status="AUTO_FIXED"
        )

        self.audit_log.append(event)

    def _detect_constant_salary(self):
        if self.df["Salary"].std() != 0:
            return

        event = AuditEvent(
            audit_id=self.audit_id,
            timestamp=datetime.utcnow().isoformat(),
            transformation="Constant column detection",
            problem="Salary has zero variance",
            solution="Flagged for manual review",
            rule_id="FINANCE_RULE_001",
            affected_rows=[],
            before_hash=dataframe_hash(self.df),
            after_hash=dataframe_hash(self.df),
            status="PENDING_REVIEW"
        )

        self.audit_log.append(event)
