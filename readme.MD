# Temperature Monitoring API

This is a Python Flask API designed to monitor device temperature and store any data that could not be parsed correctly.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.6 or later.
- PostgreSQL

### Installing

1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/<your-username>/temperature-monitoring-api.git
   ```
2. Navigate into the project directory:
   ```bash
   cd temperature-monitoring-api
   ```

3. Set up a Python virtual environment (optional, but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate
   ```

4. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
5. Set up the PostgreSQL database. The database URL should be set in an environment variable named DB_URL.


6. Run the application:
   ```bash
   python app.py
   ```
   
### API Endpoints
- POST /temp: Process temperature data from devices.
- GET /errors: Retrieve all data that could not be parsed correctly.
- DELETE /errors: Delete all error data.

### Authors 
- **Alexander Shumonov** - [Shumonov](https://github.com/Shumonov)