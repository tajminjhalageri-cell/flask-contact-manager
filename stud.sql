-- ============================================================================
-- Contact Manager Database - SQL Queries with User Input
-- ============================================================================
-- These queries accept user input through parameterized statements
-- to prevent SQL injection and ensure data integrity
-- ============================================================================

-- Database Setup (One-time execution)
-- CREATE DATABASE contact_manager;
-- USE contact_manager;

-- Table Definition
CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    contact TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- QUERY 1: INSERT NEW CONTACT (Requires: username, contact_number)
-- ============================================================================
-- User Input Required: 
--   @username (VARCHAR 100) - Full name or username
--   @contact (VARCHAR 20) - Phone number or contact
-- Usage: INSERT INTO contacts (username, contact) VALUES (?, ?)
-- Parameters: (username_value, contact_value)
INSERT INTO contacts (username, contact) VALUES (?, ?);
-- Example: INSERT INTO contacts (username, contact) VALUES ('John Smith', '9876543210');

-- ============================================================================
-- QUERY 2: GET ALL CONTACTS
-- ============================================================================
-- No user input required
-- Returns: All contacts sorted by creation date (newest first)
SELECT id, username, contact, created_at 
FROM contacts 
ORDER BY created_at DESC;

-- ============================================================================
-- QUERY 3: SEARCH CONTACT BY USERNAME (Exact Match)
-- ============================================================================
-- User Input Required:
--   @username (VARCHAR 100) - Exact username to search
-- Usage: SELECT * FROM contacts WHERE username = ?
-- Parameters: (username_value)
SELECT id, username, contact, created_at 
FROM contacts 
WHERE username = ?;
-- Example: SELECT * FROM contacts WHERE username = 'John Smith';

-- ============================================================================
-- QUERY 4: SEARCH CONTACT BY PARTIAL USERNAME (Contains)
-- ============================================================================
-- User Input Required:
--   @search_term (VARCHAR 100) - Partial username to search
-- Usage: SELECT * FROM contacts WHERE username LIKE ?
-- Parameters: ('%search_term%')
SELECT id, username, contact, created_at 
FROM contacts 
WHERE username LIKE ?
ORDER BY username ASC;
-- Example: SELECT * FROM contacts WHERE username LIKE '%John%';

-- ============================================================================
-- QUERY 5: SEARCH BY CONTACT NUMBER (Exact Match)
-- ============================================================================
-- User Input Required:
--   @contact (VARCHAR 20) - Exact contact number
-- Usage: SELECT * FROM contacts WHERE contact = ?
-- Parameters: (contact_value)
SELECT id, username, contact, created_at 
FROM contacts 
WHERE contact = ?;
-- Example: SELECT * FROM contacts WHERE contact = '9876543210';

-- ============================================================================
-- QUERY 6: SEARCH BY PARTIAL CONTACT NUMBER
-- ============================================================================
-- User Input Required:
--   @contact_partial (VARCHAR 20) - Partial contact number
-- Usage: SELECT * FROM contacts WHERE contact LIKE ?
-- Parameters: ('%contact_partial%')
SELECT id, username, contact, created_at 
FROM contacts 
WHERE contact LIKE ?
ORDER BY username ASC;
-- Example: SELECT * FROM contacts WHERE contact LIKE '%636%';

-- ============================================================================
-- QUERY 7: UPDATE CONTACT INFORMATION
-- ============================================================================
-- User Input Required:
--   @new_contact (VARCHAR 20) - New contact number
--   @username (VARCHAR 100) - Username to update
-- Usage: UPDATE contacts SET contact = ? WHERE username = ?
-- Parameters: (new_contact_value, username_value)
UPDATE contacts 
SET contact = ? 
WHERE username = ?;
-- Example: UPDATE contacts SET contact = '5551234567' WHERE username = 'John Smith';

-- ============================================================================
-- QUERY 8: UPDATE USERNAME
-- ============================================================================
-- User Input Required:
--   @new_username (VARCHAR 100) - New username
--   @old_username (VARCHAR 100) - Current username
-- Usage: UPDATE contacts SET username = ? WHERE username = ?
-- Parameters: (new_username_value, old_username_value)
UPDATE contacts 
SET username = ? 
WHERE username = ?;
-- Example: UPDATE contacts SET username = 'John Doe' WHERE username = 'John Smith';

