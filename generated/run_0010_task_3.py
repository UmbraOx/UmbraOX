from flask import Flask, render_template_string
import logging

app = Flask(__name__)

# Sample data for demonstration purposes
data = [
    {"id": 1, "name": "Alice", "age": 30},
    {"id": 2, "name": "Bob", "age": 25},
    {"id": 3, "name": "Charlie", "age": 35}
]

# HTML template for the dashboard
template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Dashboard</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>Dashboard</h1>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Age</th>
            </tr>
        </thead>
        <tbody>
            {% for item in data %}
            <tr>
                <td>{{ item.id }}</td>
                <td>{{ item.name }}</td>
                <td>{{ item.age }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """
    Renders the dashboard page with sample data.
    
    Returns:
        str: The rendered HTML content of the dashboard.
    """
    try:
        return render_template_string(template, data=data)
    except Exception as e:
        logging.error(f"An error occurred while rendering the dashboard: {e}")
        return "An error occurred. Please try again later.", 500

if __name__ == '__main__':
    app.run(debug=True)
