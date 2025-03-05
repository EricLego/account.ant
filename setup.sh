#!/bin/bash

# Setup script for the accounting application
echo "Setting up accounting application with virtual environment..."

# Check if python3-venv is installed
if ! dpkg -l | grep -q python3-venv; then
    echo "python3-venv not found. Installing..."
    sudo apt update
    sudo apt install -y python3-venv python3-full
fi

# Create a virtual environment
echo "Creating a virtual environment..."
python3 -m venv venv

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Check for ODBC driver
echo "Checking for SQL Server ODBC driver..."
python -c "import pyodbc; print('Available ODBC drivers:'); [print(f'  - {d}') for d in pyodbc.drivers()]; sql_drivers = [d for d in pyodbc.drivers() if 'SQL Server' in d]; print(f'\nSQL Server drivers found: {len(sql_drivers)}'); [print(f'  - {d}') for d in sql_drivers]"

# Check if there are any SQL Server drivers
if [ $? -ne 0 ] || ! python -c "import pyodbc; exit(0 if any('SQL Server' in d for d in pyodbc.drivers()) else 1)"; then
    echo -e "\nWARNING: No SQL Server ODBC driver found!"
    echo "Please install SQL Server ODBC driver:"
    echo ""
    echo "For Ubuntu/Debian:"
    echo "  sudo apt-get update"
    echo "  sudo apt-get install unixodbc-dev"
    echo "  sudo apt-get install msodbcsql17"
    echo ""
    echo "You might also need to add Microsoft's repository first:"
    echo "  sudo su"
    echo "  curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -"
    echo "  curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list > /etc/apt/sources.list.d/mssql-release.list"
    echo "  exit"
    echo "  sudo apt-get update"
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env << EOL
# Environment variables for the application
SECRET_KEY=your-secret-key-here
# SQL Server connection (already configured in code, but can be moved here)
# DATABASE_CONNECTION=Server=tcp:account-ant.database.windows.net,1433;Initial Catalog=account-ant-employee;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;Authentication=SqlPassword;UID=workerAnt;PWD=forTheColony01!!
EOL
    echo ".env file created. Make sure to update the values."
else
    echo ".env file already exists."
fi

echo -e "\nSetup completed!"
echo -e "\nTo run the application:"
echo "  source venv/bin/activate  # Activate the virtual environment"
echo "  python main.py            # Run the Flask application"

echo -e "\nTo deactivate the virtual environment when done:"
echo "  deactivate"