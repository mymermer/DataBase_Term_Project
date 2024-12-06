'use client';

import React, { useEffect, useState } from 'react';
import StatPageTemplate from '../../../components/StatPageTemplate';
import DataTable from '../../../components/DataTable';
import styles from '../../../styles/PointsPage.module.css';

const allColumns = [
  'game_point_id', 'game_player_id', 'game_play_id', 'game_id', 'game',
  'round_of_game', 'phase', 'season_player_id', 'season_team_id', 'player',
  'action_id', 'action_of_play', 'points', 'coord_x', 'coord_y',
  'zone_of_play', 'minute', 'points_a', 'points_b', 'date_time_stp'
];

export default function PointsPage({ params }) {
  const { league } = React.use(params);

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [rowsPerPage, setRowsPerPage] = useState(25);
  const [currentPage, setCurrentPage] = useState(0);
  const [totalRows, setTotalRows] = useState(0);
  const [selectedColumns, setSelectedColumns] = useState(allColumns.slice(0, 10));
  
  const tournament = league === "euroleague" ? "lig" : "cup";

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      const offset = currentPage * rowsPerPage;
      const columnsParam = selectedColumns.join(',');
      const dataUrl = `http://127.0.0.1:5000/api/v1/${tournament}_points?offset=${offset}&limit=${rowsPerPage}&columns=${columnsParam}`;
      const countUrl = `http://127.0.0.1:5000/api/v1/${tournament}_points/count`;
      
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
  }, [currentPage, rowsPerPage, tournament, selectedColumns]);

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

  if (error) return <p>Error: {error}</p>;

  return (
    <StatPageTemplate league={league} stat="Points">
      <div className={styles.pointsPageContent}>
        <h2>{league.charAt(0).toUpperCase() + league.slice(1)} Points Statistics</h2>
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
            isLoading={loading}
          />
        </div>
      </div>
    </StatPageTemplate>
  );
}

