import React from "react";
import styles from "../styles/LoadingOverlay.module.css";

const LoadingOverlayGeneral = ({ isLoading }) => {
  // Simply render the overlay and spinner without any dependency on `tableWrapperRef`
  if (!isLoading) return null;

  return (
    <div className={styles.overlay}>
      <div className={styles.spinner} />
    </div>
  );
};

export default LoadingOverlayGeneral;
