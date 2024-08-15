# Email Collector App

This is an Email Collector application built with Flask for the backend and React for the frontend. The app allows users to search for emails based on specific keywords.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- **Python 3.x**: [Download Python](https://www.python.org/downloads/)
- **Node.js and npm**: [Download Node.js](https://nodejs.org/)


## Installation

### Clone the repository

```bash
git clone <https://github.com/KumuthuA/email-collector.git>
cd email-collector
```

### Backend (Flask)

1. Open a command prompt and navigate to the `server` directory:

   ```bash
   cd server
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```


### Frontend (React)

1. Open another command prompt and navigate to the `client` directory:

   ```bash
   cd client
   npm i
   ```


## Running the Application

1. **Open two command prompts or terminal windows**.

2. **Start the Flask backend**:

    In the first terminal window, navigate to the `server` directory and run the Flask server:

    ```bash
    cd server
    python server.py
    ```

3. **Start the React frontend**:

    In the second terminal window, navigate to the `client` directory and start the React development server:

    ```bash
    cd client
    npm start
    ```

4. **Access the application**:

    The frontend should automatically open in your default web browser at `http://localhost:3000`. If not, open your browser and go to that address manually.


## Project Structure

```
├── client/              # React frontend
├── server/              # Flask backend
│   ├── venv/            
│   ├── server.py        
│   ├── requirements.txt 
└── README.md            # Project README
```

## Usage

1. Open the application in your web browser at `http://localhost:3000`.
2. Enter a keyword in the search bar to fetch related emails.
3. The results will be downloaded as a csv. This will take a while.