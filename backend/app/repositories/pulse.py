import sqlite3

# 固定的“仅一条启用”哨兵值；停用行此列为 NULL，配合唯一索引实现互斥
ENABLED_SENTINEL = 1


def list_rules(conn: sqlite3.Connection) -> list[dict]:
    return [dict(r) for r in conn.execute("SELECT * FROM pulse_rules ORDER BY id").fetchall()]


def get(conn: sqlite3.Connection, rule_id: int) -> dict | None:
    row = conn.execute("SELECT * FROM pulse_rules WHERE id=?", (rule_id,)).fetchone()
    return dict(row) if row else None


def get_enabled(conn: sqlite3.Connection) -> dict | None:
    row = conn.execute("SELECT * FROM pulse_rules WHERE enabled_flag=? LIMIT 1", (ENABLED_SENTINEL,)).fetchone()
    return dict(row) if row else None


def create(conn: sqlite3.Connection, name: str) -> int:
    cur = conn.execute("INSERT INTO pulse_rules(name) VALUES (?)", (name,))
    conn.commit()
    return int(cur.lastrowid)


def set_enabled(conn: sqlite3.Connection, rule_id: int, enabled: bool) -> dict | None:
    """启停规则。启用任意一条会先停用其他所有规则，因此始终最多只有一条启用。"""
    row = get(conn, rule_id)
    if row is None:
        return None
    if enabled:
        conn.execute("UPDATE pulse_rules SET enabled_flag=NULL")
        conn.execute("UPDATE pulse_rules SET enabled_flag=? WHERE id=?", (ENABLED_SENTINEL, rule_id))
    else:
        conn.execute("UPDATE pulse_rules SET enabled_flag=NULL WHERE id=?", (rule_id,))
    conn.commit()
    return get(conn, rule_id)
