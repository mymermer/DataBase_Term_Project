import styles from '../styles/StatOptions.module.css';

const statOptions = [
  { id: 'POINTS' },
  { id: 'TEAMS' },
  { id: 'COMPARISON' },
  { id: 'HEADER' },
  { id: 'PLAY_BY_PLAY' },
  { id: 'BOX_SCORE' },
  { id: 'PLAYERS'}
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

