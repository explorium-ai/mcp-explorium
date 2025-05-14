from typing import Optional

from pydantic import Field

from explorium_mcp_server.tools.shared import (
    mcp,
    create_session,
    get_session_data,
    save_session_data,
    get_session_keys,
    clear_session
)


@mcp.tool()
def create_new_session() -> dict:
    """
    Create a new session for data storage.
    
    Returns:
        A dictionary containing the new session ID.
    """
    session_id = create_session()
    return {"session_id": session_id}


@mcp.tool()
def list_session_data(
        session_id: str = Field(description="Session ID to list data for")
) -> dict:
    """
    List all keys stored in a session.
    
    Args:
        session_id: The session identifier
        
    Returns:
        A dictionary containing the list of keys in the session.
    """
    keys = get_session_keys(session_id)
    return {
        "session_id": session_id,
        "keys": keys
    }


@mcp.tool()
def store_data_in_session(
        session_id: str = Field(description="Session ID to store data in"),
        key: str = Field(description="Key to store the data under"),
        data: dict = Field(description="Data to store")
) -> dict:
    """
    Store arbitrary data in a session.
    
    Args:
        session_id: The session identifier
        key: The key to store the data under
        data: The data to store
        
    Returns:
        A confirmation message.
    """
    save_session_data(session_id, key, data)
    return {
        "session_id": session_id,
        "key": key,
        "status": "success",
        "message": f"Data stored under key '{key}' in session '{session_id}'"
    }


@mcp.tool()
def retrieve_data_from_session(
        session_id: str = Field(description="Session ID to retrieve data from"),
        key: str = Field(description="Key of the data to retrieve")
) -> dict:
    """
    Retrieve arbitrary data from a session.
    
    Args:
        session_id: The session identifier
        key: The key of the data to retrieve
        
    Returns:
        The stored data if found, an error message otherwise.
    """
    data = get_session_data(session_id, key)
    
    if data is None:
        return {
            "session_id": session_id,
            "key": key,
            "status": "error",
            "message": f"No data found for key '{key}' in session '{session_id}'",
            "available_keys": get_session_keys(session_id)
        }
    
    return {
        "session_id": session_id,
        "key": key,
        "data": data,
        "status": "success"
    }


@mcp.tool()
def delete_session_data_by_key(
        session_id: str = Field(description="Session ID to delete data from"),
        key: str = Field(description="Key of the data to delete")
) -> dict:
    """
    Delete data from a session by key.
    
    Args:
        session_id: The session identifier
        key: The key of the data to delete
        
    Returns:
        A confirmation message.
    """
    clear_session(session_id, key)
    return {
        "session_id": session_id,
        "key": key,
        "status": "success",
        "message": f"Data with key '{key}' deleted from session '{session_id}'"
    }


@mcp.tool()
def delete_entire_session(
        session_id: str = Field(description="Session ID to delete")
) -> dict:
    """
    Delete an entire session.
    
    Args:
        session_id: The session identifier to delete
        
    Returns:
        A confirmation message.
    """
    clear_session(session_id)
    return {
        "session_id": session_id,
        "status": "success",
        "message": f"Session '{session_id}' and all its data have been deleted"
    }