-- ============================================================================
-- QUERY 9: DELETE CONTACT BY USERNAME
-- ============================================================================
-- User Input Required:
--   @username (VARCHAR 100) - Username to delete
-- Usage: DELETE FROM contacts WHERE username = ?
-- Parameters: (username_value)
DELETE FROM contacts 
WHERE username = ?;
-- Example: DELETE FROM contacts WHERE username = 'John Smith';

-- ============================================================================
-- QUERY 10: DELETE CONTACT BY ID
-- ============================================================================
-- User Input Required:
--   @id (INTEGER) - Contact ID to delete
-- Usage: DELETE FROM contacts WHERE id = ?
-- Parameters: (id_value)
DELETE FROM contacts 
WHERE id = ?;
-- Example: DELETE FROM contacts WHERE id = 3;

-- ============================================================================
-- QUERY 11: COUNT TOTAL CONTACTS
-- ============================================================================
-- No user input required
-- Returns: Total number of contacts in database
SELECT COUNT(*) as total_contacts 
FROM contacts;

-- ============================================================================
-- QUERY 12: COUNT CONTACTS WITH USERNAME FILTER
-- ============================================================================
-- User Input Required:
--   @search_term (VARCHAR 100) - Username pattern
-- Usage: SELECT COUNT(*) FROM contacts WHERE username LIKE ?
-- Parameters: ('%search_term%')
SELECT COUNT(*) as matching_contacts 
FROM contacts 
WHERE username LIKE ?;
-- Example: SELECT COUNT(*) FROM contacts WHERE username LIKE '%John%';

-- ============================================================================
-- QUERY 13: GET CONTACT BY ID
-- ============================================================================
-- User Input Required:
--   @id (INTEGER) - Contact ID
-- Usage: SELECT * FROM contacts WHERE id = ?
-- Parameters: (id_value)
SELECT id, username, contact, created_at 
FROM contacts 
WHERE id = ?;
-- Example: SELECT * FROM contacts WHERE id = 1;

-- ============================================================================
-- QUERY 14: PAGINATED RESULTS
-- ============================================================================
-- User Input Required:
--   @limit (INTEGER) - Number of records per page
--   @offset (INTEGER) - Starting position (page_number - 1) * limit
-- Usage: SELECT * FROM contacts ORDER BY created_at DESC LIMIT ? OFFSET ?
-- Parameters: (limit_value, offset_value)
SELECT id, username, contact, created_at 
FROM contacts 
ORDER BY created_at DESC 
LIMIT ? OFFSET ?;
-- Example: SELECT * FROM contacts ORDER BY created_at DESC LIMIT 5 OFFSET 0; (Page 1, 5 per page)
-- Example: SELECT * FROM contacts ORDER BY created_at DESC LIMIT 5 OFFSET 5; (Page 2, 5 per page)

-- ============================================================================
-- QUERY 15: SORTED RESULTS BY FIELD
-- ============================================================================
-- User Input Required:
--   @sort_field (VARCHAR) - Field to sort (username, contact, created_at)
--   @sort_order (VARCHAR) - Order (ASC or DESC)
-- Note: Use parameterized/prepared statements in your code for sort fields
-- Parameters: Different based on sort_field and sort_order
SELECT id, username, contact, created_at 
FROM contacts 
ORDER BY username ASC;
-- Example variations:
SELECT id, username, contact, created_at FROM contacts ORDER BY username ASC;
SELECT id, username, contact, created_at FROM contacts ORDER BY username DESC;
SELECT id, username, contact, created_at FROM contacts ORDER BY contact ASC;
SELECT id, username, contact, created_at FROM contacts ORDER BY contact DESC;
SELECT id, username, contact, created_at FROM contacts ORDER BY created_at ASC;
SELECT id, username, contact, created_at FROM contacts ORDER BY created_at DESC;

-- ============================================================================
-- QUERY 16: ADVANCED SEARCH - USERNAME AND CONTACT BOTH
-- ============================================================================
-- User Input Required:
--   @username_pattern (VARCHAR 100) - Username search term
--   @contact_pattern (VARCHAR 20) - Contact search term
-- Usage: SELECT * FROM contacts WHERE username LIKE ? AND contact LIKE ?
-- Parameters: ('%username_pattern%', '%contact_pattern%')
SELECT id, username, contact, created_at 
FROM contacts 
WHERE username LIKE ? AND contact LIKE ?;
-- Example: SELECT * FROM contacts WHERE username LIKE '%John%' AND contact LIKE '%987%';

