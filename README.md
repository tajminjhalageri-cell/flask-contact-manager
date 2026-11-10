# flask-contact-manager

Flask Contact Management REST API built with SQLite database and CSV migration support.

## 🚀 Features

* Add, view, update, and delete contacts seamlessly.
* REST API built using Python and Flask.
* SQLite database (`contacts.db`) for secure and local data storage.
* CSV migration support (`Book1.csv`) for easy data import/export.
* Clean and responsive HTML/CSS user interface.

## 🛠️ Technologies Used

* **Language:** Python
* **Framework:** Flask
* **Database:** SQLite
* **Frontend:** HTML, CSS, JavaScript
* **Data Handling:** CSV

## 📂 Project Structure
```text
flask-contact-manager/

│
├── static/               # CSS and frontend static assets
│   └── style.css
│
├── templates/             # HTML templates for UI
│   └── index.html
│
├── app.py                  # Main Flask application file
├── query_handler.py        # Database and query execution logic
├── contacts.db             # SQLite database file
├── Book1.csv               # Sample CSV data for migration
├── .migration_done        # Migration tracking file
├── .gitignore              # Git ignore configuration
├── .gitattributes         # Git attributes configuration
├── requirements.txt        # Python dependencies
├── QUERIES.md              # SQL queries documentation
├── SQL_USER_INPUT_SUMMARY.md # SQL input security summary
├── USER_INPUT_GUIDE.md    # User input handling guide
└── LICENSE                # MIT License file
```
## ⚙️ How to Run

Follow these steps to run the project locally on your machine:

1. **Clone the repository:**
 1. **Clone the repository:**
    
   git clone [https://github.com/tajminhalageri-cell/flask-contact-manager.git](https://github.com/tajminhalageri-cell/flask-contact-manager.git)
   cd flask-contact-manager
2. **Install dependencies:**
   pip install -r requirements.txt
3. **Run the applicaation:**

   python app.py
4. Open your web browser and go to http://127.0.0.1:5000/
   

<img width="499" height="544" alt="Screenshot 2026-07-30 132916" src="https://github.com/user-attachments/assets/997d69fb-a07e-4e30-9f27-01b11975fd15" />
