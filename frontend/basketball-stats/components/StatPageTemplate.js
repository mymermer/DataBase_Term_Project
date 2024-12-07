'use client'

import { useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';
import Header from './Header';
import Footer from './Footer';
import ViewToggle from './ViewToggle';
import styles from '../styles/StatPageTemplate.module.css';

export default function StatPageTemplate({ league, stat, children, UserView }) {
  const router = useRouter();
  const [isAdminView, setIsAdminView] = useState(false);

  useEffect(() => {
    // Scroll to top on page load/reload
    window.scrollTo(0, 0);
  }, []);

  const onLogoClick = () => {
    router.push('/');
  };

  const toggleView = () => {
    setIsAdminView(!isAdminView);
  };

  return (
    <div className={styles.container}>
      <Header onLogoClick={onLogoClick} />
      <main className={styles.main}>
        <div className={styles.headerContainer}>
          <h1>{league.charAt(0).toUpperCase() + league.slice(1)} - {stat}</h1>
          <ViewToggle isAdminView={isAdminView} onToggle={toggleView} />
        </div>
        {isAdminView ? children : <UserView league={league} />}
      </main>
      <Footer onLogoClick={onLogoClick} />
    </div>
  );
}

