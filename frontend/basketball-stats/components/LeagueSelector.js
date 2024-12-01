import styles from '../styles/LeagueSelector.module.css';

export default function LeagueSelector({ onSelect }) {
  return (
    <div className={styles.leagueSelector}>
      <div className={styles.buttonContainer}>
        <button 
          onClick={() => onSelect('euroleague')} 
          className={styles.leagueButton}
          style={{ backgroundImage: 'url(/placeholder-euroleague.jpg)' }}
        >
          <div className={styles.buttonOverlay}>
            <span>Euroleague</span>
          </div>
        </button>
        <button 
          onClick={() => onSelect('eurocup')} 
          className={styles.leagueButton}
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

