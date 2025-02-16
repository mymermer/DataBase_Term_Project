'use client'

import React, { useState, useEffect } from 'react';
import Image from 'next/image';
import styles from '../styles/PointsUserView.module.css';
import LoadingSkeleton from './LoadingSkeleton';
import ErrorDisplay from './ErrorDisplay';

const PointsUserView = ({ league }) => {
  const [selectedSeason, setSelectedSeason] = useState('');
  const [games, setGames] = useState([]);
  const [selectedGame, setSelectedGame] = useState('');
  const [gameselectedornot, Setgameselectedornot] = useState('');
  const [scoreAttempts, setScoreAttempts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [offset, setOffset] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(25);
  const [teamInfo, setTeamInfo] = useState({});
  const [showGameDropdown, setShowGameDropdown] = useState(false);
  const [currentGameTeams, setCurrentGameTeams] = useState({ team1: null, team2: null });
  const [error, setError] = useState(null);
  const [lastFetchedGame, setLastFetchedGame] = useState('');
  const [hasNextPage, setHasNextPage] = useState(true);
  const [showPaginationControls, setShowPaginationControls] = useState(false);

  const seasons = Array.from({ length: 2016 - 2007 + 1 }, (_, i) => 2007 + i);
  const tournament = league === "euroleague" ? "lig" : "cup";

  useEffect(() => {
    if (selectedSeason) {
      fetchGames();
      setSelectedGame('');
      setCurrentGameTeams({ team1: null, team2: null });
      setShowPaginationControls(false);
    }
  }, [selectedSeason]);

  useEffect(() => {
    if (selectedGame) {
      setOffset(0);
      setRowsPerPage(25);
      fetchScoreAttempts();
      updateCurrentGameTeams();
      setShowPaginationControls(true);
    }
  }, [selectedGame]);

  useEffect(() => {
    if (lastFetchedGame) {
      fetchScoreAttempts();
    }
  }, [offset, rowsPerPage]);

  const fetchGames = async () => {
    setLoading(true);
    setError(null);
    const yearPrefix = tournament === 'cup' ? 'U' : 'E';
    const year = `${yearPrefix}${selectedSeason}`;
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/v1/${tournament}_points/year_distinct_games?likePattern=${year}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setGames(data);

      const allTeams = new Set(data.flatMap(game => game.split('-')));
      await fetchTeamInfo(Array.from(allTeams));
    } catch (error) {
      setError('Unable to fetch teams data. Please try again later.');
      console.error('Error fetching games:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchScoreAttempts = async () => {
    setLoading(true);
    setError(null);
    const yearPrefix = tournament === 'cup' ? 'U' : 'E';
    const year = `${yearPrefix}${selectedSeason}`;
    const gameToFetch = selectedGame || lastFetchedGame;
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/v1/${tournament}_points/with_year_like?likePattern=${year}%&offset=${offset}&limit=${rowsPerPage + 1}&columns=game_point_id,points,coord_x,coord_y,season_team_id,player,action_of_play,points_a,points_b,game,minute&filters=game:${gameToFetch}&sortBy=minute&order=asc`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setHasNextPage(data.length > rowsPerPage);
      setScoreAttempts(data.slice(0, rowsPerPage));
      setLastFetchedGame(gameToFetch);
    } catch (error) {
      console.error('Error fetching score attempts:', error);
      setError('Unable to fetch teams data. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const fetchTeamInfo = async (abbreviations) => {
    setError(null);
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/v1/team?abbreviation=${abbreviations.join(',')}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      const teamInfoMap = {};
      data.forEach(team => {
        teamInfoMap[team.abbreviation] = {
          fullName: team.full_name,
          logoUrl: team.logo_url && team.logo_url.trim() !== '' 
            ? `/teams_icons${team.logo_url.trimEnd()}` 
            : '/teams_icons/default_team_icon.png'
        };
      });
      setTeamInfo(prevTeamInfo => ({...prevTeamInfo, ...teamInfoMap}));
    } catch (error) {
      console.error('Error fetching team info:', error);
      setError('Unable to fetch teams data. Please try again later.');
    }
  };

  const updateCurrentGameTeams = () => {
    if (selectedGame) {
      const [team1, team2] = selectedGame.split('-');
      setCurrentGameTeams({
        team1: teamInfo[team1] || { fullName: team1, logoUrl: '/teams_icons/default_team_icon.png' },
        team2: teamInfo[team2] || { fullName: team2, logoUrl: '/teams_icons/default_team_icon.png' }
      });
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
    if (hasNextPage) {
      setOffset(offset + rowsPerPage);
    }
  };

  const renderGameOptions = () => {
    return games.map(game => {
      const [team1, team2] = game.split('-');
      const fullName1 = teamInfo[team1]?.fullName || team1;
      const fullName2 = teamInfo[team2]?.fullName || team2;
      return (
        <div 
          key={game} 
          className={`${styles.gameOption} ${selectedGame === game ? styles.selectedGame : ''}`}
          onClick={() => {
            setSelectedGame(game);
            Setgameselectedornot(true);
            setShowGameDropdown(false);
          }}
        >
          <div className={styles.teamInfo}>
            <Image 
              src={teamInfo[team1]?.logoUrl || '/teams_icons/default_team_icon.png'} 
              alt={`${fullName1} logo`} 
              width={30} 
              height={30} 
              className={styles.teamLogo}
            />
            <span className={styles.teamName}>{fullName1}</span>
          </div>
          <span className={styles.vsText}>vs</span>
          <div className={`${styles.teamInfo} ${styles.rightTeam}`}>
            <span className={styles.teamName}>{fullName2}</span>
            <Image 
              src={teamInfo[team2]?.logoUrl || '/teams_icons/default_team_icon.png'} 
              alt={`${fullName2} logo`} 
              width={30} 
              height={30} 
              className={styles.teamLogo}
            />
          </div>
        </div>
      );
    });
  };

  const renderShotLine = (coordX, coordY, isSuccessful) => {
    // Adjust the coordinate system
    const startX = ((coordY+4100) / 20000) * 100; // Normalize to 0-100 range
    const startY = ((coordX + 750) / 1500) * 100; // Normalize to 0-100 range, invert Y-axis
    const endX = 0;
    const endY = 50; // Middle of the left side

    const lineColor = isSuccessful ? "rgb(20, 221, 20)" : "#FF5252";

    return (
      <svg className={styles.shotLine} viewBox="0 0 100 100" preserveAspectRatio="none">
        <line
          x1={`${startX}%`}
          y1={`${startY}%`}
          x2={`${endX}%`}
          y2={`${endY}%`}
          stroke={lineColor}
          strokeWidth="1"
          strokeDasharray="5,5"
          className={styles.animatedDash}
        />
      </svg>
    );
  };

  return (
    <div className={styles.containerWrapper}>
      <div className={styles.container}>
        <div className={styles.initialView}>
          {!gameselectedornot && <h2>Select a competition to see score changes</h2>}
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
            <div className={styles.customSelect}>
              <div 
                className={`${styles.selectedGame} ${selectedGame ? styles.filled : ''} ${!selectedSeason ? styles.disabledGame : ''}`}
                onClick={() => selectedSeason ? setShowGameDropdown(!showGameDropdown) : null}
              >
                {selectedGame ? (
                  <>
                    <div className={styles.teamInfo}>
                      <Image 
                        src={currentGameTeams.team1?.logoUrl || '/teams_icons/default_team_icon.png'} 
                        alt={`${currentGameTeams.team1?.fullName} logo`} 
                        width={30} 
                        height={30} 
                        className={styles.teamLogo}
                      />
                      <span className={styles.teamName}>{currentGameTeams.team1?.fullName}</span>
                    </div>
                    <span className={styles.vsText}>vs</span>
                    <div className={`${styles.teamInfo} ${styles.rightTeam}`}>
                      <span className={styles.teamName}>{currentGameTeams.team2?.fullName}</span>
                      <Image 
                        src={currentGameTeams.team2?.logoUrl || '/teams_icons/default_team_icon.png'} 
                        alt={`${currentGameTeams.team2?.fullName} logo`} 
                        width={30} 
                        height={30} 
                        className={styles.teamLogo}
                      />
                    </div>
                  </>
                ) : (
                  <span>Select a game</span>
                )}
              </div>
              <span className={styles.selectLabel}>Game</span>
              {showGameDropdown && (
                <div className={styles.gameDropdown}>
                  {renderGameOptions()}
                </div>
              )}
            </div>
          </div>
        </div>
        {error && <ErrorDisplay message={error} onRetry={fetchGames} />}
        {lastFetchedGame && (
          <>
            <div className={styles.scoreAttempts}>
              {scoreAttempts.map((attempt, index) => (
                <div key={attempt.game_point_id} className={`${styles.attemptBlock} ${styles.fadeIn}`}>
                  <div className={styles.courtWrapper}>
                    <Image src="/basketball-court.png" alt="Basketball Court" layout="fill" objectFit="contain" />
                    {renderShotLine(attempt.coord_x, attempt.coord_y, attempt.points > 0)}
                    <div 
                      className={`${styles.shotMarker} ${attempt.points > 0 ? styles.successfulShot : styles.unsuccessfulShot}`}
                      style={{ 
                        left: `${((attempt.coord_y+3750) / 18000) * 100}%`, 
                        top: `${((attempt.coord_x + 750) / 1500) * 100}%` 
                      }}
                    />
                    <div className={styles.minuteDisplay}>{attempt.minute}'</div>
                  </div>
                  <div className={styles.attemptInfo}>
                    <div className={styles.teamInfo}>
                      <Image 
                        src={teamInfo[getTeamCode(attempt.season_team_id)]?.logoUrl || '/teams_icons/default_team_icon.png'} 
                        alt="Team Logo" 
                        width={60} 
                        height={60} 
                        className={styles.teamLogo}
                      />
                      <span className={styles.playerName}>{formatPlayerName(attempt.player)}</span>
                    </div>
                    <div className={styles.actionInfo}>
                      <span>{attempt.action_of_play}</span>
                      <span>
                        <span className={attempt.points > 0 && getTeamCode(attempt.season_team_id) === attempt.game.split('-')[0] ? styles.scoringTeam : ''}>
                          {attempt.points_a}
                        </span>
                        {' - '}
                        <span className={attempt.points > 0 && getTeamCode(attempt.season_team_id) === attempt.game.split('-')[1] ? styles.scoringTeam : ''}>
                          {attempt.points_b}
                        </span>
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
            {showPaginationControls && (
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
                <button onClick={handleNext} disabled={!hasNextPage}>Next</button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default PointsUserView;

