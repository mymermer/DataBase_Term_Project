import Link from 'next/link';
import Image from 'next/image';
import styles from '../styles/Footer.module.css';

const leagues = ['euroleague', 'eurocup'];
const stats = ['points', 'teams', 'comparison', 'header', 'play_by_play', 'box_score', 'players'];

export default function Footer({ onLogoClick }) {
  return (
    <footer className={styles.footer}>
      <div className={styles.footerContent}>
        <div className={styles.linksSection}>
          {leagues.map(league => (
            <div key={league} className={styles.leagueSection}>
              <h2>{league.charAt(0).toUpperCase() + league.slice(1)}</h2>
              <ul>
                {stats.map(stat => (
                  <li key={`${league}-${stat}`}>
                    <Link href={`/${league}/${stat}`}>
                      {stat
                        .replace(/_/g, ' ')
                        .split(' ')
                        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
                        .join(' ')}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
        <div className={styles.logoSection}>
          <Link href="/" onClick={onLogoClick}>
            <Image 
              src="/footer-logo.png" 
              alt="European Basketball Statistics Logo" 
              width={150} 
              height={150}
            />
          </Link>
        </div>
      </div>
      <div className={styles.footerCredits}>
        <p>© 2024 KickStats. All Rights Reserved.</p>
      </div>
    </footer>
  );
}
