"""
This script sets up a basic Flask application to serve a styled dashboard.
The dashboard is styled using inline CSS to ensure it is visually appealing and user-friendly.
"""

from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def dashboard():
    """
    Renders the dashboard HTML template with embedded CSS.
    """
    try:
        # HTML content with embedded CSS
        html_content = '''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Styled Dashboard</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f9;
                        margin: 0;
                        padding: 20px;
                    }
                    .container {
                        max-width: 800px;
                        margin: auto;
                        background-color: #fff;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                        border-radius: 8px;
                        padding: 20px;
                    }
                    h1 {
                        color: #333;
                        text-align: center;
                    }
                    .card {
                        background-color: #e9ecef;
                        border-radius: 6px;
                        padding: 15px;
                        margin-bottom: 15px;
                        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                    }
                    .card h2 {
                        color: #383d40;
                        margin-top: 0;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Welcome to the Styled Dashboard</h1>
                    <div class="card">
                        <h2>Card Title 1</h2>
                        <p>This is a sample card content.</p>
                    </div>
                    <div class="card">
                        <h2>Card Title 2</h2>
                        <p>This is another sample card content.</p>
                    </div>
                </div>
            </body>
            </html>
        '''
        
        return render_template_string(html_content)
    except Exception as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)
