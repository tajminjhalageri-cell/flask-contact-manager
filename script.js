function addContact() {
    fetch('/add', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            username: document.getElementById('username').value,
            contact: document.getElementById('contact').value
        })
    })
    .then(res => res.json())
    .then(() => {
        document.getElementById('output').innerText = "Contact added successfully";
    });
}

function getContact() {
    let user = document.getElementById('username').value;
    fetch('/contact/' + user)
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            document.getElementById('output').innerText = "User not found";
        } else {
            document.getElementById('output').innerText =
                "Username: " + data.username + "\nContact: " + data.contact;
        }
    });
}

function deleteContact() {
    let user = document.getElementById('username').value;
    fetch('/delete/' + user, {method: 'DELETE'})
    .then(res => res.json())
    .then(() => {
        document.getElementById('output').innerText = "Contact deleted successfully";
    });
}

function getAll() {
    fetch('/contacts')
    .then(res => res.json())
    .then(data => {
        let result = "";
        data.forEach(c => {
            result += "Username: " + c.username + " | Contact: " + c.contact + "\n";
        });
        document.getElementById('output').innerText = result;
    });
}