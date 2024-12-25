"use client";

import React, { useState, useEffect, useRef } from "react";
import Image from "next/image";
import styles from "../styles/ComparisonUserView.module.css";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const HeaderUserView = ({ league }) => {
  const [selectedSeason, setSelectedSeason] = useState("");
  const [games, setGames] = useState([]);
  const [selectedGame, setSelectedGame] = useState("");
  const [loading, setLoading] = useState(false);
  const [gameDetails, setGameDetails] = useState(null);
  const [showGameDropdown, setShowGameDropdown] = useState(false);

  const gameDropdownRef = useRef(null);

  const seasons = Array.from({ length: 2016 - 2007 + 1 }, (_, i) => 2007 + i);
  const tournament = league === "euroleague" ? "lig" : "cup";

  useEffect(() => {
    if (selectedSeason) {
      setSelectedGame("");
      setGameDetails(null);
      fetchGames();
    }
  }, [selectedSeason]);

  useEffect(() => {
    if (selectedGame) {
      fetchGameDetails();
    }
  }, [selectedGame]);

  const fetchGames = async () => {
    setLoading(true);
    const yearPrefix = tournament === "cup" ? "U" : "E";
    const year = `${yearPrefix}${selectedSeason}`;
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/${tournament}_header/year_distinct_games?likePattern=${year}`
      );
      if (!response.ok)
        throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();
      setGames(data);
    } catch (error) {
      console.error("Error fetching games:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchGameDetails = async () => {
    setLoading(true);
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/${tournament}_header/${selectedGame}`
      );
      if (!response.ok)
        throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();
      setGameDetails(data);
    } catch (error) {
      console.error("Error fetching game details:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleGameClick = (game_id) => {
    setSelectedGame(game_id);
    setShowGameDropdown(false);
  };

  const renderGameOptions = () =>
    games.map(({ game, game_id }) => (
      <div
        key={game_id}
        className={`${styles.gameOption} ${
          selectedGame === game_id ? styles.selectedGame : ""
        }`}
        onClick={() => handleGameClick(game_id)}
      >
        <div className={styles.teamInfo}>
          <span className={styles.teamName}>{game.split("-")[0]}</span>
        </div>
        <span className={styles.vsText}>vs</span>
        <div className={`${styles.teamInfo} ${styles.rightTeam}`}>
          <span className={styles.teamName}>{game.split("-")[1]}</span>
        </div>
      </div>
    ));

  const renderCategoryChart = (category, stats) => {
    const chartData = Object.entries(stats).map(([key, value]) => ({
      name: key.replace(/_/g, " "),
      value,
    }));

    return (
      <div key={`chart-${category}`} className={styles.chartContainer}>
        <h4>{category} Stats Chart</h4>
        <ResponsiveContainer width="100%" height={320}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="value" fill="#000080" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    );
  };

  const renderGameDetails = () => {
    if (!gameDetails) return null;

    const { generalInfo, teamAStats, teamBStats } = gameDetails;

    return (
      <div className={styles.detailsView}>
        <h3>Game Details</h3>
        <div className={styles.detailsSection}>
          <h4>General Info</h4>
          <table>
            <tbody>
              {Object.entries(generalInfo).map(([key, value]) => (
                <tr key={key}>
                  <td>{key.replace(/_/g, " ")}</td>
                  <td>{value}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className={styles.detailsSection}>
          <h4>Team A Stats</h4>
          <table>
            <tbody>
              {Object.entries(teamAStats).map(([key, value]) => (
                <tr key={key}>
                  <td>{key.replace(/_/g, " ")}</td>
                  <td>{value}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {renderCategoryChart("Team A", teamAStats)}
        </div>
        <div className={styles.detailsSection}>
          <h4>Team B Stats</h4>
          <table>
            <tbody>
              {Object.entries(teamBStats).map(([key, value]) => (
                <tr key={key}>
                  <td>{key.replace(/_/g, " ")}</td>
                  <td>{value}</td>
                </tr>
              ))}
            </tbody>
          </table>
          {renderCategoryChart("Team B", teamBStats)}
        </div>
      </div>
    );
  };

  return (
    <div className={styles.containerWrapper}>
      <div className={styles.container}>
        <div className={styles.initialView}>
          <h2>Select a game to view details</h2>
          <div className={styles.selectors}>
            <div className={styles.selectWrapper}>
              <select
                value={selectedSeason}
                onChange={(e) => setSelectedSeason(e.target.value)}
              >
                <option value="">Select a Season</option>
                {seasons.map((season) => (
                  <option key={season} value={season}>
                    {season}-{season + 1}
                  </option>
                ))}
              </select>
            </div>
            <div className={styles.customSelect} ref={gameDropdownRef}>
              <div
                className={`${styles.selectedGame} ${
                  selectedGame ? styles.filled : ""
                }`}
                onClick={() => setShowGameDropdown(!showGameDropdown)}
              >
                {selectedGame || "Select a game"}
              </div>
              {showGameDropdown && (
                <div className={styles.gameDropdown}>{renderGameOptions()}</div>
              )}
            </div>
          </div>
        </div>
        {loading && <p>Loading...</p>}
        {renderGameDetails()}
      </div>
    </div>
  );
};

export default HeaderUserView;
