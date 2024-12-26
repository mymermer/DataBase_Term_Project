import Link from "next/link";
import Image from "next/image";
import styles from "../styles/Header.module.css";
import NavButtons from "./NavButtons";

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
              src="/footer-logo.png"
              alt="Logo"
              width={30}
              height={30}
              className={styles.logo}
            />
            <h1 className={styles.headerTitle}>European Basketball Statistics</h1>
          </div>
        </Link>
        <NavButtons />
      </div>
    </header>
  );
}

