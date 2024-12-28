'use client';

import React, { useEffect, useState } from 'react';
import StatPageTemplate from '../../../components/StatPageTemplate';
import DataTable from '../../../components/DataTable';
import TeamsUserView from '../../../components/TeamsUserView';
import styles from '../../../styles/Page.module.css';


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

const foreignKeyColumns = [];
const primaryKey = 'season_team_id';
const columnTypes = {
  season_team_id: 'season_team_id',
  games_played: 'integer',
  minutes_played: 'integer',
  points: 'integer',
  two_points_made: 'integer',
  two_points_attempted: 'integer',
  three_points_made: 'integer',
  three_points_attempted: 'integer',
  free_throws_made: 'integer',
  free_throws_attempted: 'integer',
  offensive_rebounds: 'integer',
  defensive_rebounds: 'integer',
  total_rebounds: 'integer',
  assists: 'integer',
  steals: 'integer',
  turnovers: 'integer',
  blocks_favour: 'integer',
  blocks_against: 'integer',
  fouls_committed: 'integer',
  fouls_received: 'integer',
  valuation: 'integer',
  minutes_per_game: 'float',
  points_per_game: 'float',
  two_points_made_per_game: 'float',
  two_points_attempted_per_game: 'float',
  two_points_percentage: 'float',
  three_points_made_per_game: 'float',
  three_points_attempted_per_game: 'float',
  three_points_percentage: 'float',
  free_throws_made_per_game: 'float',
  free_throws_attempted_per_game: 'float',
  free_throws_percentage: 'float',
  offensive_rebounds_per_game: 'float',
  defensive_rebounds_per_game: 'float',
  total_rebounds_per_game: 'float',
  assists_per_game: 'float',
  steals_per_game: 'float',
  turnovers_per_game: 'float',
  blocks_favour_per_game: 'float',
  blocks_against_per_game: 'float',
  fouls_committed_per_game: 'float',
  fouls_received_per_game: 'float',
  valuation_per_game: 'float'
};

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
  const [sortBy, setSortBy] = useState(null);
  const [sortOrder, setSortOrder] = useState('asc');
  
  const tournament = league === "euroleague" ? "lig" : "cup";

  useEffect(() => {
    fetchData();
  }, [currentPage, rowsPerPage, tournament, selectedColumns, filters, sortBy, sortOrder]);

  const fetchData = async () => {
    setLoading(true);
    setError(null); // Added to clear previous errors
    const offset = currentPage * rowsPerPage;
    const columnsParam = selectedColumns.join(',');
    let dataUrl = `http://127.0.0.1:5000/api/v1/${tournament}_teams?offset=${offset}&limit=${rowsPerPage}&columns=${columnsParam}`;
    if (sortBy) {
      dataUrl += `&sortBy=${sortBy}&order=${sortOrder}`;
    }
    let countUrl = `http://127.0.0.1:5000/api/v1/${tournament}_teams/count`;

    if (Object.keys(filters).length > 0) {
      const filterParams = Object.entries(filters)
        .map(([column, values]) => values.map(value => `${column}:${value}`))
        .flat()
        .join(',');
      dataUrl += `&filters=${filterParams}`;
      countUrl += `?filters=${filterParams}`;
    }
  
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

      setData(result);
      setTotalRows(countResult.total);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching data:', error);
      setError(error.message);
      setLoading(false);
    }
  };

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
    setCurrentPage(0);
  };

  const handleSort = (column) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(column);
      setSortOrder('asc');
    }
  };

  const handleAdd = async (newRowData) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/v1/${tournament}_teams`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newRowData),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      await fetchData();
      return true;
    } catch (error) {
      console.error('Error adding new row:', error);
      setError(error.message);
      throw error;
    }
  };

  const handleDelete = async (season_team_id) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/v1/${tournament}_teams/${season_team_id}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      await fetchData();
      return true;
    } catch (error) {
      console.error('Error deleting row:', error);
      setError(error.message);
      throw error;
    }
  };

  const handleUpdate = async (season_team_id, column, value) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/v1/${tournament}_teams/${season_team_id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ [column]: value }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      await fetchData();
      return true;
    } catch (error) {
      console.error('Error updating row:', error);
      throw error;
    }
  };

  return (
    <StatPageTemplate league={league} stat="Teams" UserView={TeamsUserView}>
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
            onSort={handleSort}
            sortBy={sortBy}
            sortOrder={sortOrder}
            onAdd={handleAdd}
            onDelete={handleDelete}
            onUpdate={handleUpdate}
            foreignKeyColumns={foreignKeyColumns}
            league={league}
            onFetchData={fetchData}
            error={error}
            primaryKey={primaryKey}
            columnTypes={columnTypes}
          />
        </div>
      </div>
    </StatPageTemplate>
  );
}

