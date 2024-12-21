"use client";

import React, { useEffect, useState } from "react";
import StatPageTemplate from "../../../components/StatPageTemplate";
import DataTable from "../../../components/DataTable";
import styles from "../../../styles/Page.module.css";
import ComparisonUserView from "../../../components/ComparisonUserView";

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
  "points_max_lead_a",
  "points_max_lead_b",
];

const foreignKeyColumns = [
  "season_team_id",
  "game_id",
];

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
      console.error("Error adding new row:", error);
      throw error;
    }
  };

  const handleDelete = async (gameId) => {
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
      console.error("Error deleting row:", error);
      throw error;
    }
  };

  const handleUpdate = async (gameId, column, value) => {
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
      console.error("Error updating row:", error);
      throw error;
    }
  };

  if (error) return <p>Error: {error}</p>;

  return (
    <StatPageTemplate league={league} stat="Comparison" UserView={ComparisonUserView}>
      <div className={styles.PageContent}>
        <h2>
          {league.charAt(0).toUpperCase() + league.slice(1)} Comparison Statistics
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
          />
        </div>
      </div>
    </StatPageTemplate>
  );
}