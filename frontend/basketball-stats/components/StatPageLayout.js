import Header from './Header';
import Footer from './Footer';
import styles from '../styles/StatPageLayout.module.css';

export default function StatPageLayout({ children, onLogoClick }) {
  return (
    <div className={styles.container}>
      <Header onLogoClick={onLogoClick} alwaysVisible={true} />
      <main className={styles.main}>
        {children}
      </main>
      <Footer onLogoClick={onLogoClick} />
    </div>
  );
}

