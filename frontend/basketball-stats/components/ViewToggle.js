import React from 'react';
import styles from '../styles/ViewToggle.module.css';

const ViewToggle = ({ isAdminView, onToggle }) => {
  return (
    <button className={styles.viewToggle} onClick={onToggle}>
      {isAdminView ? 'Switch to User View' : 'Switch to Admin View'}
    </button>
  );
};

export default ViewToggle;

