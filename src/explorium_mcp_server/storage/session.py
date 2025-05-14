import json
import os
import uuid
from typing import Any, Optional, Dict, List, Union

import duckdb
from duckdb import DuckDBPyConnection

STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(STORAGE_DIR, "session_data.duckdb")

# Ensure storage directory exists
os.makedirs(STORAGE_DIR, exist_ok=True)

# Global connection object
_conn: Optional[DuckDBPyConnection] = None


def get_connection() -> DuckDBPyConnection:
    """Get or create a singleton connection to the DuckDB database."""
    global _conn
    if _conn is None:
        _conn = duckdb.connect(DB_PATH)
        _init_db(_conn)
    return _conn


def _init_db(conn: DuckDBPyConnection) -> None:
    """Initialize the session data table if it doesn't exist."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS session_data (
            session_id VARCHAR,
            key VARCHAR,
            value JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (session_id, key)
        )
    """)


def generate_session_id() -> str:
    """Generate a new unique session ID."""
    return str(uuid.uuid4())


def store_session_data(session_id: str, key: str, value: Any) -> None:
    """
    Store data in the session database.
    
    Args:
        session_id: The session identifier
        key: The key to store the data under
        value: The data to store (will be JSON serialized)
    """
    conn = get_connection()
    
    # Serialize complex objects to JSON
    serialized_value = json.dumps(value)
    
    # Check if entry exists
    result = conn.execute(
        "SELECT COUNT(*) FROM session_data WHERE session_id = ? AND key = ?", 
        [session_id, key]
    ).fetchone()[0]
    
    if result > 0:
        # Update existing entry
        conn.execute(
            "UPDATE session_data SET value = ? WHERE session_id = ? AND key = ?",
            [serialized_value, session_id, key]
        )
    else:
        # Insert new entry
        conn.execute(
            "INSERT INTO session_data (session_id, key, value) VALUES (?, ?, ?)",
            [session_id, key, serialized_value]
        )


def load_session_data(session_id: str, key: str) -> Optional[Any]:
    """
    Load data from the session database.
    
    Args:
        session_id: The session identifier
        key: The key to retrieve the data for
        
    Returns:
        The stored data if found, None otherwise
    """
    conn = get_connection()
    
    result = conn.execute(
        "SELECT value FROM session_data WHERE session_id = ? AND key = ?",
        [session_id, key]
    ).fetchone()
    
    if result is None:
        return None
    
    # Deserialize JSON back to Python objects
    return json.loads(result[0])


def list_session_keys(session_id: str) -> List[str]:
    """
    List all keys associated with a session.
    
    Args:
        session_id: The session identifier
        
    Returns:
        List of keys associated with the session
    """
    conn = get_connection()
    
    result = conn.execute(
        "SELECT key FROM session_data WHERE session_id = ? ORDER BY created_at",
        [session_id]
    ).fetchall()
    
    return [row[0] for row in result]


def delete_session_data(session_id: str, key: Optional[str] = None) -> None:
    """
    Delete session data.
    
    Args:
        session_id: The session identifier
        key: Optional specific key to delete. If None, all session data is deleted.
    """
    conn = get_connection()
    
    if key is not None:
        conn.execute(
            "DELETE FROM session_data WHERE session_id = ? AND key = ?",
            [session_id, key]
        )
    else:
        conn.execute(
            "DELETE FROM session_data WHERE session_id = ?",
            [session_id]
        )


def close_connection() -> None:
    """Close the database connection."""
    global _conn
    if _conn is not None:
        _conn.close()
        _conn = None
