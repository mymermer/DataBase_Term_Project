import React from 'react';
import Link from 'next/link';
import styles from '../styles/NavButtons.module.css';

const NavButtons = () => {
  return (
    <nav className={styles.navButtons}>
      <Link href="/" className={styles.navButton}>
        Home
      </Link>
      <Link href="/about" className={styles.navButton}>
        About
      </Link>
      <Link href="/contact" className={styles.navButton}>
        Contact
      </Link>
    </nav>
  );
};

export default NavButtons;

