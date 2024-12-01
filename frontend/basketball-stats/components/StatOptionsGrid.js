import Link from 'next/link';
import styles from '../styles/StatOptionsGrid.module.css';

const statOptions = [
  { id: 'POINTS', icon: '📊' },
  { id: 'TEAMS', icon: '👥' },
  { id: 'COMPARISON', icon: '⚖️' },
  { id: 'HEADER', icon: '📋' },
  { id: 'PLAY_BY_PLAY', icon: '▶️' },
  { id: 'BOX_SCORE', icon: '📦' },
  { id: 'PLAYERS', icon: '🏃' }
];

export default function StatOptionsGrid({ league }) {
  return (
    <div className={styles.statOptionsContainer}>
      <div className={styles.optionsGrid}>
        {statOptions.map((option) => (
          <Link 
            key={option.id} 
            href={league ? `/${league}/${option.id.toLowerCase()}` : '#'}
            className={`${styles.optionCard} ${!league ? styles.disabled : ''}`}
            onClick={(e) => !league && e.preventDefault()}
          >
            <span className={styles.icon}>{option.icon}</span>
            <span className={styles.label}>{option.id.replace('_', ' ')}</span>
          </Link>
        ))}
      </div>
    </div>
  );
}

