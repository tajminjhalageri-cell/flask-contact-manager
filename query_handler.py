"""
SQL Query Handler - Interactive Queries with User Input
This module demonstrates how to use parameterized SQL queries with user input
"""

import sqlite3
from datetime import datetime

class ContactQueryHandler:
    """Handle database queries with user input"""
    
    def __init__(self, db_file='contacts.db'):
        self.db_file = db_file
    
    def get_connection(self):
        """Create database connection"""
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        return conn
    
    # ==================== QUERY 1: INSERT NEW CONTACT ====================
    def insert_contact(self, username, contact):
        """
        INSERT NEW CONTACT - Requires user input
        Parameters: username (str), contact (str)
        SQL: INSERT INTO contacts (username, contact) VALUES (?, ?)
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO contacts (username, contact) VALUES (?, ?)', 
                         (username, contact))
            conn.commit()
            result = {'success': True, 'message': f'Contact {username} added', 'id': cursor.lastrowid}
            conn.close()
            return result
        except sqlite3.IntegrityError as e:
            return {'success': False, 'error': f'Username already exists: {username}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== QUERY 2: GET ALL CONTACTS ====================
    def get_all_contacts(self):
        """
        GET ALL CONTACTS
        Returns all contacts sorted by creation date
        SQL: SELECT id, username, contact, created_at FROM contacts ORDER BY created_at DESC
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id, username, contact, created_at FROM contacts ORDER BY created_at DESC')
            contacts = cursor.fetchall()
            conn.close()
            return {'success': True, 'total': len(contacts), 'contacts': [dict(c) for c in contacts]}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== QUERY 3: SEARCH BY USERNAME (EXACT) ====================
    def search_username_exact(self, username):
        """
        SEARCH BY USERNAME - Requires user input (exact match)
        Parameter: username (str)
        SQL: SELECT * FROM contacts WHERE username = ?
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id, username, contact, created_at FROM contacts WHERE username = ?', 
                         (username,))
            contact = cursor.fetchone()
            conn.close()
            
            if contact:
                return {'success': True, 'found': True, 'contact': dict(contact)}
            return {'success': True, 'found': False, 'message': f'No contact found with username: {username}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== QUERY 4: SEARCH BY USERNAME (PARTIAL) ====================
    def search_username_partial(self, search_term):
        """
        SEARCH BY PARTIAL USERNAME - Requires user input
        Parameter: search_term (str) - partial username to search
        SQL: SELECT * FROM contacts WHERE username LIKE ?
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id, username, contact, created_at FROM contacts WHERE username LIKE ? ORDER BY username ASC', 
                         (f'%{search_term}%',))
            contacts = cursor.fetchall()
            conn.close()
            
            return {'success': True, 'search_term': search_term, 'found': len(contacts), 
                   'contacts': [dict(c) for c in contacts]}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== QUERY 5: SEARCH BY CONTACT (EXACT) ====================
    def search_contact_exact(self, contact):
        """
        SEARCH BY CONTACT NUMBER - Requires user input (exact match)
        Parameter: contact (str)
        SQL: SELECT * FROM contacts WHERE contact = ?
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id, username, contact, created_at FROM contacts WHERE contact = ?', 
                         (contact,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {'success': True, 'found': True, 'contact': dict(result)}
            return {'success': True, 'found': False, 'message': f'No contact found with number: {contact}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== QUERY 6: SEARCH BY CONTACT (PARTIAL) ====================
    def search_contact_partial(self, contact_partial):
        """
        SEARCH BY PARTIAL CONTACT NUMBER - Requires user input
        Parameter: contact_partial (str)
        SQL: SELECT * FROM contacts WHERE contact LIKE ?
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id, username, contact, created_at FROM contacts WHERE contact LIKE ? ORDER BY username ASC', 
                         (f'%{contact_partial}%',))
            contacts = cursor.fetchall()
            conn.close()
            
            return {'success': True, 'search_term': contact_partial, 'found': len(contacts), 
                   'contacts': [dict(c) for c in contacts]}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== QUERY 7: UPDATE CONTACT INFORMATION ====================
    def update_contact(self, username, new_contact):
        """
        UPDATE CONTACT NUMBER - Requires user input
        Parameters: username (str), new_contact (str)
        SQL: UPDATE contacts SET contact = ? WHERE username = ?
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE contacts SET contact = ? WHERE username = ?', 
                         (new_contact, username))
            conn.commit()
            
            if cursor.rowcount == 0:
                return {'success': False, 'message': f'No contact found with username: {username}'}
            
            conn.close()
            return {'success': True, 'message': f'Contact updated for {username}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== QUERY 8: UPDATE USERNAME ====================
    def update_username(self, old_username, new_username):
        """
        UPDATE USERNAME - Requires user input
        Parameters: old_username (str), new_username (str)
        SQL: UPDATE contacts SET username = ? WHERE username = ?
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE contacts SET username = ? WHERE username = ?', 
                         (new_username, old_username))
            conn.commit()
            
            if cursor.rowcount == 0:
                return {'success': False, 'message': f'No contact found with username: {old_username}'}
            
            conn.close()
            return {'success': True, 'message': f'Username updated from {old_username} to {new_username}'}
        except sqlite3.IntegrityError:
            return {'success': False, 'error': f'Username {new_username} already exists'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== QUERY 9: DELETE BY USERNAME ====================
    def delete_by_username(self, username):
        """
        DELETE CONTACT - Requires user input (by username)
        Parameter: username (str)
        SQL: DELETE FROM contacts WHERE username = ?
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM contacts WHERE username = ?', (username,))
            conn.commit()
            
            if cursor.rowcount == 0:
                return {'success': False, 'message': f'No contact found with username: {username}'}
            
            conn.close()
            return {'success': True, 'message': f'Contact {username} deleted'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== QUERY 10: DELETE BY ID ====================
    def delete_by_id(self, contact_id):
        """
        DELETE CONTACT - Requires user input (by ID)
        Parameter: contact_id (int)
        SQL: DELETE FROM contacts WHERE id = ?
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
            conn.commit()
            
            if cursor.rowcount == 0:
                return {'success': False, 'message': f'No contact found with ID: {contact_id}'}
            
            conn.close()
            return {'success': True, 'message': f'Contact with ID {contact_id} deleted'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== QUERY 11: COUNT TOTAL CONTACTS ====================
    def count_total_contacts(self):
        """
        COUNT ALL CONTACTS
        SQL: SELECT COUNT(*) FROM contacts
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) as total FROM contacts')
            result = cursor.fetchone()
            conn.close()
            return {'success': True, 'total_contacts': result['total']}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== QUERY 12: COUNT WITH FILTER ====================
    def count_by_username_pattern(self, search_term):
        """
        COUNT CONTACTS BY USERNAME PATTERN - Requires user input
        Parameter: search_term (str)
        SQL: SELECT COUNT(*) FROM contacts WHERE username LIKE ?
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) as count FROM contacts WHERE username LIKE ?', 
                         (f'%{search_term}%',))
            result = cursor.fetchone()
            conn.close()
            return {'success': True, 'search_term': search_term, 'matching_count': result['count']}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== QUERY 13: GET BY ID ====================
    def get_by_id(self, contact_id):
        """
        GET CONTACT BY ID - Requires user input
        Parameter: contact_id (int)
        SQL: SELECT * FROM contacts WHERE id = ?
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id, username, contact, created_at FROM contacts WHERE id = ?', 
                         (contact_id,))
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {'success': True, 'found': True, 'contact': dict(result)}
            return {'success': True, 'found': False, 'message': f'No contact found with ID: {contact_id}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== QUERY 14: PAGINATED RESULTS ====================
    def get_paginated(self, page=1, limit=5):
        """
        GET PAGINATED CONTACTS - Requires user input
        Parameters: page (int), limit (int)
        SQL: SELECT * FROM contacts ORDER BY created_at DESC LIMIT ? OFFSET ?
        """
        try:
            offset = (page - 1) * limit
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get total count
            cursor.execute('SELECT COUNT(*) as total FROM contacts')
            total = cursor.fetchone()['total']
            
            # Get paginated results
            cursor.execute('SELECT id, username, contact, created_at FROM contacts ORDER BY created_at DESC LIMIT ? OFFSET ?', 
                         (limit, offset))
            contacts = cursor.fetchall()
            conn.close()
            
            total_pages = (total + limit - 1) // limit
            return {'success': True, 'page': page, 'limit': limit, 'total_contacts': total, 
                   'total_pages': total_pages, 'contacts': [dict(c) for c in contacts]}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== QUERY 15: SORTED RESULTS ====================
    def get_sorted(self, sort_by='username', order='ASC'):
        """
        GET SORTED CONTACTS - Requires user input
        Parameters: sort_by (str), order (str - 'ASC' or 'DESC')
        SQL: SELECT * FROM contacts ORDER BY {sort_by} {order}
        """
        try:
            # Validate inputs to prevent SQL injection
            valid_sorts = ['username', 'contact', 'created_at', 'id']
            valid_orders = ['ASC', 'DESC']
            
            if sort_by.lower() not in valid_sorts:
                return {'success': False, 'error': f'Invalid sort field: {sort_by}'}
            if order.upper() not in valid_orders:
                return {'success': False, 'error': f'Invalid sort order: {order}'}
            
            conn = self.get_connection()
            cursor = conn.cursor()
            query = f'SELECT id, username, contact, created_at FROM contacts ORDER BY {sort_by} {order}'
            cursor.execute(query)
            contacts = cursor.fetchall()
            conn.close()
            
            return {'success': True, 'sort_by': sort_by, 'order': order, 'total': len(contacts), 
                   'contacts': [dict(c) for c in contacts]}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== QUERY 16: ADVANCED SEARCH ====================
    def search_combined(self, username_pattern, contact_pattern):
        """
        ADVANCED SEARCH - USERNAME AND CONTACT - Requires user input
        Parameters: username_pattern (str), contact_pattern (str)
        SQL: SELECT * FROM contacts WHERE username LIKE ? AND contact LIKE ?
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id, username, contact, created_at FROM contacts WHERE username LIKE ? AND contact LIKE ?', 
                         (f'%{username_pattern}%', f'%{contact_pattern}%'))
            contacts = cursor.fetchall()
            conn.close()
            
            return {'success': True, 'username_pattern': username_pattern, 'contact_pattern': contact_pattern,
                   'found': len(contacts), 'contacts': [dict(c) for c in contacts]}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== QUERY 17: CHECK IF USERNAME EXISTS ====================
    def username_exists(self, username):
        """
        CHECK IF USERNAME EXISTS - Requires user input
        Parameter: username (str)
        SQL: SELECT COUNT(*) FROM contacts WHERE username = ?
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) as count FROM contacts WHERE username = ?', (username,))
            result = cursor.fetchone()
            conn.close()
            
            exists = result['count'] > 0
            return {'success': True, 'username': username, 'exists': exists}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== QUERY 18: CHECK IF CONTACT EXISTS ====================
    def contact_exists(self, contact):
        """
        CHECK IF CONTACT EXISTS - Requires user input
        Parameter: contact (str)
        SQL: SELECT COUNT(*) FROM contacts WHERE contact = ?
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) as count FROM contacts WHERE contact = ?', (contact,))
            result = cursor.fetchone()
            conn.close()
            
            exists = result['count'] > 0
            return {'success': True, 'contact': contact, 'exists': exists}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== QUERY 19: GET LATEST N CONTACTS ====================
    def get_latest(self, limit=5):
        """
        GET LATEST N CONTACTS - Requires user input
        Parameter: limit (int)
        SQL: SELECT * FROM contacts ORDER BY created_at DESC LIMIT ?
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT id, username, contact, created_at FROM contacts ORDER BY created_at DESC LIMIT ?', 
                         (limit,))
            contacts = cursor.fetchall()
            conn.close()
            
            return {'success': True, 'limit': limit, 'total_retrieved': len(contacts), 
                   'contacts': [dict(c) for c in contacts]}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    # ==================== QUERY 21: GET STATISTICS ====================
    def get_statistics(self):
        """
        GET DATABASE STATISTICS
        Returns: total contacts, latest added, earliest added
        SQL: SELECT COUNT(*), MAX(created_at), MIN(created_at) FROM contacts
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) as total, MAX(created_at) as latest, MIN(created_at) as earliest FROM contacts')
            result = cursor.fetchone()
            conn.close()
            
            return {'success': True, 'total_contacts': result['total'], 'latest_added': result['latest'], 
                   'earliest_added': result['earliest']}
        except Exception as e:
            return {'success': False, 'error': str(e)}


