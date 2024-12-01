'use client'

import { useRouter } from 'next/navigation';
import StatPageLayout from './StatPageLayout';
import styles from '../styles/StatPageTemplate.module.css';

export default function StatPageTemplate({ league, stat }) {
  const router = useRouter();

  const onLogoClick = () => {
    router.push('/');
  };

  return (
    <StatPageLayout onLogoClick={onLogoClick}>
      <div className={styles.content}>
        <h1>{league.charAt(0).toUpperCase() + league.slice(1)} - {stat}</h1>
        <p>This page is not ready yet.</p>
        {/* TODO: Add content for the {stat} page in the {league} */}
        {/* 
          Possible content to add:
          - Data visualization (charts, graphs) related to the specific stat
          - Table with relevant data
          - Filters for selecting seasons, teams, or players
          - Comparison tools
          - Historical data and trends
        */}
      </div>
    </StatPageLayout>
  );
}

