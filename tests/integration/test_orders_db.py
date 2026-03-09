"""Integration tests: direct database read/write via psycopg2."""


def test_manual_order_insertion_and_deletion(db_connection):
    """
    Verify direct DB write and delete operations via psycopg2.
    DB: INSERT order → SELECT (assert exists) → DELETE → SELECT (assert gone).
    Assert: Inserted order is found, deleted order is not found.
    """
    cur = db_connection.cursor()
    cur.execute(
        "INSERT INTO orders (billing_user_id, payment_method, status) VALUES (%s, %s, %s) RETURNING id",
        ("test-user-123", "Cash on Delivery", "pending"),
    )
    order_id = cur.fetchone()[0]
    cur.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
    row = cur.fetchone()
    db_connection.commit()

    assert row is not None

    cur.execute("DELETE FROM orders WHERE id = %s", (order_id,))
    db_connection.commit()
    cur.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
    deleted = cur.fetchone()
    assert deleted is None

    cur.close()
