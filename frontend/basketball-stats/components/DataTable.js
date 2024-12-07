'use client'

import React, { useState, useRef, useEffect } from 'react';
import styles from '../styles/DataTable.module.css';
import { ChevronDown, ChevronUp, ArrowUpDown, Check, Filter, Columns, Plus, Trash, Edit } from 'lucide-react';
import LoadingOverlay from './LoadingOverlay';

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
  isLoading
}) => {
  const [data, setData] = useState(initialData);
  const [visibleColumns, setVisibleColumns] = useState(initialColumns);
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'ascending' });
  const [filters, setFilters] = useState({});
  const [showColumnSelector, setShowColumnSelector] = useState(false);
  const [showFilterSelector, setShowFilterSelector] = useState(false);
  const [currentFilterColumn, setCurrentFilterColumn] = useState(null);
  const [tempVisibleColumns, setTempVisibleColumns] = useState(visibleColumns);
  const [bubbleWidth, setBubbleWidth] = useState(200);
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
      if (columnSelectorRef.current && !columnSelectorRef.current.contains(event.target) && !columnButtonRef.current.contains(event.target)) {
        setShowColumnSelector(false);
      }
      if (filterSelectorRef.current && !filterSelectorRef.current.contains(event.target) && !filterButtonRef.current.contains(event.target)) {
        setShowFilterSelector(false);
        setCurrentFilterColumn(null);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  useEffect(() => {
    const longestColumnName = allColumns.reduce((longest, current) => 
      current.length > longest.length ? current : longest
    );
    const tempElement = document.createElement('span');
    tempElement.style.visibility = 'hidden';
    tempElement.style.position = 'absolute';
    tempElement.style.whiteSpace = 'nowrap';
    tempElement.innerHTML = longestColumnName;
    document.body.appendChild(tempElement);
    const width = Math.max(200, tempElement.offsetWidth + 50);
    document.body.removeChild(tempElement);
    setBubbleWidth(width);
  }, [allColumns]);

  const toggleColumn = (columnName) => {
    setTempVisibleColumns(prev => 
      prev.includes(columnName) 
        ? prev.filter(col => col !== columnName)
        : [...prev, columnName]
    );
  };

  const applyColumnSelection = () => {
    setVisibleColumns(tempVisibleColumns);
    onColumnChange(tempVisibleColumns);
    setShowColumnSelector(false);
  };

  const requestSort = (key) => {
    let direction = 'ascending';
    if (sortConfig.key === key && sortConfig.direction === 'ascending') {
      direction = 'descending';
    }
    setSortConfig({ key, direction });
  };

  const applyFilter = () => {
    const filterValue = document.querySelector(`.${styles.filterInput}`).value;
    if (filterValue.trim() !== '') {
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
    newFilters[column] = newFilters[column].filter(v => v !== value);
    if (newFilters[column].length === 0) {
      delete newFilters[column];
    }
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  const totalPages = Math.max(1, Math.ceil(totalRows / rowsPerPage));

  return (
    <div className={styles.fullWidthWrapper}>
      <div className={styles.dataTable}>
        <LoadingOverlay isLoading={isLoading} tableWrapperRef={tableWrapperRef} />
        <div className={styles.tableControls}>
          <div className={styles.topButtons}>
            <div className={styles.leftButtons}>
              <div className={styles.controlButtonWrapper}>
                <button 
                  ref={columnButtonRef}
                  onClick={() => {
                    setShowColumnSelector(prev => !prev);
                    setShowFilterSelector(false);
                  }} 
                  className={styles.controlButton}
                >
                  <span className={styles.buttonIcon}><Columns size={16} /></span>
                  More Columns
                </button>
                {showColumnSelector && (
                  <div ref={columnSelectorRef} className={styles.selectorBubble} style={{ width: bubbleWidth }}>
                    <h3>Select Columns</h3>
                    <div className={styles.columnList}>
                      {allColumns.map(column => (
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
                      <button onClick={applyColumnSelection} className={styles.applyButton}>Apply</button>
                    </div>
                  </div>
                )}
              </div>
              <div className={styles.controlButtonWrapper}>
                <button 
                  ref={filterButtonRef}
                  onClick={() => {
                    setShowFilterSelector(prev => !prev);
                    setShowColumnSelector(false);
                    if (showFilterSelector) {
                      setCurrentFilterColumn(null);
                    }
                  }} 
                  className={styles.controlButton}
                >
                  <span className={styles.buttonIcon}><Filter size={16} /></span>
                  Add Filter
                </button>
                {showFilterSelector && (
                  <div ref={filterSelectorRef} className={styles.selectorBubble} style={{ width: bubbleWidth }}>
                    {!currentFilterColumn ? (
                      <>
                        <h3>Select Column to Filter</h3>
                        <div className={styles.columnList}>
                          {visibleColumns.map(column => (
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
                          defaultValue={filters[currentFilterColumn] ? filters[currentFilterColumn][0] : ''}
                          onKeyPress={(e) => {
                            if (e.key === 'Enter') {
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
          </div>
          <div className={styles.filterTags}>
            {Object.entries(filters).map(([column, values]) => (
              values.map((value, index) => (
                <span key={`${column}-${index}`} className={styles.filterTag}>
                  {column}: {value}
                  <button onClick={() => removeFilter(column, value)} className={styles.removeFilterButton}>×</button>
                </span>
              ))
            ))}
          </div>
        </div>
        <div className={`${styles.tableWrapper} ${isLoading ? styles.loading : ''}`} ref={tableWrapperRef}>
          <table className={styles.table}>
            <thead>
              <tr>
                {visibleColumns.map(column => (
                  <th key={column} onClick={() => requestSort(column)}>
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                      <span>{column}</span>
                      {sortConfig.key === column ? (
                        sortConfig.direction === 'ascending' ? <ChevronUp className={styles.sortIcon} /> : <ChevronDown className={styles.sortIcon} />
                      ) : (
                        <ArrowUpDown className={styles.sortIcon} />
                      )}
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row, rowIndex) => (
                <tr key={rowIndex}>
                  {visibleColumns.map(column => (
                    <td key={column}>{row[column]}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className={styles.pagination}>
          <div className={styles.bottomButtons}>
            <button 
              onClick={() => onPageChange(currentPage - 1)}
              disabled={currentPage === 0}
            >
              Previous
            </button>
            <button 
              onClick={() => onPageChange(currentPage + 1)}
              disabled={currentPage >= totalPages - 1}
            >
              Next
            </button>
          </div>
          <div className={styles.paginationControls}>
            <span>Page {currentPage + 1} of {totalPages}</span>
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
    </div>
  );
};

export default DataTable;

