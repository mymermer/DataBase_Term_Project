'use client';

import React, { useEffect, useState } from 'react';
import StatPageTemplate from '../../../components/StatPageTemplate';
import DataTable from '../../../components/DataTable';
import styles from '../../../styles/PointsPage.module.css';


// game_point_id,game_player_id,game_play_id,game_id,game,round_of_game,phase,season_player_id,season_team_id,player,action_id,action_of_play,points,coord_x,coord_y,zone_of_play,minute,points_a,points_b,time_stamp


// Define columns first
const columns = [
  'game_point_id',
  'game_player_id',
  'game_play_id',
  'game_id',
  'game',
  'round_of_game',
  'phase',
  'season_player_id',
  'season_team_id',
  'player',
  'action_id',
  'action_of_play',
  'points',
  'coord_x',
  'coord_y',
  'zone_of_play',
  'minute',
  'points_a',
  'points_b',
  'time_stamp'
];

export default function PointsPage({ params }) {
  const { league } = React.use(params);

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  let tournament = (league === "euroleague") ? "lig" : "cup";  // Fetch data from the API
  const [rowsPerPage, setRowsPerPage] = useState(25); // Default 25 rows
  const [currentPage, setCurrentPage] = useState(0); // Default page 0
  const [totalRows, setTotalRows] = useState(0); // Total rows in the table
  
  const handlePageChange = (newPage) => {
    setCurrentPage(newPage); // Update current page
  };
  
  const handleRowsPerPageChange = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10)); // Update rows per page
    setCurrentPage(0); // Reset to first page
  };


  useEffect(() => {
    const fetchData = async () => {
      setLoading(true); // Start loading
      const offset = currentPage * rowsPerPage;
      const url = `http://127.0.0.1:5000/api/v1/${tournament}_points?offset=${offset}&limit=${rowsPerPage}`;
      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const result = await response.json();
        setData(result); // Update table data
        setLoading(false); // End loading
      } catch (error) {
        console.error('Error fetching data:', error);
        setError(error.message); // Update error state
        setLoading(false); // End loading even on error
      }
    };
    fetchData();
  }, [currentPage, rowsPerPage]);
  

  if (loading) return <p>Loading data...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <StatPageTemplate league={league} stat="Points">
      <div className={styles.pointsPageContent}>
        <h2>{league.charAt(0).toUpperCase() + league.slice(1)} Points Statistics</h2>
        <div className={styles.tableContainer}>
          <DataTable initialData={data} initialColumns={columns} currentPage= {currentPage} handlePageChange = {handlePageChange}   handleRowsPerPageChange = {handleRowsPerPageChange}/>
        </div>
      </div>
    </StatPageTemplate>
  );
}
