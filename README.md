# Project README

Prerequisites
- Python 3.8+ and pip
- Node.js 16+ and npm

Start the server
1. Install Python deps:
   python -m pip install -r server/requirements.txt
2. Run server:
   uvicorn server.app.main:app --reload --host 0.0.0.0 --port 8000

Run the Node.js client
1. Change to client directory and install deps:
   cd client && npm install
2. Run the test client:
   npm run test-server

Notes
- Server exposes /health, /follow, /unfollow, /followers/{user_id}, /following/{user_id}
- Storage is in-memory; data resets on restart
- Use curl or the client to exercise the API
