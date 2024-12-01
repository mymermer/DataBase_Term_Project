import Link from 'next/link';
import styles from '../styles/Header.module.css';

export default function Header({ onLogoClick, alwaysVisible }) {
  return (
    <header className={`${styles.header} ${alwaysVisible ? styles.alwaysVisible : ''}`}>
      <div className={styles.headerContent}>
        <Link href="/" onClick={onLogoClick} className={styles.homeLink}>
          <h1>European Basketball Statistics</h1>
        </Link>
      </div>
    </header>
  );
}

