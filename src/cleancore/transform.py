import hashlib

def dataframe_hash(df):
    """
    Deterministic hash of dataframe content (stdlib only)
    """
    raw = df.to_csv(index=True).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()
