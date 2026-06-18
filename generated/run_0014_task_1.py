import os

def generate_dashboard_html(output_file):
    """
    Generates an HTML file with a basic dashboard structure.

    Args:
        output_file (str): The path where the HTML file will be saved.
    """
    try:
        # Define the HTML content for the dashboard
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            background-color: #f4f4f9;
        }}
        .dashboard {{
            width: 80%;
            max-width: 1200px;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            background-color: #fff;
        }}
        .header {{
            text-align: center;
            margin-bottom: 20px;
        }}
        .content {{
            display: flex;
            justify-content: space-around;
            align-items: start;
            gap: 20px;
        }}
        .card {{
            background-color: #e9ecef;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
    </style>
</head>
<body>

<div class="dashboard">
    <div class="header">
        <h1>Welcome to the Dashboard</h1>
    </div>
    <div class="content">
        <div class="card">
            <h2>Card 1</h2>
            <p>This is the first card.</p>
        </div>
        <div class="card">
            <h2>Card 2</h2>
            <p>This is the second card.</p>
        </div>
        <div class="card">
            <h2>Card 3</h2>
            <p>This is the third card.</p>
        </div>
    </div>
</div>

</body>
</html>
"""

        # Write the HTML content to a file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(html_content)

        print(f"Dashboard HTML generated successfully at {output_file}")

    except IOError as e:
        print(f"An error occurred while writing the HTML file: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Define the output file path
    output_file = "dashboard.html"

    # Generate the dashboard HTML
    generate_dashboard_html(output_file)
