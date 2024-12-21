import React from 'react';
import styles from '../styles/ErrorDisplay.module.css';

const ErrorDisplay = ({ message, onRetry }) => {
  return (
    <div className={styles.errorContainer}>
      <div className={styles.errorContent}>
        <h2 className={styles.errorTitle}>Oops! Something went wrong</h2>
        <p className={styles.errorMessage}>{message || 'There was an error fetching the data.'}</p>
        <p className={styles.errorHint}>This might be due to a network issue or the backend service being unavailable.</p>
        {onRetry && (
          <button className={styles.retryButton} onClick={onRetry}>
            Try Again
          </button>
        )}
      </div>
    </div>
  );
};

export default ErrorDisplay;

