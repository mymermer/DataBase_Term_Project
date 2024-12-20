'use client'

import React, { useState, useEffect } from 'react';
import Image from 'next/image';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Radar } from 'react-chartjs-2';
import { Chart as ChartJS, RadialLinearScale, PointElement, LineElement, Filler, Tooltip as ChartTooltip, Legend } from 'chart.js';
import styles from '../styles/TeamsUserView.module.css';

ChartJS.register(RadialLinearScale, PointElement, LineElement, Filler, ChartTooltip, Legend);

const TeamsUserView = ({ league }) => {
  const [selectedSeason, setSelectedSeason] = useState('');
  const [teamsData, setTeamsData] = useState([]);
  const [loading, setLoading] = useState(false);
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
    const yearPrefix = tournament === 'cup' ? 'U' : 'E';
    const year = `${yearPrefix}${selectedSeason}`;
    try {
      const response = await fetch(`http://127.0.0.1:5000/api/v1/${tournament}_teams/with_year_like?likePattern=${year}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setTeamsData(data);

      // Fetch team info for all teams
      const teamAbbrs = data.map(team => team.season_team_id.split('_')[1]);
      await fetchTeamInfo(teamAbbrs);
      await fetchPerformanceData(teamAbbrs);
      await fetchAverageValues(selectedSeason);
    } catch (error) {
      console.error('Error fetching teams data:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchTeamInfo = async (abbreviations) => {
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
            <Tooltip />
            <Line type="monotone" dataKey="valuation_per_game" stroke="#8884d8" />
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

    const data = {
      labels: stats.map(stat => stat.name),
      datasets: [
        {
          label: 'Team',
          data: stats.map(stat => stat.value),
          backgroundColor: 'rgba(255, 99, 132, 0.2)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1,
        },
        {
          label: 'League Average',
          data: stats.map(stat => stat.avg),
          backgroundColor: 'rgba(54, 162, 235, 0.2)',
          borderColor: 'rgba(54, 162, 235, 1)',
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
          suggestedMax: Math.max(...stats.map(stat => Math.max(stat.value, stat.avg))) * 1.1
        }
      }
    };

    return (
      <div className={styles.spiderChart}>
        <h4>Team Stats vs League Average</h4>
        <Radar data={data} options={options} />
      </div>
    );
  };

  return (
    <div className={styles.containerWrapper}>
      <div className={styles.container}>
        <div className={styles.seasonSelector}>
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
        {loading && <p>Loading...</p>}
        <div className={styles.teamsGrid}>
          {teamsData.map((team) => {
            const teamAbbr = team.season_team_id.split('_')[1];
            return (
              <div key={team.season_team_id} className={styles.teamCard}>
                <div className={styles.teamHeader}>
                  <h3 className={styles.teamName}>
                    <Image
                      src={teamInfo[teamAbbr]?.logoUrl || '/teams_icons/default_team_icon.png'}
                      alt={teamInfo[teamAbbr]?.fullName || 'Team Logo'}
                      width={40}
                      height={40}
                      className={styles.teamLogo}
                    />
                    {teamInfo[teamAbbr]?.fullName || teamAbbr}
                  </h3>
                </div>
                <div className={styles.teamContent}>
                  <div className={styles.teamStats}>
                    <p>Games Played: {team.games_played}</p>
                    <p>Minutes Played: {team.minutes_played}</p>
                    <p>Points: {team.points}</p>
                    <p>Valuation: {team.valuation}</p>
                  </div>
                  <div className={styles.charts}>
                    {renderPerformanceChart(teamAbbr)}
                    {renderSpiderChart(team)}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};

export default TeamsUserView;

