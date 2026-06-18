import subprocess

def install_dashboard_dependencies():
    """
    Install necessary software and dependencies for the dashboard.
    
    This function uses pip to install Python packages required for a typical web dashboard.
    It includes packages like Flask, Dash, Pandas, and Plotly which are commonly used
    in building interactive web dashboards.
    
    Raises:
        subprocess.CalledProcessError: If any of the installation commands fail.
    """
    try:
        # Install Flask, a lightweight WSGI web application framework
        subprocess.run(['pip', 'install', 'flask'], check=True)
        
        # Install Dash by Plotly for building analytical web applications
        subprocess.run(['pip', 'install', 'dash'], check=True)
        
        # Install Pandas for data manipulation and analysis
        subprocess.run(['pip', 'install', 'pandas'], check=True)
        
        # Install Plotly for interactive graphing
        subprocess.run(['pip', 'install', 'plotly'], check=True)
        
        print("All necessary software and dependencies have been installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while installing dependencies: {e}")

if __name__ == "__main__":
    install_dashboard_dependencies()
