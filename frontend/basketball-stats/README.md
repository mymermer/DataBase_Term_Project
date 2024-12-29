# basketball-stats

This document outlines the project setup, development, and error/loading handling for the basketball-stats frontend application.

## Getting Started

1. **Navigate to the project directory:**

   cd basketball-stats

2. **Install dependencies:**

   npm install

3. **Run in development mode:**

   npm run dev

4. **Build for production:**

   npm run build

## Error Handling

**1. State Management:**

- Add the following to files requiring error handling:

   const [error, setError] = useState(null);

**2. Error Handling in API Calls:**

- In API call `catch` blocks:

   setError(error.message);

**3. Displaying Errors:**

- Determine the component to display the error in.
- Add the following to the desired component:

   {
       error && <ErrorDisplay message={error} onRetry={onFetchData} />;
   }

- Import `ErrorDisplay`:

   import ErrorDisplay from 'place_of_error_display/ErrorDisplay';

- Pass `error` to components that need to display it (e.g., `DataTable`):

   <DataTable error={error} />

**4. Centralized Error Handling (Example):**

try {
    // Your API call logic
} catch (error) {
    if (error.message.includes("404")) {
        setError("No data found for the selected criteria. Please refine your search.");
    } else if (error.message.includes("Failed to fetch")) {
        setError("Unable to load data. Please check your network connection or try again later.");
    } else {
        setError("An unexpected error occurred. Please contact support.");
    }
    console.error("Error message:", error.message);
    throw error;
}

**Note:** Update `setLoading(false)` as needed based on your implementation.

## Loading Handling

**1. State Management:**

- Add the following to components requiring loading indicators:

   const [loading, setLoading] = useState(false);

**2. Loading Indicator:**

- Import `LoadingSkeleton`:

   import LoadingSkeleton from 'wherelaodingskeletonis/LoadingSkeleton';

- Display the loading indicator:

   { loading && <LoadingSkeleton rows={5} columns={3} /> }

**3. Toggle Loading State:**

- `setLoading(true)` to start loading.
- `setLoading(false)` to stop loading.

## Constraints Handling (Pickers)

- For `DateTime`, `Date`, and `Time` columns:
    - Set the `columnTypes` property in `page.js` to the respective value ("date_time", "date", or "time").
    - The picker will be implemented automatically.

This document provides a basic framework for error and loading handling in the basketball-stats application. Adapt it to your specific needs and project structure.