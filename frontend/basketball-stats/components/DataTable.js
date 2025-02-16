"use client";

import React, { useState, useRef, useEffect } from "react";
import styles from "../styles/DataTable.module.css";
import {
  ChevronDown,
  ChevronUp,
  ArrowUpDown,
  Check,
  Filter,
  Columns,
  Plus,
  Trash,
  Edit,
  X,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";
import LoadingOverlay from "./LoadingOverlay";
import ErrorDisplay from "./ErrorDisplay";
import DateTimeInput from "./DateTimeInput";
import DateInput from "./DateInput";
import TimeInput from "./TimeInput";

const DataTable = ({
  initialData,
  initialColumns,
  allColumns,
  currentPage,
  rowsPerPage,
  totalRows,
  onPageChange,
  onRowsPerPageChange,
  onColumnChange,
  onFilterChange,
  isLoading,
  onSort,
  sortBy,
  sortOrder,
  onAdd,
  onDelete,
  onUpdate,
  foreignKeyColumns,
  league,
  onFetchData,
  error,
  primaryKey,
  columnTypes,
}) => {
  const [data, setData] = useState(initialData);
  const [visibleColumns, setVisibleColumns] = useState(initialColumns);
  const [filters, setFilters] = useState({});
  const [showColumnSelector, setShowColumnSelector] = useState(false);
  const [showFilterSelector, setShowFilterSelector] = useState(false);
  const [currentFilterColumn, setCurrentFilterColumn] = useState(null);
  const [tempVisibleColumns, setTempVisibleColumns] = useState(visibleColumns);
  const [bubbleWidth, setBubbleWidth] = useState(200);
  const [showPopup, setShowPopup] = useState(false);
  const [popupType, setPopupType] = useState(null);
  const [newRowData, setNewRowData] = useState({});
  const [deleteId, setDeleteId] = useState("");
  const [updateId, setUpdateId] = useState("");
  const [updateColumn, setUpdateColumn] = useState("");
  const [updateValue, setUpdateValue] = useState("");
  const [message, setMessage] = useState(null);
  const [errors, setErrors] = useState({});

  const columnSelectorRef = useRef(null);
  const filterSelectorRef = useRef(null);
  const columnButtonRef = useRef(null);
  const filterButtonRef = useRef(null);
  const tableWrapperRef = useRef(null);

  useEffect(() => {
    setData(initialData);
  }, [initialData]);

  useEffect(() => {
    setVisibleColumns(initialColumns);
  }, [initialColumns]);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        columnSelectorRef.current &&
        !columnSelectorRef.current.contains(event.target) &&
        !columnButtonRef.current.contains(event.target)
      ) {
        setShowColumnSelector(false);
      }
      if (
        filterSelectorRef.current &&
        !filterSelectorRef.current.contains(event.target) &&
        !filterButtonRef.current.contains(event.target)
      ) {
        setShowFilterSelector(false);
        setCurrentFilterColumn(null);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  useEffect(() => {
    const longestColumnName = allColumns.reduce((longest, current) =>
      current.length > longest.length ? current : longest
    );
    const tempElement = document.createElement("span");
    tempElement.style.visibility = "hidden";
    tempElement.style.position = "absolute";
    tempElement.style.whiteSpace = "nowrap";
    tempElement.innerHTML = longestColumnName;
    document.body.appendChild(tempElement);
    const width = Math.max(200, tempElement.offsetWidth + 50);
    document.body.removeChild(tempElement);
    setBubbleWidth(width);
  }, [allColumns]);

  const toggleColumn = (columnName) => {
    setTempVisibleColumns((prev) =>
      prev.includes(columnName)
        ? prev.filter((col) => col !== columnName)
        : [...prev, columnName]
    );
  };

  const applyColumnSelection = () => {
    setVisibleColumns(tempVisibleColumns);
    onColumnChange(tempVisibleColumns);
    setShowColumnSelector(false);
  };

  const requestSort = (key) => {
    onSort(key);
  };

  const applyFilter = () => {
    const filterValue = document.querySelector(`.${styles.filterInput}`).value;
    if (filterValue.trim() !== "") {
      const newFilters = { ...filters };
      if (!newFilters[currentFilterColumn]) {
        newFilters[currentFilterColumn] = [];
      }
      if (!newFilters[currentFilterColumn].includes(filterValue)) {
        newFilters[currentFilterColumn].push(filterValue);
      }
      setFilters(newFilters);
      onFilterChange(newFilters);
    }
    setShowFilterSelector(false);
    setCurrentFilterColumn(null);
  };

  const removeFilter = (column, value) => {
    const newFilters = { ...filters };
    newFilters[column] = newFilters[column].filter((v) => v !== value);
    if (newFilters[column].length === 0) {
      delete newFilters[column];
    }
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const totalPages = Math.max(1, Math.ceil(totalRows / rowsPerPage));

  const handlePopupOpen = (type) => {
    setPopupType(type);
    setShowPopup(true);
  };

  const handlePopupClose = () => {
    setShowPopup(false);
    setPopupType(null);
    setNewRowData({});
    setDeleteId("");
    setUpdateId("");
    setUpdateColumn("");
    setUpdateValue("");
    setMessage(null); //Added to clear message on close
  };

  const handleDelete = async () => {
    try {
      await onDelete(deleteId);
      setMessage({ type: "success", text: "Row deleted successfully" });
      handlePopupClose();
      onFetchData();
    } catch (error) {
      setMessage({ type: "error", text: error.message });
    }
  };

  const handleUpdate = async () => {
    try {
      let formattedUpdateValue = updateValue;
      if (
        columnTypes[updateColumn] === "date_time" ||
        columnTypes[updateColumn] === "date" ||
        columnTypes[updateColumn] === "time"
      ) {
        formattedUpdateValue = formatDateInput(updateValue);
      }
      await onUpdate(updateId, updateColumn, formattedUpdateValue);
      setMessage({ type: "success", text: "Row updated successfully" });
      handlePopupClose();
      onFetchData();
    } catch (error) {
      setMessage({ type: "error", text: error.message });
    }
  };

  const validateInput = (value, type) => {
    switch (type) {
      case "integer":
        return Number.isInteger(Number(value));
      case "float":
        return !isNaN(parseFloat(value)) && isFinite(value);
      case "date_time":
        const dateTimeRegex = /^(\d{2})\/(\d{2})\/(\d{4}) (\d{2}):(\d{2})$/;
        return dateTimeRegex.test(value);
      case "date":
        const dateRegex = /^(\d{2})\/(\d{2})\/(\d{4})$/;
        return dateRegex.test(value);
      case "time":
        const timeRegex = /^(\d{2}):(\d{2})$/;
        return timeRegex.test(value);
      case "game_id":
        const gameIdRegex = /^(E|U)\d{4}_\d{3}$/;
        return gameIdRegex.test(value);
      case "game":
        const gameRegex = /^[A-Z]{3}-[A-Z]{3}$/;
        return gameRegex.test(value);
      case "season_team_id":
        const seasonTeamIdRegex = /^(E|U)\d{4}_[A-Z]{3}$/;
        return seasonTeamIdRegex.test(value);
      case "game_player_id":
        const gamePlayerIdRegex = /^(E|U)\d{4}_\d{3}_[A-Za-z0-9]+$/;
        return gamePlayerIdRegex.test(value);
      case "season_player_id":
        const seasonPlayerIdRegex = /^(E|U)\d{4}_[A-Za-z0-9]+_[A-Za-z]{3}$/;
        return seasonPlayerIdRegex.test(value);
      case "game_play_id":
      case "game_point_id": // Same validation as game_play_id
        const gamePlayIdRegex = /^(E|U)\d{4}_\d{3}_\d+$/;
        return gamePlayIdRegex.test(value);
      case "winner":
        return ["team_a", "team_b", "draw"].includes(value);
      case "game_time":
        const gameTimeRegex = /^\d+:\d+:\d+$/;
        return gameTimeRegex.test(value);
      default:
        return true;
    }
  };

  const errorMessages = {
    integer: "Value must be an integer.",
    float: "Value must be a float.",
    date_time: "Value must be in the format MM/DD/YYYY HH:MM.",
    date: "Value must be in the format MM/DD/YYYY.",
    time: "Value must be in the format HH:MM.",
    game_id: "Value must be in a format like E2007_001 or U2007_001.",
    game: "Value must be in the format TEAM1-TEAM2 (e.g., MAD-BAR).",
    season_team_id: "Value must be in a format like E2007_TEAM or U2007_TEAM.",
    game_player_id:
      "Value must be in the format U2007_001_ABC (e.g., U2007_123_PJEZ or E2013_123_PJEZ).",
    season_player_id:
      "Value must be in the format U2007_ABC123_ABC (e.g., U2007_PKQK_JER or E2014_PNZ130_MAD).",
    game_play_id:
      "Value must be in the format U2007_123_13245 (e.g., U2007_001_006 or E2009_052_1208).",
    game_point_id:
      "Value must be in the format U2007_123_13245 (e.g., U2007_001_006 or E2009_052_1208).",
    winner: "Value must be one of: 'team_a', 'team_b', or 'draw'.",
    game_time: "Value must match the format MM:SS:MS (e.g., 40:00:00).",
  };

  const formatDateInput = (value) => {
    return value; // The DatePicker now returns the correct format
  };

  const handleApply = async () => {
    try {
      let hasError = false;

      // Validation for the "Add" popup
      if (popupType === "add") {
        for (const [column, value] of Object.entries(newRowData)) {
          if (!validateInput(value, columnTypes[column])) {
            hasError = true;
            setErrors((prevErrors) => ({
              ...prevErrors,
              [column]: errorMessages[columnTypes[column]],
            }));
          }
        }
      }

      // Validation for the "Update" popup
      if (popupType === "update") {
        if (!validateInput(updateValue, columnTypes[updateColumn])) {
          hasError = true;
          setErrors((prevErrors) => ({
            ...prevErrors,
            [updateColumn]: errorMessages[columnTypes[updateColumn]],
          }));
        }
        if (!validateInput(updateId, columnTypes[primaryKey])) {
          hasError = true;
          setErrors((prevErrors) => ({
            ...prevErrors,
            [primaryKey]: errorMessages[columnTypes[primaryKey]],
          }));
        }
      }

      // Validation for the "Delete" popup
      if (popupType === "delete") {
        if (!validateInput(deleteId, columnTypes[primaryKey])) {
          hasError = true;
          setErrors((prevErrors) => ({
            ...prevErrors,
            [primaryKey]: errorMessages[columnTypes[primaryKey]],
          }));
        }
      }

      if (hasError) {
        setMessage({ type: "error", text: "Please correct the errors." });
        return;
      }

      let result;
      switch (popupType) {
        case "add":
          result = await onAdd(newRowData);
          break;
        case "delete":
          result = await handleDelete();
          break;
        case "update":
          result = await handleUpdate();
          break;
      }

      setMessage({ type: "success", text: "Operation successful" });
      handlePopupClose();
      onFetchData();
    } catch (error) {
      setMessage({ type: "error", text: error.message });
    }
    setTimeout(() => setMessage(null), 3000);
  };

  useEffect(() => {
    const handleEsc = (event) => {
      if (event.key === "Escape") {
        handlePopupClose();
      }
    };
    window.addEventListener("keydown", handleEsc);

    return () => {
      window.removeEventListener("keydown", handleEsc);
    };
  }, []);

  const fetchData = async () => {
    try {
      setError(null);

      setIsLoading(true);

      await onFetchData();
    } catch (err) {
      setError("Unable to fetch data. Please try again later.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.fullWidthWrapper}>
      <div className={styles.dataTable}>
        <LoadingOverlay
          isLoading={isLoading}
          tableWrapperRef={tableWrapperRef}
        />
        {message && (
          <div className={`${styles.message} ${styles[message.type]}`}>
            {message.text}
          </div>
        )}
        <div className={styles.tableControls}>
          <div className={styles.topButtons}>
            <div className={styles.leftButtons}>
              <div className={styles.controlButtonWrapper}>
                <button
                  ref={columnButtonRef}
                  onClick={() => {
                    setShowColumnSelector((prev) => !prev);
                    setShowFilterSelector(false);
                  }}
                  className={styles.controlButton}
                >
                  <span className={styles.buttonIcon}>
                    <Columns size={16} />
                  </span>
                  More Columns
                </button>
                {showColumnSelector && (
                  <div
                    ref={columnSelectorRef}
                    className={styles.selectorBubble}
                    style={{ width: bubbleWidth }}
                  >
                    <h3>Select Columns</h3>
                    <div className={styles.columnList}>
                      {allColumns.map((column) => (
                        <label key={column} className={styles.columnOption}>
                          <span>{column}</span>
                          {tempVisibleColumns.includes(column) && (
                            <Check className={styles.checkIcon} size={16} />
                          )}
                          <input
                            type="checkbox"
                            checked={tempVisibleColumns.includes(column)}
                            onChange={() => toggleColumn(column)}
                            className={styles.hiddenCheckbox}
                          />
                        </label>
                      ))}
                    </div>
                    <div className={styles.applyButtonWrapper}>
                      <button
                        onClick={applyColumnSelection}
                        className={styles.applyButton}
                      >
                        Apply
                      </button>
                    </div>
                  </div>
                )}
              </div>
              <div className={styles.controlButtonWrapper}>
                <button
                  ref={filterButtonRef}
                  onClick={() => {
                    setShowFilterSelector((prev) => !prev);
                    setShowColumnSelector(false);
                    if (showFilterSelector) {
                      setCurrentFilterColumn(null);
                    }
                  }}
                  className={styles.controlButton}
                >
                  <span className={styles.buttonIcon}>
                    <Filter size={16} />
                  </span>
                  Add Filter
                </button>
                {showFilterSelector && (
                  <div
                    ref={filterSelectorRef}
                    className={styles.selectorBubble}
                    style={{ width: bubbleWidth }}
                  >
                    {!currentFilterColumn ? (
                      <>
                        <h3>Select Column to Filter</h3>
                        <div className={styles.columnList}>
                          {visibleColumns.map((column) => (
                            <button
                              key={column}
                              onClick={() => setCurrentFilterColumn(column)}
                              className={styles.columnOption}
                            >
                              {column}
                            </button>
                          ))}
                        </div>
                      </>
                    ) : (
                      <>
                        <h3>Filter {currentFilterColumn}</h3>
                        <input
                          type="text"
                          placeholder="Enter filter value"
                          className={styles.filterInput}
                          defaultValue={
                            filters[currentFilterColumn]
                              ? filters[currentFilterColumn][0]
                              : ""
                          }
                          onKeyPress={(e) => {
                            if (e.key === "Enter") {
                              applyFilter();
                            }
                          }}
                        />
                        <div className={styles.applyButtonWrapper}>
                          <button
                            onClick={applyFilter}
                            className={styles.applyButton}
                          >
                            Apply
                          </button>
                        </div>
                      </>
                    )}
                  </div>
                )}
              </div>
            </div>
            <div className={styles.crudButtons}>
              <button
                onClick={() => handlePopupOpen("add")}
                className={`${styles.crudButton} ${styles.addButton}`}
              >
                <Plus size={16} /> Add
              </button>
              <button
                onClick={() => handlePopupOpen("delete")}
                className={`${styles.crudButton} ${styles.deleteButton}`}
              >
                <Trash size={16} /> Delete
              </button>
              <button
                onClick={() => handlePopupOpen("update")}
                className={`${styles.crudButton} ${styles.updateButton}`}
              >
                <Edit size={16} /> Update
              </button>
            </div>
          </div>
          <div className={styles.filterTags}>
            {Object.entries(filters).map(([column, values]) =>
              values.map((value, index) => (
                <span key={`${column}-${index}`} className={styles.filterTag}>
                  {column}: {value}
                  <button
                    onClick={() => removeFilter(column, value)}
                    className={styles.removeFilterButton}
                  >
                    ×
                  </button>
                </span>
              ))
            )}
          </div>
        </div>
        <div
          className={`${styles.tableWrapper} ${
            isLoading ? styles.loading : ""
          }`}
          ref={tableWrapperRef}
        >
          <table className={styles.table}>
            <thead>
              <tr>
                {visibleColumns.map((column) => (
                  <th key={column} onClick={() => requestSort(column)}>
                    <div
                      style={{
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "space-between",
                      }}
                    >
                      <span>{column}</span>
                      {sortBy === column ? (
                        sortOrder === "asc" ? (
                          <ChevronUp className={styles.sortIcon} />
                        ) : (
                          <ChevronDown className={styles.sortIcon} />
                        )
                      ) : (
                        <ArrowUpDown className={styles.sortIcon} />
                      )}
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.length > 0 ? (
                data.map((row, rowIndex) => {
                  return (
                    <tr key={rowIndex}>
                      {visibleColumns.map((column) => (
                        <td key={column}>{row[column]}</td>
                      ))}
                    </tr>
                  );
                })
              ) : (
                <tr>
                  <td colSpan={visibleColumns.length}>
                    No data available (data length: {data.length})
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
        {error && <ErrorDisplay message={error} onRetry={onFetchData} />}
        <div className={styles.pagination}>
          <div className={styles.bottomButtons}>
            <button
              onClick={() => onPageChange(currentPage - 1)}
              disabled={currentPage === 0}
              className={styles.paginationButton}
            >
              <ChevronLeft size={20} />
            </button>
            <button
              onClick={() => onPageChange(currentPage + 1)}
              disabled={currentPage >= totalPages - 1}
              className={styles.paginationButton}
            >
              <ChevronRight size={20} />
            </button>
          </div>
          <div className={styles.paginationControls}>
            <span>
              Page{" "}
              <input
                type="number"
                min={1}
                max={totalPages}
                value={currentPage + 1} // Display the current page + 1
                onChange={(e) => {
                  const page = Math.max(
                    1,
                    Math.min(totalPages, Number(e.target.value))
                  ); // Clamp the value between 1 and totalPages
                  onPageChange(page - 1); // Convert to zero-based index
                }}
                onWheel={(e) => e.stopPropagation()} // Prevent page scrolling while using mouse scroll
                className={styles.pageInput} // Add custom styling for input field
                style={{
                  width: "40px",
                  margin: "auto",
                  textAlign: "center",
                }} // Inline styles for a compact design
              />{" "}
              of {totalPages}
            </span>
            <select
              value={rowsPerPage}
              onChange={(e) => onRowsPerPageChange(Number(e.target.value))}
            >
              <option value={25}>25 rows</option>
              <option value={50}>50 rows</option>
              <option value={100}>100 rows</option>
            </select>
          </div>
        </div>
      </div>
      {showPopup && (
        <div className={styles.popupOverlay} onClick={handlePopupClose}>
          <div
            className={styles.popup}
            onClick={(e) => e.stopPropagation()}
            style={{ overflow: "visible" }}
          >
            <button className={styles.closeButton} onClick={handlePopupClose}>
              <X size={24} />
            </button>
            <h2 className={styles.popupTitle}>
              {popupType.charAt(0).toUpperCase() + popupType.slice(1)}
            </h2>
            <div className={styles.warningMessage}>
              WARNING: This method will have impact on other tables due to
              foreign key columns: {foreignKeyColumns.join(", ")}.
            </div>
            <div className={styles.popupContent}>
              {popupType === "add" && (
                <div className={styles.addForm}>
                  {allColumns.map((column) => (
                    <div key={column} className={styles.formGroup}>
                      <label htmlFor={column}>{column}</label>
                      {columnTypes[column] === "date_time" ? (
                        <DateTimeInput
                          value={newRowData[column] || ""}
                          onChange={(value) => {
                            if (validateInput(value, columnTypes[column])) {
                              setNewRowData({ ...newRowData, [column]: value });
                            }
                          }}
                          placeholder="MM/DD/YYYY HH:MM"
                        />
                      ) : columnTypes[column] === "date" ? (
                        <DateInput
                          value={newRowData[column] || ""}
                          onChange={(value) => {
                            if (validateInput(value, columnTypes[column])) {
                              setNewRowData({ ...newRowData, [column]: value });
                            }
                          }}
                          placeholder={"MM/DD/YYYY"}
                        />
                      ) : columnTypes[column] === "time" ? (
                        <TimeInput
                          value={newRowData[column] || ""}
                          onChange={(value) => {
                            if (validateInput(value, columnTypes[column])) {
                              setNewRowData({ ...newRowData, [column]: value });
                            }
                          }}
                          placeholder={"HH:MM"}
                        />
                      ) : (
                        <input
                          type="text"
                          id={column}
                          value={newRowData[column] || ""}
                          onChange={(e) => {
                            const value = e.target.value;
                            setNewRowData({ ...newRowData, [column]: value }); // Update value immediately
                          }}
                          onBlur={(e) => {
                            const value = e.target.value;
                            const isValid = validateInput(
                              value,
                              columnTypes[column]
                            );

                            setErrors((prevErrors) => {
                              if (isValid) {
                                const { [column]: _, ...rest } = prevErrors; // Remove the error for this column
                                return rest;
                              } else {
                                return {
                                  ...prevErrors,
                                  [column]: errorMessages[columnTypes[column]], // Set error only on blur
                                };
                              }
                            });
                          }}
                          placeholder={`Enter ${columnTypes[column]}`}
                          className={`${styles.input} ${
                            errors[column] ? styles.invalidInput : ""
                          }`}
                        />
                      )}
                      {/* Add the error message here */}
                      {errors[column] && (
                        <span className={styles.errorText}>
                          {errors[column]}
                        </span>
                      )}
                    </div>
                  ))}
                </div>
              )}
              {popupType === "delete" && (
                <div className={styles.deleteForm}>
                  <div className={styles.formGroup}>
                    <label htmlFor="deleteId">{primaryKey}</label>
                    <input
                      type="text"
                      id="deleteId"
                      value={deleteId}
                      onChange={(e) => {
                        const value = e.target.value;
                        setDeleteId(value); // Update value immediately

                        const isValid = validateInput(
                          value,
                          columnTypes[primaryKey]
                        );

                        // Update error state based on validation
                        setErrors((prevErrors) => {
                          if (isValid) {
                            const { [primaryKey]: _, ...rest } = prevErrors; // Remove the error for this column
                            return rest;
                          } else {
                            return {
                              ...prevErrors,
                              [primaryKey]:
                                errorMessages[columnTypes[primaryKey]],
                            };
                          }
                        });
                      }}
                      placeholder={`Enter ${primaryKey}`}
                      className={`${styles.input} ${
                        errors[primaryKey] ? styles.invalidInput : ""
                      }`}
                    />
                    {/* Display the error message */}
                    {errors[primaryKey] && (
                      <span className={styles.errorText}>
                        {errors[primaryKey]}
                      </span>
                    )}
                  </div>
                </div>
              )}
              {popupType === "update" && (
                <div className={styles.updateForm}>
                  <div className={styles.formGroup}>
                    <label htmlFor="updateId">{primaryKey}</label>
                    <input
                      type="text"
                      id="updateId"
                      value={updateId}
                      onChange={(e) => {
                        const value = e.target.value;
                        setUpdateId(value); // Update value immediately

                        const isValid = validateInput(
                          value,
                          columnTypes[primaryKey]
                        ); // Validate input

                        // Update error state based on validation
                        setErrors((prevErrors) => {
                          if (isValid) {
                            const { [primaryKey]: _, ...rest } = prevErrors; // Remove the error for this column
                            return rest;
                          } else {
                            return {
                              ...prevErrors,
                              [primaryKey]:
                                errorMessages[columnTypes[primaryKey]], // Add error message
                            };
                          }
                        });
                      }}
                      onBlur={(e) => {
                        const value = e.target.value;
                        if (!validateInput(value, columnTypes[primaryKey])) {
                          setErrors((prevErrors) => ({
                            ...prevErrors,
                            [primaryKey]:
                              errorMessages[columnTypes[primaryKey]],
                          }));
                        }
                      }}
                      placeholder={`Enter ${primaryKey}`}
                      className={`${styles.input} ${
                        errors[primaryKey] ? styles.invalidInput : ""
                      }`}
                    />
                    {/* Display the error message */}
                    {errors[primaryKey] && (
                      <span className={styles.errorText}>
                        {errors[primaryKey]}
                      </span>
                    )}
                  </div>
                  <div className={styles.formGroup}>
                    <label htmlFor="updateColumn">Column to Update</label>
                    <select
                      id="updateColumn"
                      value={updateColumn}
                      onChange={(e) => setUpdateColumn(e.target.value)}
                      className={styles.input}
                    >
                      <option value="">Select a column</option>
                      {allColumns.map((column) => (
                        <option key={column} value={column}>
                          {column}
                        </option>
                      ))}
                    </select>
                  </div>
                  <div className={styles.formGroup}>
                    <label htmlFor="updateValue">New Value</label>
                    {updateColumn &&
                    columnTypes[updateColumn] === "date_time" ? (
                      <DateTimeInput
                        value={updateValue}
                        onChange={(value) => {
                          if (validateInput(value, columnTypes[updateColumn])) {
                            setUpdateValue(value);
                          }
                        }}
                        placeholder="MM/DD/YYYY HH:MM"
                      />
                    ) : columnTypes[updateColumn] === "date" ? (
                      <DateInput
                        value={updateValue}
                        onChange={(value) => {
                          if (validateInput(value, columnTypes[updateColumn])) {
                            setUpdateValue(value);
                          }
                        }}
                        placeholder={"MM/DD/YYYY"}
                      />
                    ) : columnTypes[updateColumn] === "time" ? (
                      <TimeInput
                        value={updateValue}
                        onChange={(value) => {
                          if (validateInput(value, columnTypes[updateColumn])) {
                            setUpdateValue(value);
                          }
                        }}
                        placeholder={"HH:MM"}
                      />
                    ) : (
                      <input
                        type="text"
                        id="updateValue"
                        value={updateValue}
                        onChange={(e) => {
                          const value = e.target.value;
                          setUpdateValue(value); // Update value immediately
                        }}
                        onBlur={(e) => {
                          const value = e.target.value;
                          const isValid = validateInput(
                            value,
                            columnTypes[updateColumn]
                          );

                          setErrors((prevErrors) => {
                            if (isValid) {
                              const { [updateColumn]: _, ...rest } = prevErrors; // Remove the error for this column
                              return rest;
                            } else {
                              return {
                                ...prevErrors,
                                [updateColumn]:
                                  errorMessages[columnTypes[updateColumn]], // Set error only on blur
                              };
                            }
                          });
                        }}
                        placeholder={
                          updateColumn
                            ? `Enter ${columnTypes[updateColumn]}`
                            : "Select a column first"
                        }
                        className={`${styles.input} ${
                          errors[updateColumn] ? styles.invalidInput : ""
                        }`}
                        disabled={!updateColumn}
                      />
                    )}
                    {/* Add the error message here */}
                    {errors[updateColumn] && (
                      <span className={styles.errorText}>
                        {errors[updateColumn]}
                      </span>
                    )}
                  </div>
                </div>
              )}
            </div>
            <div className={styles.popupFooter}>
              <button
                onClick={handlePopupClose}
                className={styles.cancelButton}
              >
                Cancel
              </button>
              <button onClick={handleApply} className={styles.applyButton}>
                Apply
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default DataTable;
