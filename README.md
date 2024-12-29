# KickStats Term Project

Welcome to the KickStats Term Project! Follow the instructions below to set up and run the project on your local machine.

---

## Prerequisites

1. **MySQL**: Ensure MySQL is installed on your machine. If not, download and install it from the [official website](https://www.mysql.com/).
2. **Node.js and npm**: Required for the frontend setup. Download and install them from the [official Node.js website](https://nodejs.org/).

---

## Setup Instructions

### 1. Database Setup

1. Place the CSV files in the folder specified in the `table_initialization/load_tables.sql` file. If you are using a different version of MySQL, update the file paths in the SQL file accordingly.

2. Create a database in MySQL with the following command:

    ```sql
    CREATE DATABASE BASKETBALL;
    ```

3. Run the SQL scripts in the following order:

    - `table_initialization/create_tables.sql`
    - `table_initialization/load_tables.sql`
    - `table_initialization/prepare_for_foreign_keys.sql`
    - `table_initialization/add_foreign_keys.sql`

---

### 2. Backend Setup

1. Navigate to the `backend` directory:

    ```bash
    cd backend
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Install the `waitress` server:

    ```bash
    pip install waitress
    ```

4. Start the backend server:

    ```bash
    waitress-serve --port=5000 run:app
    ```

---

### 3. Frontend Setup

1. Open a new terminal and navigate to the `frontend/basketball-stats` directory:

    ```bash
    cd frontend/basketball-stats
    ```

2. Install the required npm packages:

    ```bash
    npm install
    ```

3. Build the frontend:

    ```bash
    npm run build
    ```

4. Start the frontend in release mode:

    ```bash
    npm run start
    ```

---

With these steps completed, both the backend and frontend should be running, and the project will be fully operational!
