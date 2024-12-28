import React, { useState, useEffect, useRef } from "react";
import styles from "../styles/LoadingOverlay.module.css";

const LoadingOverlay = ({ isLoading, tableWrapperRef }) => {
  const [position, setPosition] = useState({ top: "50%", left: "50%" });
  const overlayRef = useRef(null);

  useEffect(() => {
    const handleScroll = () => {
      if (!tableWrapperRef.current || !overlayRef.current) return;

      const tableRect = tableWrapperRef.current.getBoundingClientRect();
      const overlayRect = overlayRef.current.getBoundingClientRect();
      const viewportHeight = window.innerHeight;

      let top = "50%";
      if (tableRect.top > viewportHeight) {
        top = `${overlayRect.height / 2}px`;
      } else if (tableRect.bottom < 0) {
        top = `${viewportHeight - overlayRect.height / 2}px`;
      } else {
        const visibleTableHeight =
          Math.min(tableRect.bottom, viewportHeight) -
          Math.max(tableRect.top, 0);
        const centerY = Math.max(tableRect.top, 0) + visibleTableHeight / 2;
        top = `${centerY}px`;
      }

      setPosition({ top, left: "50%" });
    };

    window.addEventListener("scroll", handleScroll);
    handleScroll(); // Initial position

    return () => window.removeEventListener("scroll", handleScroll);
  }, [tableWrapperRef]);

  if (!isLoading) return null;

  return (
    <div className={styles.overlay} ref={overlayRef}>
      <div
        className={styles.spinner}
        style={{ top: position.top, left: position.left }}
      />
    </div>
  );
};

export default LoadingOverlay;
