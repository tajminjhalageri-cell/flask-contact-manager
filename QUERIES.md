# SQL Database Queries - Contact Manager API

## Overview
All queries interact with the SQLite database (`contacts.db`). Data is automatically migrated from `Book1.csv` on first run.

## Available Endpoints

### 1. **Get All Contacts**
- **URL:** `GET /contacts`
- **Purpose:** Retrieve all contacts sorted by creation date (newest first)
- **Response:** Array of contact objects with `id`, `username`, `contact`, `created_at`
- **Example:**
  ```
  http://127.0.0.1:5000/contacts
  ```

### 2. **Get Specific Contact**
- **URL:** `GET /contact/<username>`
- **Purpose:** Get a single contact by exact username match
- **Response:** Single contact object or 404 error
- **Example:**
  ```
  http://127.0.0.1:5000/contact/John%20Smith
  ```

### 3. **Database Statistics**
- **URL:** `GET /stats`
- **Purpose:** Get database metadata and statistics
- **Returns:** 
  - Total contact count
  - Database file name
  - Database size in bytes
  - Latest contact added
- **Example:**
  ```
  http://127.0.0.1:5000/stats
  ```

### 4. **Search Contacts (by Username)**
- **URL:** `GET /search?q=<query>`
- **Purpose:** Search for contacts by partial username match (case-insensitive)
- **Parameters:**
  - `q`: Search query (required)
- **Returns:** Array of matching contacts
- **Example:**
  ```
  http://127.0.0.1:5000/search?q=Thejas
  http://127.0.0.1:5000/search?q=John
  ```

### 5. **Search Contacts (by Contact Number)**
- **URL:** `GET /query/by-contact?c=<contact>`
- **Purpose:** Search for contacts by partial contact number match
- **Parameters:**
  - `c`: Contact number or partial match (required)
- **Returns:** Array of matching contacts
- **Example:**
  ```
  http://127.0.0.1:5000/query/by-contact?c=636
  http://127.0.0.1:5000/query/by-contact?c=9876
  ```

### 6. **Paginated Results**
- **URL:** `GET /contacts/paginated?page=<page>&limit=<limit>`
- **Purpose:** Get contacts with pagination support
- **Parameters:**
  - `page`: Page number (default: 1)
  - `limit`: Records per page (default: 5)
- **Returns:** 
  - Paginated contact array
  - Current page, limit, total contacts, total pages
- **Example:**
  ```
  http://127.0.0.1:5000/contacts/paginated?page=1&limit=2
  http://127.0.0.1:5000/contacts/paginated?page=2&limit=5
  ```

### 7. **Sorted Results**
- **URL:** `GET /query/sorted?sort=<field>&order=<order>`
- **Purpose:** Get all contacts sorted by specified field
- **Parameters:**
  - `sort`: Field to sort by (`username`, `contact`, `created_at`) (default: `username`)
  - `order`: Sort order (`asc` or `desc`) (default: `asc`)
- **Returns:** Sorted contact array
- **Example:**
  ```
  http://127.0.0.1:5000/query/sorted?sort=contact&order=desc
  http://127.0.0.1:5000/query/sorted?sort=created_at&order=asc
  ```

### 8. **Export All Contacts**
- **URL:** `GET /export`
- **Purpose:** Export all contacts as JSON for backup/integration
- **Returns:** 
  - Export date/time
  - Total records
  - Complete contact array
- **Example:**
  ```
  http://127.0.0.1:5000/export
  ```

### 9. **Health Check**
- **URL:** `GET /health`
- **Purpose:** Verify server and database connectivity
- **Returns:** Server status and database connection status
- **Example:**
  ```
  http://127.0.0.1:5000/health
  ```

## Write Operations

### Add Contact
- **URL:** `POST /add`
- **Body (JSON):**
  ```json
  {
    "username": "Contact Name",
    "contact": "Contact Number"
  }
  ```
- **Validation:**
  - Username: minimum 2 characters, unique
  - Contact: minimum 5 characters
- **Response:** 201 with created contact or 400 error

### Delete Contact
- **URL:** `DELETE /delete/<username>`
- **Purpose:** Delete contact by username
- **Response:** 200 success or 404 not found

## Database Schema

```sql
CREATE TABLE contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    contact TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Current Data (Sample)

| ID | Username | Contact | Created_at |
|----|----------|---------|-----------|
| 3 | Thejas kg | 7483605864 | 2026-06-05 04:58:10 |
| 4 | Sanjana | 6364165715 | 2026-06-05 04:58:10 |
| 1 | John Smith | 9876543210 | 2026-06-05 04:54:20 |

## Migration Information

- **CSV Data:** Automatically imported from `Book1.csv` on first database initialization
- **Migration Flag:** `.migration_done` file prevents duplicate migrations
- **Imported Records:** 2 contacts from original CSV data

## Usage Examples in cURL

```bash
# Get all contacts
curl http://127.0.0.1:5000/contacts

# Search by username
curl "http://127.0.0.1:5000/search?q=Thejas"

# Search by contact number
curl "http://127.0.0.1:5000/query/by-contact?c=636"

# Get paginated results
curl "http://127.0.0.1:5000/contacts/paginated?page=1&limit=2"

# Sort by contact descending
curl "http://127.0.0.1:5000/query/sorted?sort=contact&order=desc"

# Export all
curl http://127.0.0.1:5000/export

# Get stats
curl http://127.0.0.1:5000/stats

# Health check
curl http://127.0.0.1:5000/health

# Add contact
curl -X POST http://127.0.0.1:5000/add \
  -H "Content-Type: application/json" \
  -d '{"username": "Jane Doe", "contact": "5551234567"}'

# Delete contact
curl -X DELETE http://127.0.0.1:5000/delete/Jane%20Doe
```

## Notes

- All responses are JSON formatted
- Dates/times are in ISO 8601 format
- Search queries are case-insensitive
- Pagination is 1-indexed
- Maximum characters enforced: username (100), contact (20)