# ============================================================================
# EXAMPLE USAGE
# ============================================================================
if __name__ == '__main__':
    handler = ContactQueryHandler()
    
    print("=" * 60)
    print("SQL QUERY HANDLER - USER INPUT EXAMPLES")
    print("=" * 60)
    
    # Example 1: Insert contact with user input
    print("\n1. INSERT CONTACT (User Input: John Doe, 5551234567)")
    result = handler.insert_contact('John Doe', '5551234567')
    print(result)
    
    # Example 2: Search by exact username
    print("\n2. SEARCH BY EXACT USERNAME (User Input: 'John Doe')")
    result = handler.search_username_exact('John Doe')
    print(result)
    
    # Example 3: Search by partial username
    print("\n3. SEARCH BY PARTIAL USERNAME (User Input: 'John')")
    result = handler.search_username_partial('John')
    print(result)
    
    # Example 4: Get all contacts
    print("\n4. GET ALL CONTACTS")
    result = handler.get_all_contacts()
    print(result)
    
    # Example 5: Count total
    print("\n5. COUNT TOTAL CONTACTS")
    result = handler.count_total_contacts()
    print(result)
    
    # Example 6: Get paginated results
    print("\n6. GET PAGINATED (Page 1, Limit 2)")
    result = handler.get_paginated(page=1, limit=2)
    print(result)
    
    # Example 7: Sort contacts
    print("\n7. GET SORTED BY USERNAME ASC")
    result = handler.get_sorted(sort_by='username', order='ASC')
    print(result)
    
    # Example 8: Check if exists
    print("\n8. CHECK IF USERNAME 'John Doe' EXISTS")
    result = handler.username_exists('John Doe')
    print(result)
    
    # Example 9: Get latest contacts
    print("\n9. GET LATEST 3 CONTACTS")
    result = handler.get_latest(limit=3)
    print(result)
    
    # Example 10: Get statistics
    print("\n10. GET DATABASE STATISTICS")
    result = handler.get_statistics()
    print(result)
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)
