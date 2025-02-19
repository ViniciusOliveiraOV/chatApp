# ChatApp - Real-Time Chat Application

This guide provides instructions to set up and run a real-time chat application with **FastAPI** for the backend and **React** for the frontend.

## Requirements

### On Linux (Arch/Ubuntu) and Windows:
- **Node.js** (version 14.x or higher)
- **npm** (Node package manager)
- **Python 3.8+**
- **PostgreSQL**
- **git**

### Install Dependencies

#### For Linux:
1. Ensure your system is up to date:

   ```bash
   sudo pacman -Syu  # For Arch Linux
   sudo apt update && sudo apt upgrade  # For Ubuntu

    Install the required tools:

    sudo pacman -S git python nodejs npm postgresql nginx  # For Arch Linux
    sudo apt install git python3 nodejs npm postgresql nginx  # For Ubuntu

For Windows:

    Install Node.js from here
    Install Python from here
    Install PostgreSQL from here
    Install git from here

1. Backend: FastAPI + WebSockets
Install and Set Up the Backend

    Clone the repository:

git clone https://github.com/yourusername/chatapp.git
cd chatapp

Set up a Python virtual environment:

python -m venv chat-env
source chat-env/bin/activate  # Linux
.\chat-env\Scripts\activate  # Windows

Install the required Python dependencies:

pip install -r backend/requirements.txt

Set up PostgreSQL:

    Install PostgreSQL if not already installed (refer to system-specific instructions above).

    Create the database and user for the app:

    sudo -u postgres psql
    CREATE DATABASE chat_app;
    CREATE USER chat_user WITH PASSWORD 'your_password';
    GRANT ALL PRIVILEGES ON DATABASE chat_app TO chat_user;
    \q

Run the backend server:

    uvicorn backend.main:app --reload

    The backend server will be running at http://localhost:8000.

2. Frontend: React + JavaScript
Install and Set Up the Frontend

    Navigate to the frontend directory:

cd chatapp/frontend

Install the frontend dependencies:

npm install

Set up the WebSocket connection to the backend:

    In src/App.js, update the WebSocket URL to ws://localhost:8000/ws/{username}, where {username} is the username you want to use.

Start the frontend server:

    npm start

    The frontend will be available at http://localhost:3000.

3. Connecting Backend and Frontend

Once both servers (backend and frontend) are running, open the frontend URL in your browser (http://localhost:3000).

    Enter a username.
    The frontend will connect to the backend WebSocket server running at http://localhost:8000/ws/{username}.
    You can now start sending and receiving messages in real-time.

4. Troubleshooting
Common Issues:

    PostgreSQL issues: Ensure that PostgreSQL is running. You can check its status with:

sudo systemctl status postgresql  # Linux

For Windows, use the PostgreSQL service manager to ensure it is running.

Backend not connecting to the database: Double-check your database credentials (chat_user and your_password) in the backend/main.py file to make sure they match what you set up in PostgreSQL.

Port conflicts: If either the backend or frontend server ports are occupied, change the port by specifying it explicitly:

    For backend:

uvicorn backend.main:app --reload --host 0.0.0.0 --port 8001

For frontend:

        PORT=4000 npm start  # Linux/Windows

Logs:

    Backend logs: Check your terminal for any errors when running uvicorn (backend).
    Frontend logs: Open the browser developer console (F12) to check for any issues in the React app.

License

This project is licensed under the MIT License - see the LICENSE file for details.


### Key Highlights:
1. **Setup for both Linux and Windows**: The instructions cover both platforms without replicating code.
2. **Backend setup with FastAPI**: Clear steps to get the backend up and running with PostgreSQL.
3. **Frontend setup with React**: Easy steps to install and run the React frontend.
4. **Database configuration**: Clear instructions to set up PostgreSQL.
5. **Troubleshooting section**: Practical tips for resolving common issues.

With these instructions, you'll be able to get the backend and frontend running on both Linux (including Arch) and Windows.