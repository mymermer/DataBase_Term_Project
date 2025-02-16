"use client";

import React, { useEffect, useState } from "react";
import StatPageTemplate from "../../../components/StatPageTemplate";
import DataTable from "../../../components/DataTable";
import styles from "../../../styles/Page.module.css";
import PointsUserView from "../../../components/PointsUserView";


const allColumns = [
  "game_point_id",
  "game_player_id",
  "game_play_id",
  "game_id",
  "game",
  "round_of_game",
  "phase",
  "season_player_id",
  "season_team_id",
  "player",
  "action_id",
  "action_of_play",
  "points",
  "coord_x",
  "coord_y",
  "zone_of_play",
  "minute",
  "points_a",
  "points_b",
  "date_time_stp",
];

const foreignKeyColumns = [
  "season_team_id",
  "game_id",
  "game_play_id",
  "game_player_id",
  "season_player_id",
];

const primaryKey = 'game_point_id';
const columnTypes = {
  game_point_id: 'game_point_id',
  game_player_id: 'game_player_id',
  game_play_id: 'game_play_id',
  game_id: 'game_id',
  game: 'game',
  round_of_game: 'integer',
  phase: 'string',
  season_player_id: 'season_player_id',
  season_team_id: 'season_team_id',
  player: 'string',
  action_id: 'integer',
  action_of_play: 'string',
  points: 'integer',
  coord_x: 'float',
  coord_y: 'float',
  zone_of_play: 'string',
  minute: 'integer',
  points_a: 'integer',
  points_b: 'integer',
  date_time_stp: 'date_time'
};

export default function PointsPage({ params }) {
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
    setError(null); // Added to clear previous errors
    const offset = currentPage * rowsPerPage;
    const columnsParam = selectedColumns.join(",");
    let dataUrl = `http://127.0.0.1:5000/api/v1/${tournament}_points?offset=${offset}&limit=${rowsPerPage}&columns=${columnsParam}`;
    if (sortBy) {
      dataUrl += `&sortBy=${sortBy}&order=${sortOrder}`;
    }
    let countUrl = `http://127.0.0.1:5000/api/v1/${tournament}_points/count`;

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
    setError(null)
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/${tournament}_points`,
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
      setError(error.message);
      throw error;
    }
  };

  const handleDelete = async (gamePointId) => {
    setError(null)
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/${tournament}_points/${gamePointId}`,
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
      setError(error.message);
      throw error;
    }
  };

  const handleUpdate = async (gamePointId, column, value) => {
    setError(null)
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/${tournament}_points/${gamePointId}`,
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
      setError(error.message);

      throw error;
    }
  };


  return (
    <StatPageTemplate league={league} stat="Points" UserView={PointsUserView}>
      <div className={styles.PageContent}>
        <h2>
          {league.charAt(0).toUpperCase() + league.slice(1)} Points Statistics
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

