import React from 'react';
import styles from '../styles/ViewToggle.module.css';
import {
  RefreshCcw
} from "lucide-react";

const ViewToggle = ({ isAdminView, onToggle }) => {
  return (
    <button className={styles.viewToggle} onClick={onToggle}>
      <RefreshCcw size={16} /> {isAdminView ? 'Switch to User View' : 'Switch to Admin View'}
    </button>
  );
};

export default ViewToggle;

