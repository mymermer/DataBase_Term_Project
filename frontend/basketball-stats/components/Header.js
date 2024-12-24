import Link from "next/link";
import Image from "next/image";
import styles from "../styles/Header.module.css";
import { FaHome, FaInfoCircle, FaEnvelope } from "react-icons/fa";

export default function Header({ onLogoClick, alwaysVisible }) {
  return (
    <header
      className={`${styles.header} ${
        alwaysVisible ? styles.alwaysVisible : ""
      }`}
    >
      <div className={styles.headerContent}>
        <Link href="/" onClick={onLogoClick} className={styles.homeLink}>
          <div className={styles.logoWrapper}>
            <Image
              src="/footer-logo.png" // Path to your logo file
              alt="Logo"
              width={40} // Adjust width
              height={40} // Adjust height
              className={styles.logo}
            />
            <h1>European Basketball Statistics</h1>
          </div>
        </Link>
        <nav className={styles.nav}>
          <ul>
            <li>
              <Link href="/" className={styles.navLink}>
                <FaHome className={styles.navIcon} /> Home
              </Link>
            </li>
            <li>
              <Link href="/about" className={styles.navLink}>
                <FaInfoCircle className={styles.navIcon} /> About
              </Link>
            </li>
            <li>
              <Link href="/contact" className={styles.navLink}>
                <FaEnvelope className={styles.navIcon} /> Contact
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
}
