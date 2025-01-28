# European Basketball Statistics

<img src="logo.png" alt="Logo" width="100" />


This project is built on a relational database schema, utilizing advanced SQL query techniques and extensive preprocessing to adapt tables for various use cases. The backend and frontend work seamlessly together to present statistics to users in a visually appealing and interactive manner.

For more details about the project, including in-depth explanations and user interface designs, check out our [project report](./documentation/Report.pdf).

If you want to run the project on your local machine, follow the instructions below.

## Prerequisites

1. **MySQL (9.1 recomended)**: Ensure MySQL is installed on your machine. If not, download and install it from the [official website](https://www.mysql.com/).
2. **Node.js and npm**: Required for the frontend setup. Download and install them from the [official Node.js website](https://nodejs.org/).
3. **Python (3.12 recomended)**: Required for the backend setup. Download and install it from the [official Python website](https://www.python.org/).

---

## Setup Instructions

### 1. Database Setup

1. You can download the required CSV files from the following link: [Google Drive - CSV Files](https://drive.google.com/drive/folders/1bf3SSKFpJ-_Hd-Ut3kM-QVPX0uZqp-Az?usp=sharing).
Put these CSV files in the folder specified in the `table_initialization/load_tables.sql` file. If you are using a different version of MySQL, update the file paths in the SQL file accordingly.

2. Create a database in MySQL with the following command:

    ```sql
    CREATE DATABASE BASKETBALL;
    ```

3. Run the SQL scripts in the following order:

    - `backend/table_initialization/create_tables.sql`
    - `backend/table_initialization/load_tables.sql`
    - `backend/table_initialization/prepare_for_foreign_keys.sql`
    - `backend/table_initialization/foreign_keys.sql`

---

### 2. Backend Setup

1. Navigate to the `backend` directory:

    ```bash
    cd backend
    ```
2. Change `app/config.py`according to your mysql username and password.    

3. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Install the `waitress` server:

    ```bash
    pip install waitress
    ```

5. Start the backend server:

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
