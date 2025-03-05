"""
Setup script to ensure all prerequisites are set up for the application.
"""
import os
import subprocess
import sys

def check_pyodbc_driver():
    """Check if the ODBC driver for SQL Server is installed."""
    try:
        import pyodbc
        drivers = pyodbc.drivers()
        print("Available ODBC drivers:")
        for driver in drivers:
            print(f"  - {driver}")
        
        # Check for SQL Server driver
        sql_server_drivers = [d for d in drivers if 'SQL Server' in d]
        if not sql_server_drivers:
            print("\nWARNING: No SQL Server ODBC driver found!")
            print("Please install SQL Server ODBC driver:\n")
            if sys.platform == 'linux':
                print("For Ubuntu/Debian:")
                print("  sudo apt-get update")
                print("  sudo apt-get install unixodbc-dev")
                print("  sudo apt-get install msodbcsql17")
            elif sys.platform == 'darwin':
                print("For macOS:")
                print("  brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release")
                print("  brew update")
                print("  brew install msodbcsql17 mssql-tools")
            elif sys.platform == 'win32':
                print("For Windows:")
                print("  Download and install the Microsoft ODBC Driver for SQL Server from:")
                print("  https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server")
            return False
        else:
            print(f"\nSQL Server ODBC driver found: {sql_server_drivers[0]}")
            return True
    except ImportError:
        print("pyodbc is not installed. Installing requirements first...")
        return False

def install_requirements():
    """Install required Python packages."""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist."""
    if not os.path.exists('.env'):
        print("Creating .env file...")
        with open('.env', 'w') as f:
            f.write("# Environment variables for the application\n")
            f.write("SECRET_KEY=your-secret-key-here\n")
            f.write("# SQL Server connection (already configured in code, but can be moved here)\n")
            f.write("# DATABASE_CONNECTION=Server=tcp:account-ant.database.windows.net,1433;Initial Catalog=account-ant-employee;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;Authentication=SqlPassword;UID=workerAnt;PWD=forTheColony01!!\n")
        print(".env file created. Make sure to update the values.")
        return True
    else:
        print(".env file already exists.")
        return True

def main():
    """Run all setup steps."""
    print("Setting up accounting application...")
    
    # Install requirements
    if not install_requirements():
        print("Failed to install requirements. Setup aborted.")
        return False
    
    # Check ODBC driver
    if not check_pyodbc_driver():
        print("SQL Server ODBC driver not found. Please install it manually.")
        print("Setup will continue, but the application might not work properly.")
    
    # Create .env file
    if not create_env_file():
        print("Failed to create .env file. Setup aborted.")
        return False
    
    print("\nSetup completed successfully!")
    print("\nTo run the application:")
    print("  python main.py")
    
    return True

if __name__ == "__main__":
    main()