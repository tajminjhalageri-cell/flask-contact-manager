from flask import Flask, render_template, request, jsonify
import sqlite3
import os
import csv
from datetime import datetime
import json

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Database configuration
DB_FILE = 'contacts.db'
CSV_FILE = 'Book1.csv'
MIGRATION_FLAG = '.migration_done'

def get_db_connection():
    """Get database connection with row factory"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def migrate_csv_to_db():
    """Migrate contacts from CSV file to database"""
    if os.path.exists(MIGRATION_FLAG):
        return  # Already migrated
    
    if not os.path.exists(CSV_FILE):
        # Create migration flag even if CSV doesn't exist
        open(MIGRATION_FLAG, 'a').close()
        return
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        with open(CSV_FILE, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                username = row.get('username', '').strip()
                contact = row.get('contact', '').strip()
                
                if username and contact:
                    try:
                        cursor.execute(
                            'INSERT INTO contacts (username, contact) VALUES (?, ?)',
                            (username, contact)
                        )
                        count += 1
                    except sqlite3.IntegrityError:
                        # Skip if username already exists
                        pass
            
            conn.commit()
            print(f"✓ Migrated {count} contacts from CSV to database")
        
        # Create migration flag
        open(MIGRATION_FLAG, 'a').close()
        conn.close()
    except Exception as e:
        print(f"Migration error: {e}")

def init_db():
    """Initialize database with contacts table and migrate data"""
    db_exists = os.path.exists(DB_FILE)
    
    if not db_exists:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                contact TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    # Migrate CSV data to database
    migrate_csv_to_db()

# Initialize database on startup
init_db()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contacts', methods=['GET'])
def get_all():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, contact, created_at FROM contacts ORDER BY created_at DESC')
        contacts = cursor.fetchall()
        conn.close()
        
        result = []
        for contact in contacts:
            result.append({
                'id': contact['id'],
                'username': contact['username'],
                'contact': contact['contact'],
                'created_at': contact['created_at']
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/contact/<username>', methods=['GET'])
def get_contact(username):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, contact, created_at FROM contacts WHERE username = ?', (username,))
        contact = cursor.fetchone()
        conn.close()
        
        if contact:
            return jsonify({
                'id': contact['id'],
                'username': contact['username'],
                'contact': contact['contact'],
                'created_at': contact['created_at']
            })
        return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add', methods=['POST'])
def add_contact():
    try:
        data = request.json
        
        # Validation
        if not data or not data.get('username') or not data.get('contact'):
            return jsonify({'error': 'Username and contact are required'}), 400
        
        username = data['username'].strip()
        contact = data['contact'].strip()
        
        # Validate input
        if len(username) < 2:
            return jsonify({'error': 'Username must be at least 2 characters'}), 400
        
        if len(contact) < 5:
            return jsonify({'error': 'Contact must be at least 5 characters'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('INSERT INTO contacts (username, contact) VALUES (?, ?)', (username, contact))
            conn.commit()
            
            # Return the created contact
            contact_id = cursor.lastrowid
            cursor.execute('SELECT id, username, contact, created_at FROM contacts WHERE id = ?', (contact_id,))
            new_contact = cursor.fetchone()
            conn.close()
            
            return jsonify({
                'message': 'Contact added successfully',
                'contact': {
                    'id': new_contact['id'],
                    'username': new_contact['username'],
                    'contact': new_contact['contact'],
                    'created_at': new_contact['created_at']
                }
            }), 201
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'error': 'Username already exists'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/delete/<username>', methods=['DELETE'])
def delete_contact(username):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if contact exists
        cursor.execute('SELECT id FROM contacts WHERE username = ?', (username,))
        contact = cursor.fetchone()
        
        if not contact:
            conn.close()
            return jsonify({'error': 'User not found'}), 404
        
        # Delete the contact
        cursor.execute('DELETE FROM contacts WHERE username = ?', (username,))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Contact deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        conn.close()
        return jsonify({'status': 'Server is running', 'database': 'Connected'}), 200
    except Exception as e:
        return jsonify({'status': 'Server is running', 'database': 'Disconnected', 'error': str(e)}), 500

# Additional Query Endpoints

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get database statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total contacts
        cursor.execute('SELECT COUNT(*) as count FROM contacts')
        total = cursor.fetchone()['count']
        
        # Total contacts with detailed info
        cursor.execute('SELECT COUNT(*) as count FROM contacts')
        contact_count = cursor.fetchone()['count']
        
        # Database size
        cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
        db_size = cursor.fetchone()
        
        # Latest contact
        cursor.execute('SELECT username, contact, created_at FROM contacts ORDER BY created_at DESC LIMIT 1')
        latest = cursor.fetchone()
        
        conn.close()
        
        return jsonify({
            'total_contacts': contact_count,
            'database_file': DB_FILE,
            'database_size_bytes': db_size['size'] if db_size else 0,
            'latest_contact': {
                'username': latest['username'],
                'contact': latest['contact'],
                'created_at': latest['created_at']
            } if latest else None
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search', methods=['GET'])
def search_contacts():
    """Search contacts by username pattern"""
    try:
        query = request.args.get('q', '').strip()
        
        if not query:
            return jsonify({'error': 'Query parameter "q" is required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Search with LIKE pattern
        cursor.execute(
            'SELECT id, username, contact, created_at FROM contacts WHERE username LIKE ? ORDER BY username ASC',
            (f'%{query}%',)
        )
        contacts = cursor.fetchall()
        conn.close()
        
        result = []
        for contact in contacts:
            result.append({
                'id': contact['id'],
                'username': contact['username'],
                'contact': contact['contact'],
                'created_at': contact['created_at']
            })
        
        return jsonify({
            'query': query,
            'found': len(result),
            'contacts': result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/contacts/paginated', methods=['GET'])
def get_paginated_contacts():
    """Get contacts with pagination"""
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 5))
        
        if page < 1 or limit < 1:
            return jsonify({'error': 'Page and limit must be positive integers'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get total count
        cursor.execute('SELECT COUNT(*) as count FROM contacts')
        total = cursor.fetchone()['count']
        
        # Get paginated results
        offset = (page - 1) * limit
        cursor.execute(
            'SELECT id, username, contact, created_at FROM contacts ORDER BY created_at DESC LIMIT ? OFFSET ?',
            (limit, offset)
        )
        contacts = cursor.fetchall()
        conn.close()
        
        result = []
        for contact in contacts:
            result.append({
                'id': contact['id'],
                'username': contact['username'],
                'contact': contact['contact'],
                'created_at': contact['created_at']
            })
        
        total_pages = (total + limit - 1) // limit
        
        return jsonify({
            'page': page,
            'limit': limit,
            'total_contacts': total,
            'total_pages': total_pages,
            'contacts': result
        }), 200
    except ValueError:
        return jsonify({'error': 'Invalid page or limit parameter'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/export', methods=['GET'])
def export_contacts():
    """Export all contacts as JSON"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, username, contact, created_at FROM contacts ORDER BY created_at DESC')
        contacts = cursor.fetchall()
        conn.close()
        
        result = []
        for contact in contacts:
            result.append({
                'id': contact['id'],
                'username': contact['username'],
                'contact': contact['contact'],
                'created_at': contact['created_at']
            })
        
        return jsonify({
            'export_date': datetime.now().isoformat(),
            'total_records': len(result),
            'contacts': result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/query/by-contact', methods=['GET'])
def query_by_contact():
    """Query contacts by contact number"""
    try:
        contact = request.args.get('c', '').strip()
        
        if not contact:
            return jsonify({'error': 'Contact parameter "c" is required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT id, username, contact, created_at FROM contacts WHERE contact LIKE ? ORDER BY username ASC',
            (f'%{contact}%',)
        )
        contacts = cursor.fetchall()
        conn.close()
        
        result = []
        for c in contacts:
            result.append({
                'id': c['id'],
                'username': c['username'],
                'contact': c['contact'],
                'created_at': c['created_at']
            })
        
        return jsonify({
            'search_contact': contact,
            'found': len(result),
            'contacts': result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/query/sorted', methods=['GET'])
def query_sorted():
    """Get all contacts sorted by parameter"""
    try:
        sort_by = request.args.get('sort', 'username').lower()
        order = request.args.get('order', 'asc').lower()
        
        if sort_by not in ['username', 'contact', 'created_at']:
            return jsonify({'error': 'sort must be: username, contact, or created_at'}), 400
        
        if order not in ['asc', 'desc']:
            return jsonify({'error': 'order must be: asc or desc'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = f'SELECT id, username, contact, created_at FROM contacts ORDER BY {sort_by} {order.upper()}'
        cursor.execute(query)
        contacts = cursor.fetchall()
        conn.close()
        
        result = []
        for contact in contacts:
            result.append({
                'id': contact['id'],
                'username': contact['username'],
                'contact': contact['contact'],
                'created_at': contact['created_at']
            })
        
        return jsonify({
            'sort_by': sort_by,
            'order': order,
            'total': len(result),
            'contacts': result
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)