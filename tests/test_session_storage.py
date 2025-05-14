import os
import pytest
import uuid

from explorium_mcp_server.storage.session import (
    generate_session_id,
    store_session_data,
    load_session_data,
    list_session_keys,
    delete_session_data,
    close_connection,
    get_connection
)

# Test with an in-memory database
@pytest.fixture(scope="function")
def session_db():
    # Use a temporary test database
    test_db_path = f"/tmp/test_session_{uuid.uuid4()}.duckdb"
    os.environ["EXPLORIUM_DB_PATH"] = test_db_path
    
    # Get a connection to initialize the database
    conn = get_connection()
    
    yield conn
    
    # Clean up
    close_connection()
    if os.path.exists(test_db_path):
        os.remove(test_db_path)


def test_generate_session_id():
    session_id = generate_session_id()
    assert isinstance(session_id, str)
    assert len(session_id) > 0


def test_store_and_load_session_data(session_db):
    session_id = generate_session_id()
    test_data = {"test": "value", "nested": {"key": "value"}}
    
    # Store data
    store_session_data(session_id, "test_key", test_data)
    
    # Load data
    loaded_data = load_session_data(session_id, "test_key")
    
    assert loaded_data == test_data


def test_update_session_data(session_db):
    session_id = generate_session_id()
    initial_data = {"count": 1}
    updated_data = {"count": 2}
    
    # Store initial data
    store_session_data(session_id, "counter", initial_data)
    
    # Update the data
    store_session_data(session_id, "counter", updated_data)
    
    # Load data
    loaded_data = load_session_data(session_id, "counter")
    
    assert loaded_data == updated_data


def test_list_session_keys(session_db):
    session_id = generate_session_id()
    
    # Store multiple keys
    store_session_data(session_id, "key1", "value1")
    store_session_data(session_id, "key2", "value2")
    store_session_data(session_id, "key3", "value3")
    
    # List keys
    keys = list_session_keys(session_id)
    
    assert set(keys) == {"key1", "key2", "key3"}


def test_delete_session_data(session_db):
    session_id = generate_session_id()
    
    # Store multiple keys
    store_session_data(session_id, "key1", "value1")
    store_session_data(session_id, "key2", "value2")
    
    # Delete one key
    delete_session_data(session_id, "key1")
    
    # Check that only key2 remains
    assert load_session_data(session_id, "key1") is None
    assert load_session_data(session_id, "key2") == "value2"
    
    # Delete all keys
    delete_session_data(session_id)
    
    # Check that no keys remain
    assert load_session_data(session_id, "key2") is None
    assert list_session_keys(session_id) == []


def test_different_sessions(session_db):
    session_id1 = generate_session_id()
    session_id2 = generate_session_id()
    
    # Store data in different sessions
    store_session_data(session_id1, "key", "value1")
    store_session_data(session_id2, "key", "value2")
    
    # Check that data is separated by session
    assert load_session_data(session_id1, "key") == "value1"
    assert load_session_data(session_id2, "key") == "value2"