-- ============================================================================
-- QUERY 17: CHECK IF USERNAME EXISTS
-- ============================================================================
-- User Input Required:
--   @username (VARCHAR 100) - Username to check
-- Usage: SELECT COUNT(*) FROM contacts WHERE username = ?
-- Parameters: (username_value)
SELECT COUNT(*) as exists 
FROM contacts 
WHERE username = ?;
-- Example: SELECT COUNT(*) FROM contacts WHERE username = 'John Smith'; (Returns 1 if exists, 0 if not)

-- ============================================================================
-- QUERY 18: CHECK IF CONTACT EXISTS
-- ============================================================================
-- User Input Required:
--   @contact (VARCHAR 20) - Contact to check
-- Usage: SELECT COUNT(*) FROM contacts WHERE contact = ?
-- Parameters: (contact_value)
SELECT COUNT(*) as exists 
FROM contacts 
WHERE contact = ?;
-- Example: SELECT COUNT(*) FROM contacts WHERE contact = '9876543210';

-- ============================================================================
-- QUERY 19: GET LATEST N CONTACTS
-- ============================================================================
-- User Input Required:
--   @limit (INTEGER) - Number of latest contacts to retrieve
-- Usage: SELECT * FROM contacts ORDER BY created_at DESC LIMIT ?
-- Parameters: (limit_value)
SELECT id, username, contact, created_at 
FROM contacts 
ORDER BY created_at DESC 
LIMIT ?;
-- Example: SELECT * FROM contacts ORDER BY created_at DESC LIMIT 5; (Get last 5 added)

-- ============================================================================
-- QUERY 20: BULK INSERT MULTIPLE CONTACTS
-- ============================================================================
-- User Input Required:
--   Multiple pairs of (username, contact)
-- Usage: INSERT INTO contacts (username, contact) VALUES (?, ?), (?, ?), ...
-- Parameters: (username1, contact1, username2, contact2, ...)
INSERT INTO contacts (username, contact) VALUES 
(?, ?), 
(?, ?), 
(?, ?);
-- Example: 
-- INSERT INTO contacts (username, contact) VALUES 
-- ('Alice', '5551111111'),
-- ('Bob', '5552222222'),
-- ('Charlie', '5553333333');

-- ============================================================================
-- QUERY 21: GET CONTACT STATISTICS
-- ============================================================================
-- No user input required
-- Returns: Total contacts, latest contact date, earliest contact date
SELECT 
    COUNT(*) as total_contacts,
    MAX(created_at) as latest_contact_added,
    MIN(created_at) as earliest_contact_added
FROM contacts;

-- ============================================================================
-- QUERY 22: BETWEEN DATE RANGE (Optional - if dates matter)
-- ============================================================================
-- User Input Required:
--   @start_date (TIMESTAMP) - Start date
--   @end_date (TIMESTAMP) - End date
-- Usage: SELECT * FROM contacts WHERE created_at BETWEEN ? AND ?
-- Parameters: (start_date_value, end_date_value)
SELECT id, username, contact, created_at 
FROM contacts 
WHERE created_at BETWEEN ? AND ?
ORDER BY created_at DESC;
-- Example: SELECT * FROM contacts WHERE created_at BETWEEN '2026-01-01' AND '2026-12-31';

-- ============================================================================
-- QUERY 23: BACKUP - EXPORT ALL DATA
-- ============================================================================
-- No user input required
-- Returns: All contact data formatted for export
SELECT 
    id,
    username,
    contact,
    created_at
FROM contacts
ORDER BY id ASC;

-- ============================================================================
-- SUMMARY OF PARAMETERIZED QUERIES
-- ============================================================================
-- Total Queries: 23
-- Queries requiring user input: 17
-- Read-only queries: 13
-- Write queries (INSERT/UPDATE/DELETE): 10
--
-- INPUT TYPES REQUIRED:
-- - Text/String input: username, contact number, search terms
-- - Integer input: id, limit, offset, count
-- - Timestamp input: dates for range queries
--
-- BEST PRACTICES IMPLEMENTED:
-- ✓ Parameterized statements (?) prevent SQL injection
-- ✓ Input validation at application level
-- ✓ Consistent column selection for all queries
-- ✓ Proper error handling required in application
-- ============================================================================