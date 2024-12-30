'use client';

import React, { useState, useEffect } from 'react';
import Image from 'next/image';
import styles from '../styles/PointsUserView.module.css';
import LoadingSkeleton from './LoadingSkeleton';
import ErrorDisplay from './ErrorDisplay';
import {
    Chart as ChartJS,
    ArcElement,
    Tooltip,
    Legend,
    Title
  } from 'chart.js';
import { Pie } from 'react-chartjs-2';  
ChartJS.register(ArcElement, Tooltip, Legend, Title);

const PointsUserView = ({ league }) => {
  const [selectedSeason, setSelectedSeason] = useState('');
  const [games, setGames] = useState([]);
  const [selectedGame, setSelectedGame] = useState(null); 
  const [playerPoints, setPlayerPoints] = useState([]);
  const [scoreAttempts, setScoreAttempts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [teamInfo, setTeamInfo] = useState({});
  const [showGameDropdown, setShowGameDropdown] = useState(false);
  const [currentGameTeams, setCurrentGameTeams] = useState({ team1: null});
  const [error, setError] = useState(null);

  const seasons = Array.from({ length: 2016 - 2007 + 1 }, (_, i) => 2007 + i);
  const tournament = league === "euroleague" ? "lig" : "cup";

  useEffect(() => {
    if (selectedSeason) {
      fetchGames();
    }
  }, [selectedSeason]);

  useEffect(() => {
    if (selectedGame) {
      updateCurrentGameTeams();
      fetchPlayerPercentages();  // Add this call
    }
  }, [selectedGame]);

  const fetchGames = async () => {
    setLoading(true);
    setError(null);
    const yearPrefix = tournament === 'cup' ? 'U' : 'E';
    const year = `${yearPrefix}${selectedSeason}`;
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/v1/${tournament}_players/${year}/teams`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const distinctTeams = await response.json();

      // Map the distinct teams into game-like objects to maintain compatibility
      const games = distinctTeams.map(team => ({ game: `${team}-${team}` }));

      setGames(games);

      // Fetch team info for these teams
      await fetchTeamInfo(distinctTeams);
    } catch (error) {
      setError('Unable to fetch teams data. Please try again later.');
      console.error('Error fetching games:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchPlayerPercentages = async () => {
    setLoading(true);
    setError(null);
    const yearPrefix = tournament === 'cup' ? 'U' : 'E';
    const year = `${yearPrefix}${selectedSeason}`;
    const team = selectedGame?.game.split('-')[0]; // Extract the team code
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/v1/${tournament}_players/${year}/${team}/player_percentages`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setPlayerPoints(data);
    } catch (error) {
      console.error('Error fetching player percentages:', error);
      setError('Unable to fetch percentages data. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const renderPieChart = () => {
    if (!playerPoints.length) return <p>No data available for this team.</p>;
    
      // Define a custom color palette (feel free to adjust these colors)
    
    const data = {
      labels: playerPoints.map(player => player.player_name),
      datasets: [
        {
          label: 'Player Point Percentages',
          data: playerPoints.map(player => parseFloat(player.point_percentage) * 100),
          backgroundColor: playerPoints.map((_, i) =>
            `hsl(${(i * 280) / playerPoints.length + 20}, 75%, 50%)`
          ),
        },
      ],
    };
  
    const options = {
      responsive: true,
      maintainAspectRatio: true,
      plugins: {
        legend: {
          position: 'right',
          labels: {
            font: {
              size: 16,
              weight: 'bold'
            },
            padding: 25 
          }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              return `${context.formattedValue}%`;
            }
          },
          titleFont: {
            size: 18
          },
          bodyFont: {
            size: 16
          }
        },
        // (Optional) Add a title if you wish:
        title: {
            
            display: true,
            text: 'Player Points Percentages',
            align: 'right', 
            font: { size: 45, weight: 'bold' },
            padding: { bottom: 20 },
        },
      }
    };
  
    return (
      <div className="flex justify-center items-center" style={{ display: 'flex', justifyContent: 'center', width: '100%', maxWidth: '1000px', height: '800px', margin: '0 auto' }}>
        <Pie data={data} options={options} />
      </div>
    );
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
      const [team1] = selectedGame.game.split('-'); 
      setCurrentGameTeams({
        team1: teamInfo[team1] || { fullName: team1, logoUrl: '/teams_icons/default_team_icon.png' },
      });
    }
  };

  const renderGameOptions = () => {
    const uniqueTeams = Array.from(
      new Set(games.flatMap((game) => game.game.split('-')))
    );
    return uniqueTeams.map((team) => (
      <div
        key={team}
        className={`${styles.gameOption} ${
          selectedGame?.game.includes(team) ? styles.selectedGameOption : ''
        }`}
        onClick={() => {
          const matchingGame = games.find((game) =>
            game.game.includes(team)
          );
          setSelectedGame(matchingGame || null);
          setShowGameDropdown(false);
        }}
      >
        <div className={`${styles.teamInfo} ${styles.singleTeam}`}>
          <Image 
            src={teamInfo[team]?.logoUrl || '/teams_icons/default_team_icon.png'} 
            alt={`${teamInfo[team]?.fullName || team} logo`} 
            width={30} 
            height={30} 
            className={styles.teamLogo}
          />
          <span className={styles.teamName}>
            {teamInfo[team]?.fullName || team}
          </span>
        </div>
      </div>
    ));
  };

  return (
    <div className={styles.containerWrapper}>
      <div className={styles.container}>
        <div className={styles.initialView}>
          {!selectedGame && <h2>Select a Team and Season to View Player Points Contribution</h2>}
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
                      <span className={styles.teamName}>
                        {currentGameTeams.team1?.fullName || 'Team'}
                      </span>
                    </div>
                  </>
                ) : (
                  <span>Select a team</span>
                )}
              </div>
              <span className={styles.selectLabel}>Team</span>
              {showGameDropdown && (
                <div className={styles.gameDropdown}>
                  {renderGameOptions()}
                </div>
              )}
            </div>
          </div>
        </div>
        {error && <ErrorDisplay message={error} onRetry={fetchGames} />}
        {selectedGame && (
          <>
            {loading ? (
              <LoadingSkeleton rows={5} columns={3} />
            ) : (
                <div className={styles.chartContainer}>
                {renderPieChart()}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default PointsUserView;

``
