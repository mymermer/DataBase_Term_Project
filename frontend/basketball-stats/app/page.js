'use client'

import { useState, useRef, useEffect } from 'react';
import Header from '../components/Header';
import LeagueSelectorButtons from '../components/LeagueSelectorButtons';
import StatOptionsGrid from '../components/StatOptionsGrid';
import Footer from '../components/Footer';
import styles from '../styles/HomePage.module.css';

export default function HomePage() {
  const [selectedLeague, setSelectedLeague] = useState(null);
  const [showHeader, setShowHeader] = useState(false);
  const statsRef = useRef(null);
  const titleRef = useRef(null);

  useEffect(() => {
    const handleScroll = () => {
      if (titleRef.current) {
        const rect = titleRef.current.getBoundingClientRect();
        setShowHeader(rect.top < 0);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleLeagueSelect = (league) => {
    setSelectedLeague(league);
    setTimeout(() => {
      statsRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
  };

  const resetSelection = () => {
    setSelectedLeague(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <div className={styles.container}>
      {showHeader && <Header onLogoClick={resetSelection} />}
      <main className={styles.main}>
        <div className={styles.topSection}>
          <div ref={titleRef} className={styles.titleSection}>
            <h1>European Basketball Statistics</h1>
          </div>
          <div className={styles.leagueSection}>
            <LeagueSelectorButtons onSelect={handleLeagueSelect} />
          </div>
        </div>
        <div ref={statsRef} className={styles.statsSection}>
          <StatOptionsGrid league={selectedLeague} />
        </div>
      </main>
      <Footer onLogoClick={resetSelection} />
    </div>
  );
}

