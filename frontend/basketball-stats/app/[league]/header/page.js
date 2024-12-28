"use client";

import React, { useEffect, useState } from "react";
import StatPageTemplate from "../../../components/StatPageTemplate";
import DataTable from "../../../components/DataTable";
import styles from "../../../styles/Page.module.css";
import HeaderUserView from "../../../components/HeaderUserView";
import ErrorDisplay from "../../../components/ErrorDisplay";

const allColumns = [
  "game_id",
  "game",
  "date_of_game",
  "time_of_game",
  "round_of_game",
  "phase",
  "season_team_id_a",
  "season_team_id_b",
  "score_a",
  "score_b",
  "coach_a",
  "coach_b",
  "game_time",
  "referee_1",
  "referee_2",
  "referee_3",
  "stadium",
  "capacity",
  "fouls_a",
  "fouls_b",
  "timeouts_a",
  "timeouts_b",
  "score_quarter_1_a",
  "score_quarter_2_a",
  "score_quarter_3_a",
  "score_quarter_4_a",
  "score_quarter_1_b",
  "score_quarter_2_b",
  "score_quarter_3_b",
  "score_quarter_4_b",
  "score_extra_time_1_a",
  "score_extra_time_2_a",
  "score_extra_time_3_a",
  "score_extra_time_4_a",
  "score_extra_time_1_b",
  "score_extra_time_2_b",
  "score_extra_time_3_b",
  "score_extra_time_4_b",
  "winner",
];

const foreignKeyColumns = ["season_team_id"];

const primaryKey = "game_id";
const columnTypes = {
  game_id: "string",
  game: "string",
  date_of_game: "string",
  time_of_game: "string",
  round_of_game: "integer",
  phase: "string",
  season_team_id_a: "string",
  season_team_id_b: "string",
  score_a: "integer",
  score_b: "integer",
  coach_a: "string",
  coach_b: "string",
  game_time: "string",
  referee_1: "string",
  referee_2: "string",
  referee_3: "string",
  stadium: "string",
  capacity: "integer",
  fouls_a: "integer",
  fouls_b: "integer",
  timeouts_a: "integer",
  timeouts_b: "integer",
  score_quarter_1_a: "integer",
  score_quarter_2_a: "integer",
  score_quarter_3_a: "integer",
  score_quarter_4_a: "integer",
  score_quarter_1_b: "integer",
  score_quarter_2_b: "integer",
  score_quarter_3_b: "integer",
  score_quarter_4_b: "integer",
  score_extra_time_1_a: "integer",
  score_extra_time_2_a: "integer",
  score_extra_time_3_a: "integer",
  score_extra_time_4_a: "integer",
  score_extra_time_1_b: "integer",
  score_extra_time_2_b: "integer",
  score_extra_time_3_b: "integer",
  score_extra_time_4_b: "integer",
  winner: "string",
};

export default function HeaderPage({ params }) {
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
    setError(null);
    const offset = currentPage * rowsPerPage;
    const columnsParam = selectedColumns.join(",");
    let dataUrl = `http://127.0.0.1:5000/api/v1/${tournament}_header?offset=${offset}&limit=${rowsPerPage}&columns=${columnsParam}`;
    if (sortBy) {
      dataUrl += `&sortBy=${sortBy}&order=${sortOrder}`;
    }
    let countUrl = `http://127.0.0.1:5000/api/v1/${tournament}_header/count`;

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
      setLoading(false);
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
    setError(null);
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/${tournament}_header`,
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
  };

  const handleDelete = async (gameId) => {
    setError(null);
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/${tournament}_header/${gameId}`,
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
  };

  const handleUpdate = async (gameId, column, value) => {
    setError(null);
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/${tournament}_header/${gameId}`,
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
  };

  {
    error && <ErrorDisplay message={error} onRetry={fetchData} />;
  }

  return (
    <StatPageTemplate league={league} stat="Header" UserView={HeaderUserView}>
      <div className={styles.PageContent}>
        <h2>
          {league.charAt(0).toUpperCase() + league.slice(1)} Header Statistics
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
            onRetry={fetchData}
            primaryKey={primaryKey}
            columnTypes={columnTypes}
          />
        </div>
      </div>
    </StatPageTemplate>
  );
}
