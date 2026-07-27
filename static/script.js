function addContact() {
    const username = document.getElementById('username').value.trim();
    const contact = document.getElementById('contact').value.trim();
    
    if (!username || !contact) {
        document.getElementById('output').innerText = "Error: Please fill in all fields";
        return;
    }
    
    fetch('/add', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            username: username,
            contact: contact
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            document.getElementById('output').innerText = "Error: " + data.error;
        } else {
            document.getElementById('output').innerText = "✓ Contact added successfully";
            document.getElementById('username').value = '';
            document.getElementById('contact').value = '';
        }
    })
    .catch(err => {
        document.getElementById('output').innerText = "Error: " + err.message;
    });
}

function getContact() {
    let user = document.getElementById('username').value.trim();
    
    if (!user) {
        document.getElementById('output').innerText = "Error: Please enter a username";
        return;
    }
    
    fetch('/contact/' + encodeURIComponent(user))
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            document.getElementById('output').innerText = "✗ User not found";
        } else {
            document.getElementById('output').innerText =
                "Username: " + data.username + "\nContact: " + data.contact;
        }
    })
    .catch(err => {
        document.getElementById('output').innerText = "Error: " + err.message;
    });
}

function deleteContact() {
    let user = document.getElementById('username').value.trim();
    
    if (!user) {
        document.getElementById('output').innerText = "Error: Please enter a username";
        return;
    }
    
    if (!confirm('Are you sure you want to delete ' + user + '?')) {
        return;
    }
    
    fetch('/delete/' + encodeURIComponent(user), {method: 'DELETE'})
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            document.getElementById('output').innerText = "✗ " + data.error;
        } else {
            document.getElementById('output').innerText = "✓ Contact deleted successfully";
            document.getElementById('username').value = '';
            document.getElementById('contact').value = '';
        }
    })
    .catch(err => {
        document.getElementById('output').innerText = "Error: " + err.message;
    });
}

function getAll() {
    fetch('/contacts')
    .then(res => res.json())
    .then(data => {
        if (!data || data.length === 0) {
            document.getElementById('output').innerText = "No contacts found";
            return;
        }
        let result = "=== ALL CONTACTS ===\n\n";
        data.forEach((c, index) => {
            result += (index + 1) + ". Username: " + c.username + "\n   Contact: " + c.contact + "\n\n";
        });
        document.getElementById('output').innerText = result;
    })
    .catch(err => {
        document.getElementById('output').innerText = "Error: " + err.message;
    });
}
