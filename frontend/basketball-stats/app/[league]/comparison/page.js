"use client";

import React, { useEffect, useState } from "react";
import StatPageTemplate from "../../../components/StatPageTemplate";
import DataTable from "../../../components/DataTable";
import styles from "../../../styles/Page.module.css";
import ComparisonUserView from "../../../components/ComparisonUserView";
import ErrorDisplay from "../../../components/ErrorDisplay";

const allColumns = [
  "game_id",
  "game",
  "round_of_game",
  "phase",
  "season_team_id_a",
  "season_team_id_b",
  "fast_break_points_a",
  "fast_break_points_b",
  "turnover_points_a",
  "turnover_points_b",
  "second_chance_points_a",
  "second_chance_points_b",
  "defensive_rebounds_a",
  "offensive_rebounds_b",
  "offensive_rebounds_a",
  "defensive_rebounds_b",
  "turnovers_starters_a",
  "turnovers_bench_a",
  "turnovers_starters_b",
  "turnovers_bench_b",
  "steals_starters_a",
  "steals_bench_a",
  "steals_starters_b",
  "steals_bench_b",
  "assists_starters_a",
  "assists_bench_a",
  "assists_starters_b",
  "assists_bench_b",
  "points_starters_a",
  "points_bench_a",
  "points_starters_b",
  "points_bench_b",
  "max_lead_a",
  "max_lead_b",
  "minute_max_lead_a",
  "minute_max_lead_b",
];

const foreignKeyColumns = ["season_team_id", "game_id"];

const primaryKey = "game_id";
const columnTypes = {
  game_id: "game_id",
  game: "game",
  round_of_game: "integer",
  phase: "string",
  season_team_id_a: "season_team_id",
  season_team_id_b: "season_team_id",
  fast_break_points_a: "integer",
  fast_break_points_b: "integer",
  turnover_points_a: "integer",
  turnover_points_b: "integer",
  second_chance_points_a: "integer",
  second_chance_points_b: "integer",
  defensive_rebounds_a: "integer",
  offensive_rebounds_b: "integer",
  offensive_rebounds_a: "integer",
  defensive_rebounds_b: "integer",
  turnovers_starters_a: "integer",
  turnovers_bench_a: "integer",
  turnovers_starters_b: "integer",
  turnovers_bench_b: "integer",
  steals_starters_a: "integer",
  steals_bench_a: "integer",
  steals_starters_b: "integer",
  steals_bench_b: "integer",
  assists_starters_a: "integer",
  assists_bench_a: "integer",
  assists_starters_b: "integer",
  assists_bench_b: "integer",
  points_starters_a: "integer",
  points_bench_a: "integer",
  points_starters_b: "integer",
  points_bench_b: "integer",
  max_lead_a: "integer",
  max_lead_b: "integer",
  minute_max_lead_a: "integer",
  minute_max_lead_b: "integer",
};

export default function ComparisonPage({ params }) {
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
    let dataUrl = `http://127.0.0.1:5000/api/v1/${tournament}_comparison?offset=${offset}&limit=${rowsPerPage}&columns=${columnsParam}`;
    if (sortBy) {
      dataUrl += `&sortBy=${sortBy}&order=${sortOrder}`;
    }
    let countUrl = `http://127.0.0.1:5000/api/v1/${tournament}_comparison/count`;

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
        `http://127.0.0.1:5000/api/v1/${tournament}_comparison`,
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
        `http://127.0.0.1:5000/api/v1/${tournament}_comparison/${gameId}`,
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
        `http://127.0.0.1:5000/api/v1/${tournament}_comparison/${gameId}`,
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
    <StatPageTemplate
      league={league}
      stat="Comparison"
      UserView={ComparisonUserView}
    >
      <div className={styles.PageContent}>
        <h2>
          {league.charAt(0).toUpperCase() + league.slice(1)} Comparison
          Statistics
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
