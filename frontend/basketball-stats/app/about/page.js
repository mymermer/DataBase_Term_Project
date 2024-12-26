import React from 'react';
import Header from '../../components/Header';
import Footer from '../../components/Footer';
import styles from '../../styles/About.module.css';

export default function About() {
  return (
    <div className={styles.container}>
      <Header alwaysVisible={true} />
      <main className={styles.main}>
        <h1>About European Basketball Statistics</h1>
        <p>
          European Basketball Statistics is your go-to resource for comprehensive data and analysis on European basketball leagues. Our platform provides in-depth statistics, player profiles, and team performance metrics for the Euroleague and Eurocup.
        </p>
        <p>
          Whether you're a fan, analyst, or industry professional, our user-friendly interface and detailed insights will help you stay informed about the exciting world of European basketball.
        </p>
      </main>
      <Footer />
    </div>
  );
}

