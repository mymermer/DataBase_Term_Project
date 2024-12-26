'use client'

import React, { useState, useEffect } from 'react';
import Image from 'next/image';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Radar } from 'react-chartjs-2';
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip as ChartTooltip, Legend } from 'chart.js';
import styles from '../styles/TeamsUserView.module.css';
import LoadingSkeleton from './LoadingSkeleton';
import ErrorDisplay from './ErrorDisplay';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, ChartTooltip, Legend);

const TeamsUserView = ({ league }) => {
  const [selectedSeason, setSelectedSeason] = useState('');
  const [teamsData, setTeamsData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [teamInfo, setTeamInfo] = useState({});
  const [performanceData, setPerformanceData] = useState({});
  const [averageValues, setAverageValues] = useState({});

  const seasons = Array.from({ length: 2017 - 2007 + 1 }, (_, i) => 2007 + i);
  const tournament = league === "euroleague" ? "lig" : "cup";

  useEffect(() => {
    if (selectedSeason) {
      fetchTeamsData();
    }
  }, [selectedSeason]);

  const fetchTeamsData = async () => {
    setLoading(true);
    setError(null);
    const yearPrefix = tournament === 'cup' ? 'U' : 'E';
    const year = `${yearPrefix}${selectedSeason}`;
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/v1/${tournament}_teams/with_year_like?likePattern=${year}&sortBy=points&order=desc`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
    
      // Filter out duplicate team entries
      const uniqueTeamsData = data.reduce((acc, current) => {
        const x = acc.find(item => item.season_team_id === current.season_team_id);
        if (!x) {
          return acc.concat([current]);
        } else {
          return acc;
        }
      }, []);

      setTeamsData(uniqueTeamsData.map(team => ({
        ...team,
        best_player: formatPlayerName(team.best_player)
      })));

      const teamAbbrs = uniqueTeamsData.map(team => team.season_team_id.split('_')[1]);
      await fetchTeamInfo(teamAbbrs);
      await fetchPerformanceData(teamAbbrs);
      await fetchAverageValues(selectedSeason);
    } catch (error) {
      console.error('Error fetching teams data:', error);
      setError('Unable to fetch teams data. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const formatPlayerName = (playerName) => {
    if (!playerName) return '';
    const [surname, firstName] = playerName.split(', ');
    return `${firstName} ${surname}`;
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
      setTeamInfo(teamInfoMap);
    } catch (error) {
      console.error('Error fetching team info:', error);
      setError('Unable to fetch score attempts. Please try again later.');
    }
  };

  const fetchPerformanceData = async (teamAbbrs) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/v1/${tournament}_teams/by_team_abbrs?teamAbbrs=${teamAbbrs.join(',')}&columns=season_team_id,valuation_per_game`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setPerformanceData(data);
    } catch (error) {
      console.error('Error fetching performance data:', error);
    }
  };

  const fetchAverageValues = async (year) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/v1/${tournament}_teams/average-values/${year}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setAverageValues(data.averages);
    } catch (error) {
      console.error('Error fetching average values:', error);
    }
  };

  const renderPerformanceChart = (teamAbbr) => {
    const teamData = performanceData[teamAbbr] || [];
    
    return (
      <div className={styles.performanceChart}>
        <h4>Performance Progress</h4>
        <ResponsiveContainer width="100%" height={200}>
          <LineChart data={teamData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="year" />
            <YAxis />
            <Tooltip formatter={(value, name) => [value, 'Value per Game']} />
            <Line type="monotone" dataKey="valuation_per_game" name="Value per Game" stroke="#8884d8" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    );
  };

  const renderSpiderChart = (team) => {
    const stats = [
      { name: 'Rebounds', value: team.total_rebounds_per_game, avg: averageValues.total_rebounds_per_game },
      { name: 'Assists', value: team.assists_per_game, avg: averageValues.assists_per_game },
      { name: 'Steals', value: team.steals_per_game, avg: averageValues.steals_per_game },
      { name: 'Blocks', value: team.blocks_favour_per_game, avg: averageValues.blocks_favour_per_game },
    ];

    const scaledData = stats.map(stat => ({
      ...stat,
      scaledValue: (stat.value / stat.avg) * 100
    }));

    const data = {
      labels: scaledData.map(stat => stat.name),
      datasets: [
        {
          label: 'Team',
          data: scaledData.map(stat => stat.scaledValue),
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1,
        },
      ],
    };

    const options = {
      scales: {
        r: {
          angleLines: {
            display: false
          },
          suggestedMin: 0,
          suggestedMax: 200,
          ticks: {
            stepSize: 50,
            callback: (value) => value === 100 ? 'Avg' : ''
          }
        }
      },
      plugins: {
        legend: { display: false },
        tooltip: { enabled: false },
      },
      pointLabels: {
        font: { size: 12 },
        callback: (label, index) => {
          return `${label}: ${scaledData[index].value.toFixed(2)}`;
        },
      },
    };

    return (
      <div className={styles.spiderChartWrapper}>
        <h4>Team Stats vs League Average</h4>
        <div className={styles.spiderChart}>
          <Radar data={data} options={options} />
        </div>
      </div>
    );
  };

  if (!selectedSeason) {
    return (
      <div className={styles.initialView}>
        <h2>Select a season to see team information</h2>
        <select 
          value={selectedSeason} 
          onChange={(e) => setSelectedSeason(e.target.value)}
          className={styles.selectTrigger}
        >
          <option value="">Select Season</option>
          {seasons.map(season => (
            <option key={season} value={season.toString()}>
              {season}-{season + 1}
            </option>
          ))}
        </select>
      </div>
    );
  }

  return (
    <div className={styles.containerWrapper}>
      <div className={styles.container}>
        <div className={styles.seasonSelector}>
          <label htmlFor="seasonSelect" className={styles.seasonLabel}>Season</label>
          <select 
            id="seasonSelect"
            value={selectedSeason} 
            onChange={(e) => setSelectedSeason(e.target.value)}
            className={styles.selectTrigger}
          >
            <option value="">Select Season</option>
            {seasons.map(season => (
              <option key={season} value={season.toString()}>
                {season}-{season + 1}
              </option>
            ))}
          </select>
        </div>
        <div className={styles.teamsGrid}>
          {error ? (
            <ErrorDisplay message={error} onRetry={fetchTeamsData} />
          ) : loading ? (
            <LoadingSkeleton rows={5} columns={4} />
          ) : teamsData.length > 0 ? (
            teamsData.map((team) => {
              const teamAbbr = team.season_team_id.split('_')[1];
              return (
                <div key={team.season_team_id} className={`${styles.teamCard} ${styles.fadeIn}`}>
                  <div className={styles.teamContent}>
                    <div className={styles.teamInfo}>
                      <div className={styles.teamLogo}>
                        <Image
                          src={teamInfo[teamAbbr]?.logoUrl || '/teams_icons/default_team_icon.png'}
                          alt={teamInfo[teamAbbr]?.fullName || 'Team Logo'}
                          width={60}
                          height={60}
                          objectFit="contain"
                        />
                      </div>
                      <div className={styles.teamDetails}>
                        <h3 className={styles.teamName}>
                          {teamInfo[teamAbbr]?.fullName || teamAbbr}
                        </h3>
                        <div className={styles.teamStats}>
                          <div className={styles.statItem}>
                            <span className={styles.statLabel}>Games</span>
                            <span className={styles.statValue}>{team.games_played}</span>
                          </div>
                          <div className={styles.statItem}>
                            <span className={styles.statLabel}>Points</span>
                            <span className={styles.statValue}>{team.points}</span>
                          </div>
                          <div className={styles.statItem}>
                            <span className={styles.statLabel}>Minutes</span>
                            <span className={styles.statValue}>{team.minutes_played}</span>
                          </div>
                          <div className={styles.statItem}>
                            <span className={styles.statLabel}>Valuation</span>
                            <span className={styles.statValue}>{team.valuation}</span>
                          </div>
                        </div>
                        <div className={styles.bestPlayer}>
                          <span className={styles.bestPlayerLabel}>Best Player:</span>
                          <span className={styles.bestPlayerName}>{team.best_player}</span>
                        </div>
                      </div>
                    </div>
                    <div className={styles.charts}>
                      {renderPerformanceChart(teamAbbr)}
                      {renderSpiderChart(team)}
                    </div>
                  </div>
                </div>
              );
            })
          ) : (
            <div className={styles.noDataMessage}>No team data available</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TeamsUserView;

