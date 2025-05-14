# Session-Based Storage for Explorium MCP Server

This PR adds session-based storage capabilities to the Explorium MCP Server using DuckDB. This enhancement allows for storing large datasets in a database rather than passing them through the context, enabling more efficient data management and retrieval.

## Key Features

- **DuckDB Session Storage**: Persistent storage for all API response data using DuckDB.
- **Session ID Management**: Functions to generate, store, and retrieve data with session IDs.
- **Tool Integration**: Updated MCP tools to use session storage for large payloads.
- **Improved Data Flow**: Reduced context size by keeping large payloads in the database.

## Usage Pattern

1. **First Call**: The client sends input, which is stored in DuckDB with a generated session ID, and the session ID is returned to the LLM.
2. **Follow-up Calls**: The LLM issues requests that reference the session ID to access previously stored data.

## Implementation Details

- Added `storage` module with session management functionality.
- Added session ID parameter to all relevant API tools.
- Added utility tools for session data management.
- Updated `shared.py` with session data helper functions.
- Added tests for session storage.

## Usage Example

```python
# Initial request - returns a session_id in the response
result = match_businesses(businesses_to_match=[{"name": "Google"}])
session_id = result["session_id"]

# Retrieve stored data using the session_id
stored_data = get_session_businesses(
    session_id=session_id,
    key="match_businesses_result"
)

# Use the retrieved data
business_ids = [business["business_id"] for business in stored_data["data"]["businesses"]]

# Pass session_id to another tool to continue using the same session
enrichment_data = enrich_businesses_firmographics(
    business_ids=business_ids,
    session_id=session_id
)
```

## Benefits

- **Reduced Context Size**: Large data payloads are stored in the database instead of being passed in the context.
- **Improved Performance**: Faster execution with smaller contexts.
- **Better Data Management**: Easier tracking of data flow through the application.
- **Persistent Storage**: Data remains available between function calls.

## Technical Details

- **Database**: DuckDB file-based database.
- **Table Schema**: `session_id TEXT, key TEXT, value JSON, created_at TIMESTAMP`.
- **Dependencies**: Added DuckDB to project dependencies.
