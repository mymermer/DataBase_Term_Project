come to directory of basketball-stats

npm install

npm run dev

for production:
npm run build

************\*\*\*\*************HANDILING ERROR************\*\*\*\*************
At first put "const [error, setError] = useState(null); " if you didn't put to your file that needs error handling.

Those errors handling places are where you fetch data via sending requests to database (just look places that have api calls)
put "setError(error.message);" to their catch statement.

Then we need to put the error box. Determine file that you need to put error to. DataTable already puts. If you need to put to another file, put this code to the file that you need to put error to:

```javascript
{
  error && <ErrorDisplay message={error} onRetry={onFetchData} />;
}
```

you need to put ErrorDisplay to your path as:
import ErrorDisplay from 'place_of_error_display/ErrorDisplay';

"onFetchData" is const variable that you are saving your request to. Just put your the variable at the beginning of your api's call

If you need to handle error from other files, please also add them as parameter you are sending. like:
<DataTable error={error} />

Besides of your user view, you need to also send your errors to DataTable as well as parameter. DataTable will handle the rest.

You can use this block for catching errors inside your functions:

```javascript
    catch (error) {
      if (error.message.includes("404")) {
        setError(
          "No data found for the selected criteria. Please refine your search."
        );
      } else if (error.message.includes("Failed to fetch")) {
        setError(
          "Unable to load data. Please check your network connection or try again later."
        );
      } else {
        setError("An unexpected error occurred. Please contact support.");
      }
      console.error("Error message:", error.message);
      throw error;
    }
```

Note: Sometimes, you will need to setLoading(false); too (it depends on your implementation)

************\*\*\*\*************HANDILING LOADING************\*\*\*\*************
in same manner
import LoadingSkeleton from 'wherelaodingskeletonis/LoadingSkeleton';

    const [loading, setLoading] = useState(false);

    setLoading(true); //to start loading
    setLoading(false); //to stop loading


    {  loading &&  <LoadingSkeleton rows={5} columns={3} /> }
