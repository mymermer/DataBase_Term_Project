import React from "react";
import Header from "../../components/Header";
import Footer from "../../components/Footer";
import styles from "../../styles/About.module.css";

export default function About() {
  return (
    <div className={styles.container}>
      <Header alwaysVisible={true} />
      <main className={styles.main}>
        <span style={{ display: "block", textAlign: "center" }}>
          <h1>About European Basketball Statistics</h1>
        </span>
        <p>
          Welcome to <strong>European Basketball Statistics</strong>, the
          ultimate hub for <em>data enthusiasts</em>, <em>basketball fans</em>,
          and <em>professionals</em>. Our platform is dedicated to delivering
          precise, comprehensive, and real-time statistics for two of the most
          prestigious basketball competitions in Europe: the <em>Euroleague</em>{" "}
          and the <em>Eurocup</em>.
        </p>
        <p>
          We pride ourselves on offering in-depth player profiles, team
          performance metrics, and historical data analysis, allowing users to
          gain a deeper understanding of the game. Whether you’re looking to
          analyze match outcomes, compare player performance, or follow your
          favorite team's progress, our platform ensures you have all the tools
          at your fingertips.
        </p>
        <p>
          Designed with a clean, user-friendly interface,{" "}
          <strong>European Basketball Statistics</strong> is perfect for fans
          seeking quick updates, analysts diving into advanced metrics, and
          industry professionals making data-driven decisions. Our mission is to
          connect you to the pulse of <em>European basketball</em>.
        </p>
        <p>
          Thank you for choosing <strong>European Basketball Statistics</strong>{" "}
          as your trusted source. Let’s celebrate the passion and excitement of
          European basketball together! 🏀
        </p>
        {/* QR Code Section */}
        <div className={styles.qrSection}>
          <p>Feel free to share our website with others!</p>
          <div className={styles.qrCodeContainer}>
            <img
              src="/qr-code.png"
              alt="QR Code for website"
              className={styles.qrCode}
            />
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
}
