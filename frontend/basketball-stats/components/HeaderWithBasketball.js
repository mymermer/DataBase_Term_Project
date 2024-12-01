import Link from 'next/link';
import styles from '../styles/HeaderWithBasketball.module.css';

export default function HeaderWithBasketball() {
  return (
    <header className={styles.header}>
      <div className={styles.headerContent}>
        <Link href="/" className={styles.homeLink}>
          <h1>European Basketball Statistics</h1>
        </Link>
        <div className={styles.basketballIconWrapper}>
          <img 
            src="/placeholder-basketball.png" 
            alt="Basketball" 
            className={styles.basketballIcon}
          />
        </div>
      </div>
    </header>
  );
}

