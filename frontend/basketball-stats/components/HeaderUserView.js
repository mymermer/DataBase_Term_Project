"use client";

import React, { useState, useEffect, useRef } from "react";
import Image from "next/image";
import styles from "../styles/HeaderUserView.module.css";
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
  const [selectedGame, setSelectedGame] = useState(null);
  const [loading, setLoading] = useState(false);
  const [gameDetails, setGameDetails] = useState(null);
  const [teamInfo, setTeamInfo] = useState({});
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

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        gameDropdownRef.current &&
        !gameDropdownRef.current.contains(event.target)
      ) {
        setShowGameDropdown(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  const fetchGames = async () => {
    setLoading(true);
    const yearPrefix = tournament === "cup" ? "U" : "E";
    const year = `${yearPrefix}${selectedSeason}`;
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/${tournament}_header/year_distinct_games?likePattern=${year}`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setGames(data);

      const allTeams = new Set(data.flatMap(({ game }) => game.split("-")));
      await fetchTeamInfo(Array.from(allTeams));
    } catch (error) {
      console.error("Error fetching games:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchTeamInfo = async (teamAbbreviations) => {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/team?abbreviation=${teamAbbreviations.join(
          ","
        )}`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      const teamInfoMap = {};
      data.forEach((team) => {
        teamInfoMap[team.abbreviation] = {
          fullName: team.full_name,
          logoUrl:
            team.logo_url && team.logo_url.trim() !== ""
              ? `/teams_icons${team.logo_url.trimEnd()}`
              : "/teams_icons/default_team_icon.png",
        };
      });
      setTeamInfo((prev) => ({ ...prev, ...teamInfoMap }));
    } catch (error) {
      console.error("Error fetching team info:", error);
    }
  };

  const fetchGameDetails = async () => {
    setLoading(true);
    try {
      if (!selectedGame || !selectedGame.game_id) {
        throw new Error("Invalid game selected.");
      }

      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/${tournament}_header/${selectedGame.game_id}`
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Log data to confirm API response
      console.log("Fetched game details:", data);

      if (!data || typeof data !== "object") {
        throw new Error("Unexpected response format.");
      }

      setGameDetails(data);
    } catch (error) {
      console.error("Error fetching game details:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleGameClick = (gameId) => {
    const selectedGameData = games.find((g) => g.game_id === gameId);
    setSelectedGame(selectedGameData);
    setShowGameDropdown(false);
  };

  const renderGameOptions = () => {
    return games.map(({ game, game_id }) => {
      const [team1, team2] = game.split("-");
      return (
        <div
          key={game_id}
          className={`${styles.gameOption} ${
            selectedGame?.game_id === game_id ? styles.selectedGame : ""
          }`}
          onClick={() => handleGameClick(game_id)}
        >
          <div className={styles.teamInfo}>
            <Image
              src={
                teamInfo[team1]?.logoUrl || "/teams_icons/default_team_icon.png"
              }
              alt={`${teamInfo[team1]?.fullName || team1} logo`}
              width={30}
              height={30}
              className={styles.teamLogo}
            />
            <span className={styles.teamName}>
              {teamInfo[team1]?.fullName || team1}
            </span>
          </div>
          <span className={styles.vsText}>vs</span>
          <div className={`${styles.teamInfo} ${styles.rightTeam}`}>
            <span className={styles.teamName}>
              {teamInfo[team2]?.fullName || team2}
            </span>
            <Image
              src={
                teamInfo[team2]?.logoUrl || "/teams_icons/default_team_icon.png"
              }
              alt={`${teamInfo[team2]?.fullName || team2} logo`}
              width={30}
              height={30}
              className={styles.teamLogo}
            />
          </div>
        </div>
      );
    });
  };

  const renderCategoryChart = (category, stats = {}) => {
    if (!stats || Object.keys(stats).length === 0) {
      // Handle the case where stats is empty
      return <p>No data available for {category}</p>;
    }

    // Prepare data for the chart
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
                {selectedGame ? selectedGame.game : "Select a game"}
              </div>
              {showGameDropdown && (
                <div className={styles.gameDropdown}>{renderGameOptions()}</div>
              )}
            </div>
          </div>
        </div>
        {loading && <p>Loading...</p>}
        {gameDetails && (
          <div className={styles.detailsView}>
            <h3>Game Details</h3>

            {/* General Info Section */}
            <div className={styles.detailsSection}>
              <h4>General Info</h4>
              <table className={styles.detailsTable}>
                <tbody>
                  {Object.entries(gameDetails || {}).map(([key, value]) =>
                    [
                      "game",
                      "date_of_game",
                      "time_of_game",
                      "round_of_game",
                      "phase",
                      "stadium",
                      "capacity",
                      "winner",
                    ].includes(key) ? (
                      <tr key={key}>
                        <td className={styles.keyCell}>
                          {key.replace(/_/g, " ")}
                        </td>
                        <td className={styles.valueCell}>{value}</td>
                      </tr>
                    ) : null
                  )}
                </tbody>
              </table>
            </div>

            {/* Team A Stats Section */}
            <div className={styles.detailsSection}>
              <h4>Team A Stats</h4>
              <table className={styles.detailsTable}>
                <tbody>
                  {Object.entries(gameDetails || {}).map(([key, value]) =>
                    key.endsWith("_a") ? (
                      <tr key={key}>
                        <td className={styles.keyCell}>
                          {key.replace(/_/g, " ").replace(/_a/g, "")}
                        </td>
                        <td className={styles.valueCell}>{value}</td>
                      </tr>
                    ) : null
                  )}
                </tbody>
              </table>
            </div>

            {/* Team B Stats Section */}
            <div className={styles.detailsSection}>
              <h4>Team B Stats</h4>
              <table className={styles.detailsTable}>
                <tbody>
                  {Object.entries(gameDetails || {}).map(([key, value]) =>
                    key.endsWith("_b") ? (
                      <tr key={key}>
                        <td className={styles.keyCell}>
                          {key.replace(/_/g, " ").replace(/_b/g, "")}
                        </td>
                        <td className={styles.valueCell}>{value}</td>
                      </tr>
                    ) : null
                  )}
                </tbody>
              </table>
            </div>

            {/* Render Quarter Details */}
            <div className={styles.detailsSection}>
              <h4>Quarter Scores</h4>
              <table className={styles.detailsTable}>
                <thead>
                  <tr>
                    <th>Quarter</th>
                    <th>Team A</th>
                    <th>Team B</th>
                  </tr>
                </thead>
                <tbody>
                  {[1, 2, 3, 4].map((q) => (
                    <tr key={`quarter-${q}`}>
                      <td>Quarter {q}</td>
                      <td>{gameDetails[`score_quarter_${q}_a`] || "N/A"}</td>
                      <td>{gameDetails[`score_quarter_${q}_b`] || "N/A"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default HeaderUserView;
