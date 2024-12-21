'use client';

import React, { useState, useEffect } from 'react';
import styles from '../styles/DynamicText.module.css';

const words = ['learn', 'compare', 'see'];

export default function DynamicText() {
  const [currentWord, setCurrentWord] = useState(0);
  const [isChanging, setIsChanging] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setIsChanging(true);
      setTimeout(() => {
        setCurrentWord((prev) => (prev + 1) % words.length);
        setIsChanging(false);
      }, 500);
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <h2 className={styles.dynamicText}>
      What do you want to{' '}
      <span className={`${styles.changingWord} ${isChanging ? styles.changing : ''}`}>
        {words[currentWord]}
      </span>?
    </h2>
  );
}

