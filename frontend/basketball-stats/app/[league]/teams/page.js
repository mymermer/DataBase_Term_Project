'use client';

import React, { useEffect, useState } from 'react';
import StatPageTemplate from '../../../components/StatPageTemplate';
import DataTable from '../../../components/DataTable';
import styles from '../../../styles/TeamsPage.module.css';


const allColumns = [
  'season_team_id',
  'games_played',
  'minutes_played',
  'points',
  'two_points_made',
  'two_points_attempted',
  'three_points_made',
  'three_points_attempted',
  'free_throws_made',
  'free_throws_attempted',
  'offensive_rebounds',
  'defensive_rebounds',
  'total_rebounds',
  'assists',
  'steals',
  'turnovers',
  'blocks_favour',
  'blocks_against',
  'fouls_committed',
  'fouls_received',
  'valuation',
  'minutes_per_game',
  'points_per_game',
  'two_points_made_per_game',
  'two_points_attempted_per_game',
  'two_points_percentage',
  'three_points_made_per_game',
  'three_points_attempted_per_game',
  'three_points_percentage',
  'free_throws_made_per_game',
  'free_throws_attempted_per_game',
  'free_throws_percentage',
  'offensive_rebounds_per_game',
  'defensive_rebounds_per_game',
  'total_rebounds_per_game',
  'assists_per_game',
  'steals_per_game',
  'turnovers_per_game',
  'blocks_favour_per_game',
  'blocks_against_per_game',
  'fouls_committed_per_game',
  'fouls_received_per_game',
  'valuation_per_game'

];

export default function TeamsPage({ params }) {
  const { league } = React.use(params);

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [rowsPerPage, setRowsPerPage] = useState(25);
  const [currentPage, setCurrentPage] = useState(0);
  const [totalRows, setTotalRows] = useState(0);
  const [selectedColumns, setSelectedColumns] = useState(allColumns.slice(0, 10));
  const [filters, setFilters] = useState({});
  
  const tournament = league === "euroleague" ? "lig" : "cup";

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      const offset = currentPage * rowsPerPage;
      const columnsParam = selectedColumns.join(',');
      let dataUrl = `http://127.0.0.1:5000/api/v1/${tournament}_teams?offset=${offset}&limit=${rowsPerPage}&columns=${columnsParam}`;
    
      // Add filters to the URL
      if (Object.keys(filters).length > 0) {
        const filterParams = Object.entries(filters)
          .map(([column, values]) => values.map(value => `${column}:${value}`))
          .flat()
          .join(',');
        dataUrl += `&filters=${filterParams}`;
      }
    
      const countUrl = `http://127.0.0.1:5000/api/v1/${tournament}_teams/count`;
    
      try {
        const [dataResponse, countResponse] = await Promise.all([
          fetch(dataUrl),
          fetch(countUrl)
        ]);

        if (!dataResponse.ok || !countResponse.ok) {
          throw new Error(`HTTP error! status: ${dataResponse.status} or ${countResponse.status}`);
        }

        const [result, countResult] = await Promise.all([
          dataResponse.json(),
          countResponse.json()
        ]);

        console.log('Count result:', countResult);
        console.log('Total rows:', countResult.count);

        setData(result);
        setTotalRows(countResult.count);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching data:', error);
        setError(error.message);
        setLoading(false);
      }
    };

    fetchData();
  }, [currentPage, rowsPerPage, tournament, selectedColumns, filters]);

  const handlePageChange = (newPage) => {
    setCurrentPage(newPage);
  };

  const handleRowsPerPageChange = (newRowsPerPage) => {
    setRowsPerPage(newRowsPerPage);
    setCurrentPage(0);
  };

  const handleColumnChange = (newColumns) => {
    setSelectedColumns(newColumns);
  };

  const handleFilterChange = (newFilters) => {
    setFilters(newFilters);
    setCurrentPage(0); // Reset to first page when filters change
  };

  if (error) return <p>Error: {error}</p>;

  return (
    <StatPageTemplate league={league} stat="Teams">
      <div className={styles.teamsPageContent}>
        <h2>{league.charAt(0).toUpperCase() + league.slice(1)} Teams Statistics</h2>
        <div className={styles.tableContainer}>
          <DataTable 
            initialData={data} 
            initialColumns={selectedColumns}
            allColumns={allColumns}
            currentPage={currentPage}
            rowsPerPage={rowsPerPage}
            totalRows={totalRows}
            onPageChange={handlePageChange}
            onRowsPerPageChange={handleRowsPerPageChange}
            onColumnChange={handleColumnChange}
            onFilterChange={handleFilterChange}
            isLoading={loading}
          />
        </div>
      </div>
    </StatPageTemplate>
  );
}

