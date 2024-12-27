import React from "react";
import Header from "../../components/Header";
import Footer from "../../components/Footer";
import styles from "../../styles/About.module.css";

export default function Contact() {
  return (
    <div className={styles.container}>
      <Header alwaysVisible={true} />
      <main className={styles.main}>
        <h1>Contact Us</h1>
        <p>
          We'd love to hear from you! If you have any questions, feedback, or
          inquiries about European Basketball Statistics, please don't hesitate
          to reach out.
        </p>
        <div className={styles.contactInfo}>
          <p>
            <strong>Email:</strong> info@eurobasketstats.com
          </p>
          <p>
            <strong>Phone:</strong> +1 (555) 123-4567
          </p>
          <p>
            <strong>Address:</strong> 123 Basketball Avenue, Sports City, EU
            12345
          </p>
        </div>
        <form className={styles.contactForm}>
          <input type="text" placeholder="Your Name" required />
          <input type="email" placeholder="Your Email" required />
          <textarea placeholder="Your Message" required></textarea>
          <button type="submit">Send Message</button>
        </form>
      </main>
      <Footer />
    </div>
  );
}
