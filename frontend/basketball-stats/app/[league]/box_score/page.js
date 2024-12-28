"use client";

import React, { useEffect, useState } from "react";
import StatPageTemplate from "../../../components/StatPageTemplate";
import DataTable from "../../../components/DataTable";
import styles from "../../../styles/Page.module.css";
import BoxScoreUserView from "../../../components/BoxScoreUserView";

const allColumns = [
  'game_player_id', 'game_id', 'game', 'round_of_game', 'phase', 'season_player_id', 'season_team_id',
  'is_starter', 'is_playing', 'dorsal', 'player', 'points',
  'two_points_made', 'two_points_attempted',
  'three_points_made', 'three_points_attempted',
  'free_throws_made', 'free_throws_attempted',
  'offensive_rebounds', 'defensive_rebounds', 'total_rebounds',
  'assists', 'steals', 'turnovers', 'blocks_favour', 'blocks_against',
  'fouls_committed', 'fouls_received', 'valuation'
];

const foreignKeyColumns = [
  "season_player_id",
  "game_id",
  "season_team_id",
];

const primaryKey = "game_player_id";
const columnTypes = {
  game_player_id: 'game_player_id',
  game_id: 'game_id',
  game: 'game',
  round_of_game: 'integer',
  phase: 'string',
  season_player_id: 'season_player_id',
  season_team_id: 'season_team_id',
  is_starter: 'boolean',
  is_playing: 'boolean',
  dorsal: 'integer',
  player: 'string',
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
  valuation: 'integer'
};


export default function BoxScorePage({ params }) {
  const { league } = React.use(params);

  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [rowsPerPage, setRowsPerPage] = useState(25);
  const [currentPage, setCurrentPage] = useState(0);
  const [totalRows, setTotalRows] = useState(0);
  const [selectedColumns, setSelectedColumns] = useState(
    allColumns.slice(0, 10)
  );
  const [filters, setFilters] = useState({});
  const [sortBy, setSortBy] = useState(null);
  const [sortOrder, setSortOrder] = useState("asc");

  const tournament = league === "euroleague" ? "lig" : "cup";

  useEffect(() => {
    fetchData();
  }, [
    currentPage,
    rowsPerPage,
    tournament,
    selectedColumns,
    filters,
    sortBy,
    sortOrder,
  ]);

  const fetchData = async () => {
    setLoading(true);
    const offset = currentPage * rowsPerPage;
    const columnsParam = selectedColumns.join(",");
    let dataUrl = `http://127.0.0.1:5000/api/v1/${tournament}_box_score?offset=${offset}&limit=${rowsPerPage}&columns=${columnsParam}`;
    if (sortBy) {
      dataUrl += `&sortBy=${sortBy}&order=${sortOrder}`;
    }
    let countUrl = `http://127.0.0.1:5000/api/v1/${tournament}_box_score/count`;

    // Add filters to the URL
    if (Object.keys(filters).length > 0) {
      const filterParams = Object.entries(filters)
        .map(([column, values]) => values.map((value) => `${column}:${value}`))
        .flat()
        .join(",");
      dataUrl += `&filters=${filterParams}`;
      countUrl += `?filters=${filterParams}`;
    }

    try {
      const [dataResponse, countResponse] = await Promise.all([
        fetch(dataUrl),
        fetch(countUrl),
      ]);

      if (!dataResponse.ok || !countResponse.ok) {
        throw new Error(
          `HTTP error! status: ${dataResponse.status} or ${countResponse.status}`
        );
      }

      const [result, countResult] = await Promise.all([
        dataResponse.json(),
        countResponse.json(),
      ]);

      setData(result);
      setTotalRows(countResult.total);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching data:", error);
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
    setCurrentPage(0); // Reset to first page when filters change
  };

  const handleSort = (column) => {
    if (sortBy === column) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortBy(column);
      setSortOrder("asc");
    }
  };

  const handleAdd = async (newRowData) => {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/${tournament}_box_score`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(newRowData),
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      await fetchData(); // Refresh data after successful add
      return true;
    } catch (error) {
      console.error("Error adding new row:", error);
      throw error;
    }
  };

  const handleDelete = async (game_player_id) => {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/${tournament}_box_score/${game_player_id}`,
        {
          method: "DELETE",
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      await fetchData(); // Refresh data after successful delete
      return true;
    } catch (error) {
      console.error("Error deleting row:", error);
      throw error;
    }
  };

  const handleUpdate = async (game_player_id, column, value) => {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/${tournament}_box_score/${game_player_id}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ [column]: value }),
        }
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      await fetchData(); // Refresh data after successful update
      return true;
    } catch (error) {
      console.error("Error updating row:", error);
      throw error;
    }
  };

  if (error) return <p>Error: {error}</p>;

  return (
    <StatPageTemplate league={league} stat="Box Score" UserView={BoxScoreUserView}>
      <div className={styles.PageContent}>
        <h2>
          {league.charAt(0).toUpperCase() + league.slice(1)} Box Score Statistics
        </h2>
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
            onFetchData={fetchData}
            foreignKeyColumns={foreignKeyColumns}
            primaryKey={primaryKey}
            columnTypes={columnTypes}
          />
        </div>
      </div>
    </StatPageTemplate>
  );

}
