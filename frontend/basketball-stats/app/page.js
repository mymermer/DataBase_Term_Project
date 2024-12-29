"use client";

import { useState, useRef, useEffect } from "react";
import Header from "../components/Header";
import LeagueSelectorButtons from "../components/LeagueSelectorButtons";
import StatOptionsGrid from "../components/StatOptionsGrid";
import DynamicText from "../components/DynamicText";
import Footer from "../components/Footer";
import styles from "../styles/HomePage.module.css";
import LoadingOverlay from "../components/LoadingOverlay";

export default function HomePage() {
  const [selectedLeague, setSelectedLeague] = useState(null);
  const [showHeader, setShowHeader] = useState(false);
  const statsRef = useRef(null);
  const titleRef = useRef(null);
  const [isLoading, setIsLoading] = useState(false);
  const mainContentRef = useRef(null);

  useEffect(() => {
    if ("scrollRestoration" in history) {
      history.scrollRestoration = "manual";
    }
    window.scrollTo({ top: 0, behavior: "smooth" });
    return () => {
      history.scrollRestoration = "auto";
    };
  }, []);

  useEffect(() => {
    const handleScroll = () => {
      if (titleRef.current) {
        const rect = titleRef.current.getBoundingClientRect();
        setShowHeader(rect.top < 0);
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  useEffect(() => {
    const handlePopState = () => {
      setSelectedLeague(null);
      window.scrollTo({ top: 0, behavior: "smooth" });
    };

    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  const handleLeagueSelect = (league) => {
    setSelectedLeague(league);
    setTimeout(() => {
      statsRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 100);
  };

  const resetSelection = () => {
    setSelectedLeague(null);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const fetchData = async () => {
    setIsLoading(true);
    try {
      // Perform data fetch or other operations
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <LoadingOverlay isLoading={isLoading} tableWrapperRef={mainContentRef} />
      {showHeader && <Header onLogoClick={resetSelection} />}
      <main className={styles.main} ref={mainContentRef}>
        <div className={styles.topSection}>
          <div ref={titleRef} className={styles.titleSection}>
            <h1>European Basketball Statistics</h1>
          </div>
          <div className={styles.leagueSection}>
            <LeagueSelectorButtons onSelect={handleLeagueSelect} />
            <p className={styles.selectPrompt}>Select a tournament to start...</p>
          </div>
        </div>
        <div ref={statsRef} className={styles.statsSection}>
          <DynamicText />
          <StatOptionsGrid league={selectedLeague} />
        </div>
      </main>
      <Footer onLogoClick={resetSelection} />
    </div>
  );
}
