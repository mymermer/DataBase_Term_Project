import React, { useEffect, useState } from 'react';
import styles from '../styles/LeagueSelectorButtons.module.css';

export default function LeagueSelectorButtons({ onSelect }) {
  const [isInitialLoad, setIsInitialLoad] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsInitialLoad(false);
    }, 3000); // Increased to 3 seconds

    return () => clearTimeout(timer);
  }, []);

  return (
    <div className={styles.leagueSelector}>
      <div className={styles.buttonContainer}>
        <button 
          onClick={() => onSelect('euroleague')} 
          className={`${styles.leagueButton} ${isInitialLoad ? styles.initialLoad : ''}`}
          style={{ backgroundImage: 'url(/placeholder-euroleague.jpg)' }}
        >
          <div className={styles.buttonOverlay}>
            <span>Euroleague</span>
          </div>
        </button>
        <button 
          onClick={() => onSelect('eurocup')} 
          className={`${styles.leagueButton} ${isInitialLoad ? styles.initialLoad : ''}`}
          style={{ backgroundImage: 'url(/placeholder-eurocup.jpg)' }}
        >
          <div className={styles.buttonOverlay}>
            <span>Eurocup</span>
          </div>
        </button>
      </div>
    </div>
  );
}

