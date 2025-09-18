from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# The backend API server URL
API_SERVER_URL = "http://localhost:5000"

@app.route('/')
def index():
    """Home page that lists all menu items."""
    try:
        response = requests.get(f"{API_SERVER_URL}/menu-items")
        if response.status_code == 200:
            items = response.json()
            return render_template('index.html', items=items)
        else:
            return render_template('error.html', message="Failed to fetch menu from the server.")
    except requests.exceptions.ConnectionError:
        return render_template('error.html', message="Could not connect to the API server. Make sure it's running on port 5000.")

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    """Page to add a new menu item."""
    if request.method == 'POST':
        form_data = {
            'name': request.form['name'],
            'price': request.form['price'],
            'category': request.form['category'],
            'description': request.form['description'],
            'image_url': request.form['imageUrl']
        }
        response = requests.post(f"{API_SERVER_URL}/menu-items", json=form_data)
        if response.status_code == 201:
            return redirect(url_for('index'))
        else:
            return render_template('error.html', message=f"Failed to add item: {response.json().get('error', 'Unknown error')}")
    
    return render_template('add_in_menu.html')

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    """Page  toedit an existing menu item."""
    if request.method == 'POST':
        form_data = {
            'name': request.form['name'],
            'price': request.form['price'],
            'category': request.form['category'],
            'description': request.form['description'],
            'image_url': request.form['imageUrl']
        }
        response = requests.put(f"{API_SERVER_URL}/menu-items/{item_id}", json=form_data)
        if response.status_code == 200:
            return redirect(url_for('index'))
        else:
            return render_template('error.html', message=f"Failed to update item: {response.json().get('error', 'Unknown error')}")

    # For GET request, fetch the item data to pre-fill the form
    try:
        response = requests.get(f"{API_SERVER_URL}/menu-items/{item_id}")
        if response.status_code == 200:
            item = response.json()
            return render_template('edit_the_menu.html', item=item)
        else:
            return render_template('error.html', message="Menu item not found.")
    except requests.exceptions.ConnectionError:
        return render_template('error.html', message="Could not connect to the API server.")

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    """Deletes a menu item and redirects to the index."""
    try:
        response = requests.delete(f"{API_SERVER_URL}/menu-items/{item_id}")
        if response.status_code != 200:
            return render_template('error.html', message=f"Failed to delete item: {response.json().get('error', 'Unknown error')}")
    except requests.exceptions.ConnectionError:
        return render_template('error.html', message="Could not connect to the API server.")
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    # This client server runs on port 5050
    app.run(debug=True, port=5050)
