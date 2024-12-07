'use client'

import React, { useState, useEffect } from 'react';
import Image from 'next/image';
import styles from '../styles/PointsUserView.module.css';

const PointsUserView = ({ league }) => {
  const [selectedSeason, setSelectedSeason] = useState('');
  const [games, setGames] = useState([]);
  const [selectedGame, setSelectedGame] = useState('');
  const [scoreAttempts, setScoreAttempts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [offset, setOffset] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(25);

  const seasons = Array.from({ length: 2023 - 2007 + 1 }, (_, i) => 2007 + i);
  const tournament = league === "euroleague" ? "lig" : "cup";

  useEffect(() => {
    if (selectedSeason) {
      fetchGames();
    }
  }, [selectedSeason]);

  useEffect(() => {
    if (selectedGame) {
      fetchScoreAttempts();
    }
  }, [selectedGame, offset, rowsPerPage]);

  const fetchGames = async () => {
    setLoading(true);
    const yearPrefix = tournament === 'cup' ? 'U' : 'e';
    const year = `${yearPrefix}${selectedSeason}`;
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/v1/${tournament}_points/year_distinct_games?likePattern=${year}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setGames(data);
    } catch (error) {
      console.error('Error fetching games:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchScoreAttempts = async () => {
    setLoading(true);
    const yearPrefix = tournament === 'cup' ? 'U' : 'E';
    const year = `${yearPrefix}${selectedSeason}`;
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/v1/${tournament}_points/with_year_like?likePattern=${year}%&offset=${offset}&limit=${rowsPerPage}&columns=game_point_id,points,coord_x,coord_y,season_team_id,player,action_of_play,points_a,points_b,game,minute&filters=game:${selectedGame}&sortBy=minute&order=asc`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setScoreAttempts(data);
    } catch (error) {
      console.error('Error fetching score attempts:', error);
    } finally {
      setLoading(false);
    }
  };

  const getTeamCode = (seasonTeamId) => {
    return seasonTeamId.split('_')[1];
  };

  const formatPlayerName = (playerName) => {
    const [surname, name] = playerName.split(', ');
    return `${name} ${surname}`;
  };

  const handlePrevious = () => {
    if (offset >= rowsPerPage) {
      setOffset(offset - rowsPerPage);
    }
  };

  const handleNext = () => {
    setOffset(offset + rowsPerPage);
  };

  return (
    <div className={styles.container}>
      {!selectedGame ? (
        <div className={styles.initialView}>
          <h2>Select a competition to see score changes</h2>
          <div className={styles.selectors}>
            <div className={styles.selectWrapper}>
              <select 
                value={selectedSeason} 
                onChange={(e) => setSelectedSeason(e.target.value)}
                className={selectedSeason ? styles.filled : ''}
              >
                <option value="">Season</option>
                {seasons.map(season => (
                  <option key={season} value={season}>{season}-{season + 1}</option>
                ))}
              </select>
              <span className={styles.selectLabel}>Season</span>
            </div>
            <div className={styles.selectWrapper}>
              <select 
                value={selectedGame} 
                onChange={(e) => setSelectedGame(e.target.value)} 
                disabled={!selectedSeason}
                className={selectedGame ? styles.filled : ''}
              >
                <option value="">Game</option>
                {games.map(game => (
                  <option key={game} value={game}>{game}</option>
                ))}
              </select>
              <span className={styles.selectLabel}>Game</span>
            </div>
          </div>
        </div>
      ) : (
        <>
          <div className={styles.topControls}>
            <div className={styles.selectWrapper}>
              <select 
                value={selectedSeason} 
                onChange={(e) => setSelectedSeason(e.target.value)}
                className={styles.filled}
              >
                <option value="">Season</option>
                {seasons.map(season => (
                  <option key={season} value={season}>{season}-{season + 1}</option>
                ))}
              </select>
              <span className={styles.selectLabel}>Season</span>
            </div>
            <div className={styles.selectWrapper}>
              <select 
                value={selectedGame} 
                onChange={(e) => setSelectedGame(e.target.value)}
                className={styles.filled}
              >
                <option value="">Game</option>
                {games.map(game => (
                  <option key={game} value={game}>{game}</option>
                ))}
              </select>
              <span className={styles.selectLabel}>Game</span>
            </div>
          </div>
          {loading && <p>Loading...</p>}
          <div className={styles.scoreAttempts}>
            {scoreAttempts.map((attempt, index) => {
              const [team1, team2] = attempt.game.split('-');
              const scoringTeam = attempt.points > 0 ? getTeamCode(attempt.season_team_id) : null;
              const isTeam1Scoring = scoringTeam === team1;
              return (
                <div key={attempt.game_point_id} className={styles.attemptBlock}>
                  <div className={styles.courtWrapper}>
                    <Image src="/basketball-court.png" alt="Basketball Court" width={300} height={150} />
                    <div 
                      className={styles.shotMarker} 
                      style={{ 
                        left: `${(1500 + attempt.coord_y) / 7000  * 300}px`, 
                        top: `${(950 + attempt.coord_x) / 1900 * 150}px` 
                      }}
                    />
                    <div className={styles.minuteDisplay}>{attempt.minute}'</div>
                  </div>
                  <div className={styles.attemptInfo}>
                    <div className={styles.teamInfo}>
                      <Image 
                        src={`/team-logos/${getTeamCode(attempt.season_team_id)}.png`} 
                        alt="Team Logo" 
                        width={60} 
                        height={60} 
                      />
                      <span className={styles.playerName}>{formatPlayerName(attempt.player)}</span>
                    </div>
                    <div className={styles.actionInfo}>
                      <span>{attempt.action_of_play}</span>
                      <span>
                        <span className={attempt.points > 0 && isTeam1Scoring ? styles.scoringTeam : ''}>
                          {attempt.points_a}
                        </span>
                        {' - '}
                        <span className={attempt.points > 0 && !isTeam1Scoring ? styles.scoringTeam : ''}>
                          {attempt.points_b}
                        </span>
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
          <div className={styles.paginationControls}>
            <button onClick={handlePrevious} disabled={offset === 0}>Previous</button>
            <select 
              value={rowsPerPage} 
              onChange={(e) => setRowsPerPage(Number(e.target.value))}
            >
              <option value={25}>25 rows</option>
              <option value={50}>50 rows</option>
              <option value={100}>100 rows</option>
            </select>
            <button onClick={handleNext}>Next</button>
          </div>
        </>
      )}
    </div>
  );
};

export default PointsUserView;

