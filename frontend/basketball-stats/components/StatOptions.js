import styles from '../styles/StatOptions.module.css';

const statOptions = [
  { id: 'POINTS', icon: '📊' },
  { id: 'TEAMS', icon: '👥' },
  { id: 'COMPARISON', icon: '⚖️' },
  { id: 'HEADER', icon: '📋' },
  { id: 'PLAY_BY_PLAY', icon: '▶️' },
  { id: 'BOX_SCORE', icon: '📦' },
  { id: 'PLAYERS', icon: '🏃' }
];

export default function StatOptions({ league }) {
  return (
    <div className={styles.statOptions}>
      <div className={styles.optionsGrid}>
        {statOptions.map((option, index) => (
          <div 
            key={option.id} 
            className={`${styles.optionCard} ${!league ? styles.disabled : ''} ${
              index === statOptions.length - 1 ? styles.lastCard : ''
            }`}
          >
            <span className={styles.icon}>{option.icon}</span>
            <span className={styles.label}>{option.id.replace('_', ' ')}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

