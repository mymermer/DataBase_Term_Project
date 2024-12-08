'use client'

import React, { useEffect, useState } from 'react';
import StatPageTemplate from '../../../components/StatPageTemplate';
import DataTable from '../../../components/DataTable';
import styles from '../../../styles/PointsPage.module.css';

// Define columns first
const columns = [
  'Player', 'Team', 'Jersey Number', 'Round of Game', 'Phase','Is Starter?', 'Is Playing',
   'Offensive Rebounds','Defensive Rebounds','Assists','Steals','Turnovers','Blocks Favour',
   'Blocks Against','Fouls Committed','Fouls Received','Total Rebounds','Games Played', 'Minutes Per Game', 
  'Field Goals Made', 'Field Goals Attempted', 'Field Goal Percentage',
  'Three Pointers Made', 'Three Pointers Attempted', 'Three Point Percentage',
  'Free Throws Made', 'Free Throws Attempted', 'Free Throw Percentage',
  'Points Per Game', 'Total Points'
];

// More generative dummy data
const generateDummyData = (rowCount) => {
  const data = [];

  for (let i = 0; i < rowCount; i++) {
    const row = {};
    row['Player'] = `Player ${i + 1}`;
    row['Team'] = `Team ${Math.floor(i / 5) + 1}`;
    row['Jersey Number'] = Math.floor(Math.random() * 30) + 20;
    row['Quarter'] = `Quarter ${Math.floor(Math.random() * 4) + 1}`;
    row['Games Played'] = Math.floor(Math.random() * 100);
    row['Minutes Per Game'] = (Math.random() * 20 + 20).toFixed(1);
    row['Field Goals Made'] = Math.floor(Math.random() * 10) + 2;
    row['Field Goals Attempted'] = row['Field Goals Made'] + Math.floor(Math.random() * 10) + 5;
    row['Field Goal Percentage'] = (row['Field Goals Made'] / row['Field Goals Attempted'] * 100).toFixed(1) + '%';
    row['Three Pointers Made'] = Math.floor(Math.random() * 5);
    row['Three Pointers Attempted'] = row['Three Pointers Made'] + Math.floor(Math.random() * 5) + 2;
    row['Three Point Percentage'] = (row['Three Pointers Made'] / row['Three Pointers Attempted'] * 100).toFixed(1) + '%';
    row['Free Throws Made'] = Math.floor(Math.random() * 8) + 1;
    row['Free Throws Attempted'] = row['Free Throws Made'] + Math.floor(Math.random() * 4);
    row['Free Throw Percentage'] = (row['Free Throws Made'] / row['Free Throws Attempted'] * 100).toFixed(1) + '%';
    row['Points Per Game'] = ((row['Field Goals Made'] * 2 + row['Three Pointers Made'] + row['Free Throws Made']) / row['Games Played']).toFixed(1);
    row['Total Points'] = (row['Points Per Game'] * row['Games Played']).toFixed(0);
    data.push(row);
  }

  return data;
};

const data = generateDummyData(100);

export default function PointsPage({ params }) {
  const { league } = React.use(params);

  return (
    <StatPageTemplate league={league} stat="Points">
      <div className={styles.pointsPageContent}>
        <h2>{league.charAt(0).toUpperCase() + league.slice(1)} Points Statistics</h2>
        <DataTable initialData={data} initialColumns={columns} />
      </div>
    </StatPageTemplate>
  );
}



