'use client'

import { useRouter } from 'next/navigation';
import StatPageLayout from './StatPageLayout';
import styles from '../styles/StatPageTemplate.module.css';

export default function StatPageTemplate({ league, stat, children }) {
  const router = useRouter();

  const onLogoClick = () => {
    router.push('/');
  };

  return (
    <StatPageLayout onLogoClick={onLogoClick}>
      <div className={styles.content}>
        <h1>{league.charAt(0).toUpperCase() + league.slice(1)} - {stat}</h1>
        {children}
      </div>
    </StatPageLayout>
  );
}

