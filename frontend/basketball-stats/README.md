come to directory of basketball-stats

npm install

npm run dev

for production:
npm run build




****************************HANDILING ERROR****************************
At first put "const [error, setError] = useState(null); " if you didn't put to your file that needs error hadiling.

Thoes error hadiling places are where you fetch data via sending requests to database (just look places that have api calls)
put "setError(error.message);" to their catch statment.


Then we need to put the error box. Determine file that you need to put error to. DataTable already puts. If you need to put to another file, put this code to the file that you need to put error to:
    {error && <ErrorDisplay message={error} onRetry={onFetchData} />}

you need to put ErrorDisplay to your path as:
    import ErrorDisplay from 'place_of_error_display/ErrorDisplay';

"onFetchData" is const variable that you are saving your request to. Just put your the varaible at the beggining of your api's call

If you need to handle error from other files, please also add them as paramter you are sending. like:
<DataTable error={error} />



****************************HANDILING LOADING****************************
    in same manner
    import LoadingSkeleton from 'wherelaodingskeletonis/LoadingSkeleton';

    const [loading, setLoading] = useState(false);

    setLoading(true); //to start loading
    setLoading(false); //to stop loading


    {  loading &&  <LoadingSkeleton rows={5} columns={3} /> }

