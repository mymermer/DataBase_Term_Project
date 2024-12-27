import React from "react";
import Header from "../../components/Header";
import Footer from "../../components/Footer";
import styles from "../../styles/Contact.module.css";

export default function Contact() {
  const teamMembers = [
    {
      name: (
        <>
          Mohamed Ahmed Abdelsattar <br /> Mahmoud
        </>
      ),
      studentId: "150210926",
      email: "mahmoud21@itu.edu.tr",
    },
    {
      name: (
        <>
          Muhammed Yusuf <br /> Mermer
        </>
      ),
      studentId: "150220762",
      email: "mermer22@itu.edu.tr",
    },
    {
      name: (
        <>
          MHD Kamal <br /> Rushdi
        </>
      ),
      studentId: "150210907",
      email: "rushdi21@itu.edu.tr",
    },
    {
      name: (
        <>
          Muhammed Can <br /> Özkurt
        </>
      ),
      studentId: "820220710",
      email: "ozkurtm22@itu.edu.tr",
    },
  ];

  return (
    <div className={styles.container}>
      <Header alwaysVisible={true} />
      <main className={styles.main}>
        <h1>Contact KickStats Team</h1>
        <div className={styles.cardContainer}>
          {teamMembers.map((member, index) => (
            <div key={index} className={styles.card}>
              <div className={styles.avatar}>
                {/* Simple shape of a person */}
                <img
                  src="/person_icon.png"
                  alt="Person"
                  style={{
                    filter:
                      "brightness(0) saturate(100%) invert(20%) sepia(5%) saturate(50%) hue-rotate(0deg) brightness(60%) contrast(80%)",
                  }}
                />
              </div>
              <div className={styles.info}>
                <h2>{member.name}</h2>
                <p>
                  <strong>Student ID:</strong> {member.studentId}
                </p>
                <p>
                  <strong>Email:</strong>{" "}
                  <a href={`mailto:${member.email}`}>{member.email}</a>
                </p>
              </div>
            </div>
          ))}
        </div>
        {/* New Section */}
        <div className={styles.contactText}>
          <h2>Feel free to contact us!</h2>
          <p>
            Whether you have questions, suggestions, or need assistance, we’re
            here to help. Reach out to any of our team members via the provided
            contact details, and we’ll respond as soon as possible.
          </p>
        </div>
      </main>
      <Footer />
    </div>
  );
}
