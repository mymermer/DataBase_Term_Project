## Database Initialization

### Steps to Setup the Database
1. **Start MySQL**:
   - Run the SQL files in the following order:
     - `create.sql`
     - `load.sql`
     - `prepare.sql`
     - `foreign_keys.sql`

   ⚠️ **Important**:
   - Ensure you have the latest version of the required CSV files, typically were shared via WhatsApp.

2. **Troubleshooting Database Reset**:
   - If you encounter issues re-running the files, use the following commands to reset your database:

   ```sql
   -- Disable foreign key checks and drop the existing database
   DROP DATABASE basketball;

   -- Recreate the database
   CREATE DATABASE basketball;

   -- Navigate to the directory containing initialization scripts and execute each file
   SOURCE create_tables.sql;


- **CSV File Access**:
   - The SQL scripts do not have access to CSV files outside the specified directory. Ensure the directory is correctly set up, and update version names if necessary.

- **Configuration Updates**:
   - Modify the `app/config.py` file to reflect your database credentials. Example configuration:
     ```python
     class Config:
         DB_HOST = "127.0.0.1"
         DB_PORT = 3306
         DB_USER = "root"
         DB_PASSWORD = "yourpassword"
         DB_NAME = "basketball"
         DEBUG = True
     ```
   - This file will eventually be removed from the repository and `.gitignore`d as configurations will differ for each user.

## Running the Application

1. **Start the Backend**:
   - Run the `run.py` script to initialize the backend server.

2. **API Interaction Using Postman**:
   - Download the Postman app for testing.
   - Open a new request to interact with the backend.
   - For `update` and `create` operations, fill the request body in JSON format.

## Development Tasks (TODOs)

1. **Create Route Files**:
   - Organize the routes into separate files for better modularity.

2. **Update Model Functions**:
   - Modify the `update` and `create` functions in the model files to handle `NULL` values gracefully.

3. **Blueprint Registration**:
   - Register blueprints in `__init__.py` to connect route files to the main application.

4. **Ignore Directory-Specific SQL Files**:
   - Add `load_tables.sql` to `.gitignore` to avoid pushing files with directory-specific configurations.
