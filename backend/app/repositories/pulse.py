import sqlite3


def _row_to_dict(row) -> dict:
    return {
        "id": row["id"],
        "enabled": bool(row["enabled"]),
        "distance_step_km": row["distance_step_km"],
        "slow_step_min": row["slow_step_min"],
        "created_at": row["created_at"],
    }


def get_active(conn: sqlite3.Connection) -> dict | None:
    """唯一启用中的脉冲规则；没有时返回 None。"""
    row = conn.execute("SELECT * FROM pulse_rules WHERE enabled=1 ORDER BY id LIMIT 1").fetchone()
    return _row_to_dict(row) if row else None


def list_all(conn: sqlite3.Connection) -> list[dict]:
    return [_row_to_dict(r) for r in conn.execute("SELECT * FROM pulse_rules ORDER BY id").fetchall()]


def enable(conn: sqlite3.Connection, rule_id: int) -> dict:
    """启用指定规则，同时停用其余规则；全局最多一条启用。"""
    row = conn.execute("SELECT * FROM pulse_rules WHERE id=?", (rule_id,)).fetchone()
    if not row:
        return None
    conn.execute("UPDATE pulse_rules SET enabled=0")
    conn.execute("UPDATE pulse_rules SET enabled=1 WHERE id=?", (rule_id,))
    conn.commit()
    return get_active(conn)


def disable_all(conn: sqlite3.Connection) -> None:
    conn.execute("UPDATE pulse_rules SET enabled=0")
    conn.commit()
