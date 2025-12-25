class AuditEvent:
    def __init__(
        self,
        audit_id,
        timestamp,
        transformation,
        problem,
        solution,
        rule_id,
        affected_rows,
        before_hash,
        after_hash,
        status
    ):
        self.audit_id = audit_id
        self.timestamp = timestamp
        self.transformation = transformation
        self.problem = problem
        self.solution = solution
        self.rule_id = rule_id
        self.affected_rows = affected_rows
        self.before_hash = before_hash
        self.after_hash = after_hash
        self.status = status
