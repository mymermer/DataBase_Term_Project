import React from 'react';
import styles from '../styles/LoadingSkeleton.module.css';

const LoadingSkeleton = ({ rows = 5, columns = 4 }) => {
  return (
    <div className={styles.loadingContainer}>
      {Array(rows).fill().map((_, rowIndex) => (
        <div key={rowIndex} className={styles.loadingRow}>
          {Array(columns).fill().map((_, colIndex) => (
            <div key={colIndex} className={styles.loadingCell}></div>
          ))}
        </div>
      ))}
    </div>
  );
};

export default LoadingSkeleton;

