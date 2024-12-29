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
import ErrorDisplay from "./ErrorDisplay";
import LoadingSkeleton from "./LoadingSkeleton";

const ComparisonUserView = ({ league }) => {
  const [selectedSeason, setSelectedSeason] = useState("");
  const [games, setGames] = useState([]);
  const [selectedGame, setSelectedGame] = useState(null);
  const [loading, setLoading] = useState(false);
  const [teamInfo, setTeamInfo] = useState({});
  const [showGameDropdown, setShowGameDropdown] = useState(false);
  const [currentGameTeams, setCurrentGameTeams] = useState({
    team1: null,
    team2: null,
  });
  const [comparisonData, setComparisonData] = useState(null); // New state for fetched comparison data
  const [error, setError] = useState(null); // New state for error handling
  const [winLossData, setWinLossData] = useState(null);
  const [isWinLossLoading, setIsWinLossLoading] = useState(false);
  const [sortOrder, setSortOrder] = useState("desc");

  // Define categories for dividing the stats
  const categories = {
    OFFENSIVE: [
      "points_starters",
      "points_bench",
      "fast_break_points",
      "second_chance_points",
      "offensive_rebounds",
      "assists_starters",
      "assists_bench",
    ],
    DEFENSIVE: [
      "turnovers_starters",
      "turnovers_bench",
      "turnover_points",
      "steals_starters",
      "steals_bench",
      "defensive_rebounds",
    ],
    PERFORMANCE: ["minute_max_lead", "max_lead"],
  };

  const emojiMap = {
    points_starters: "⭐ Points (Starters)",
    points_bench: "🌟 Points (Bench)",
    fast_break_points: "⚡ Fast Break Points",
    second_chance_points: "🔄 Second Chance Points",
    offensive_rebounds: "🏀 Offensive Rebounds",
    assists_starters: "🤝🏻 Assists (Starters)",
    assists_bench: "🤝 Assists (Bench)",

    turnovers_starters: "🔁 Turnovers (Starters)",
    turnovers_bench: "🔃 Turnovers (Bench)",
    turnover_points: "✨ Turnover Points",
    steals_starters: "🥷 Steals (Starters)",
    steals_bench: "🕵️ Steals (Bench)",
    defensive_rebounds: "🛡️ Defensive Rebounds",

    minute_max_lead: "⏳ Minutes Max Lead",
    max_lead: "📈 Max Lead",
  };

  const chartMap = {
    points_starters: "⭐Points (Starters)",
    points_bench: "🌟Points (Bench)",
    fast_break_points: "⚡F.B. Points",
    second_chance_points: "🔄S.C. Points",
    offensive_rebounds: "🏀Off. Rebounds",
    assists_starters: "🤝🏻Assists (Starters)",
    assists_bench: "🤝Assists (Bench)",

    turnovers_starters: "🔁Turnovers (Starters)",
    turnovers_bench: "🔃Turnovers (Bench)",
    turnover_points: "✨Turnover Points",
    steals_starters: "🥷Steals (Starters)",
    steals_bench: "🕵️Steals (Bench)",
    defensive_rebounds: "🛡️Defensive Rebounds",

    minute_max_lead: "⏳Minutes Max Lead",
    max_lead: "📈Max Lead",
  };

  const seasons = Array.from({ length: 2023 - 2007 + 1 }, (_, i) => 2007 + i);
  const tournament = league === "euroleague" ? "lig" : "cup";

  const gameDropdownRef = useRef(null);

  const sortDataByDate = () => {
    const sortedData = [...winLossData.history].sort((a, b) => {
      const dateA = new Date(a.date_of_game);
      const dateB = new Date(b.date_of_game);
      return sortOrder === "asc" ? dateA - dateB : dateB - dateA;
    });

    setWinLossData({ ...winLossData, history: sortedData });
    setSortOrder(sortOrder === "asc" ? "desc" : "asc");
  };

  const renderCategoryChart = (category, keys) => {
    // Prepare data for the chart
    const chartData = keys.map((key) => {
      const statName = chartMap[key] || key.replace(/_/g, " ");
      return {
        name: statName,
        TeamA: comparisonData[`${key}_a`] || 0,
        TeamB: comparisonData[`${key}_b`] || 0,
      };
    });

    return (
      <div key={`chart-${category}`} className={styles.chartContainer}>
        <h4 className={styles.chartHeader}>{category} STATS CHART</h4>
        <ResponsiveContainer width="100%" height={320}>
          <BarChart
            data={chartData}
            layout="horizontal" // Change layout to horizontal for vertical representation
            margin={{ top: 20, right: 30, left: 30, bottom: 20 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" type="category" />{" "}
            {/* Use XAxis for stat names */}
            <YAxis type="number" /> {/* Use YAxis for numeric values */}
            <Tooltip />
            <Legend />
            <Bar
              dataKey="TeamA"
              fill="#480000"
              name={currentGameTeams.team1?.fullName || "Team A"}
            />
            <Bar
              dataKey="TeamB"
              fill="#000080"
              name={currentGameTeams.team2?.fullName || "Team B"}
            />
          </BarChart>
        </ResponsiveContainer>
      </div>
    );
  };

  useEffect(() => {
    if (selectedSeason) {
      // Reset the selected game, current game teams, and comparison data
      setSelectedGame("");
      setCurrentGameTeams({ team1: null, team2: null });
      setComparisonData(null);
      fetchGames();
    }
  }, [selectedSeason]);

  useEffect(() => {
    if (selectedGame) {
      fetchComparisonData();
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
    setError(null); // Added to clear previous errors
    const yearPrefix = tournament === "cup" ? "U" : "E";
    const year = `${yearPrefix}${selectedSeason}`;
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/${tournament}_comparison/year_distinct_games?likePattern=${year}`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setGames(data); // Now contains an array of { game_id, game }

      // Extract unique team abbreviations
      const allTeams = new Set(data.flatMap(({ game }) => game.split("-")));
      await fetchTeamInfo(Array.from(allTeams)); // Fetch team info
    } catch (error) {
      if (error.message.includes("404")) {
        setError(
          "No data found for the selected criteria. Please refine your search."
        );
      } else if (error.message.includes("Failed to fetch")) {
        setError(
          "Unable to load data. Please check your network connection or try again later."
        );
      } else {
        setError("An unexpected error occurred. Please contact support.");
      }
      console.error("Error message:", error.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const fetchTeamInfo = async (abbreviations) => {
    setLoading(true);
    setError(null); // Added to clear previous errors
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/team?abbreviation=${abbreviations.join(
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
      setTeamInfo((prevTeamInfo) => ({ ...prevTeamInfo, ...teamInfoMap }));
    } catch (error) {
      if (error.message.includes("404")) {
        setError(
          "No data found for the selected criteria. Please refine your search."
        );
      } else if (error.message.includes("Failed to fetch")) {
        setError(
          "Unable to load data. Please check your network connection or try again later."
        );
      } else {
        setError("An unexpected error occurred. Please contact support.");
      }
      console.error("Error message:", error.message);
      throw error;
    }
  };

  const fetchComparisonData = async () => {
    if (!selectedGame || !selectedGame.gameId) {
      console.error("Invalid selectedGame:", selectedGame);
      return;
    }

    setLoading(true);
    setError(null); // Added to clear previous errors
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/${tournament}_comparison/${selectedGame.gameId}`
      );

      if (response.status === 404) {
        console.error("Game data not found");
        setComparisonData(null);
        return;
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setComparisonData(data);
    } catch (error) {
      if (error.message.includes("404")) {
        setError(
          "No data found for the selected criteria. Please refine your search."
        );
      } else if (error.message.includes("Failed to fetch")) {
        setError(
          "Unable to load data. Please check your network connection or try again later."
        );
      } else {
        setError("An unexpected error occurred. Please contact support.");
      }
      console.error("Error message:", error.message);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const fetchWinLossHistory = async (team1Name, team2Name) => {
    if (!team1Name || !team2Name) {
      console.error("Teams are not selected.");
      setWinLossData(null); // Clear the previous win-loss data
      return;
    }

    setIsWinLossLoading(true);
    setError(null);

    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/${tournament}_comparison/win_loss_history?team1=${team1Name}&team2=${team2Name}`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();

      // Sort the fetched data by date in ascending order
      const sortedHistory = data.history.sort((a, b) => {
        const dateA = new Date(a.date_of_game);
        const dateB = new Date(b.date_of_game);
        return dateA - dateB; // Ascending order
      });

      // Update the state with sorted history
      setWinLossData({ ...data, history: sortedHistory });
    } catch (error) {
      console.error("Error fetching win-loss history:", error.message);
      setError("Failed to fetch win-loss history. Please try again later.");
    } finally {
      setIsWinLossLoading(false);
    }
  };

  const renderWinLossHistory = () => {
    if (isWinLossLoading) {
      return <p>Loading win-loss history...</p>;
    }

    if (!winLossData) {
      return <p>Win-loss history not available for this matchup.</p>;
    }

    return (
      <div className={styles.winLossContainer}>
        <h3>Win-Loss History</h3>
        <div
          style={{
            textAlign: "center",
            marginTop: "20px",
            fontSize: "1.2rem",
            color: "#333",
          }}
        >
          <p
            style={{
              marginBottom: "10px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontWeight: "bold",
            }}
          >
            <Image
              src={
                currentGameTeams.team1.logoUrl ||
                "/teams_icons/default_team_icon.png"
              }
              alt={`${currentGameTeams.team1.fullName} logo`}
              width={20}
              height={20}
              style={{ marginRight: "10px", verticalAlign: "middle" }}
            />
            {currentGameTeams.team1.fullName}: {winLossData.team1_wins} wins
          </p>
          <p
            style={{
              marginBottom: "10px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontWeight: "bold",
            }}
          >
            <Image
              src={
                currentGameTeams.team2.logoUrl ||
                "/teams_icons/default_team_icon.png"
              }
              alt={`${currentGameTeams.team2.fullName} logo`}
              width={20}
              height={20}
              style={{ marginRight: "10px", verticalAlign: "middle" }}
            />
            {currentGameTeams.team2.fullName}: {winLossData.team2_wins} wins
          </p>
          <p style={{ marginTop: "10px", fontWeight: "bold" }}>
            🤝 Draws: {winLossData.draws}
          </p>
          <h4
            style={{ marginTop: "10px", fontWeight: "bold", color: "#000080" }}
          >
            Total Games: {winLossData.total_games}
          </h4>
        </div>

        <table className={styles.historyTable}>
          <thead>
            <tr>
              <th onClick={sortDataByDate} style={{ cursor: "pointer" }}>
                Date {sortOrder === "asc" ? "⬆️" : "⬇️"}
              </th>
              <th>Time</th>
              <th>Game</th>
              <th>Score</th>
              <th>Winner</th>
            </tr>
          </thead>
          <tbody>
            {winLossData.history.map((game, index) => (
              <tr key={index}>
                <td>{game.date_of_game}</td>
                <td>{game.time_of_game?.slice(0, -3)}</td>
                <td>
                  {teamInfo[game.game.split("-")[0]]?.fullName ||
                    game.game.split("-")[0]}{" "}
                  -{" "}
                  {teamInfo[game.game.split("-")[1]]?.fullName ||
                    game.game.split("-")[1]}
                </td>
                <td>
                  <span
                    style={{
                      color:
                        game.score_a === game.score_b
                          ? "blue"
                          : game.score_a > game.score_b
                          ? "green"
                          : "red",
                    }}
                  >
                    {game.score_a}
                  </span>{" "}
                  -{" "}
                  <span
                    style={{
                      color:
                        game.score_a === game.score_b
                          ? "blue"
                          : game.score_b > game.score_a
                          ? "green"
                          : "red",
                    }}
                  >
                    {game.score_b}
                  </span>
                </td>
                <td>
                  {(() => {
                    const winner = game.winner?.trim().toLowerCase(); // Normalize the value of `game.winner`
                    if (winner === "team_a") {
                      return (
                        teamInfo[game.game.split("-")[0]]?.fullName || "Team A"
                      );
                    } else if (winner === "team_b") {
                      return (
                        teamInfo[game.game.split("-")[1]]?.fullName || "Team B"
                      );
                    } else if (winner === "draw") {
                      return "Draw!";
                    } else {
                      return "N/A"; // Fallback if no condition matches
                    }
                  })()}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  };

  const handleGameClick = (game_id) => {
    const selectedGameData = games.find((g) => g.game_id === game_id);
    const team1 = teamInfo[selectedGameData?.game.split("-")[0]];
    const team2 = teamInfo[selectedGameData?.game.split("-")[1]];

    if (!team1 || !team2) {
      console.error("Teams are not selected.");
      return;
    }

    setSelectedGame({
      gameId: game_id,
      team1: {
        fullName: team1.fullName || "Team 1",
        logoUrl: team1.logoUrl || "/teams_icons/default_team_icon.png",
      },
      team2: {
        fullName: team2.fullName || "Team 2",
        logoUrl: team2.logoUrl || "/teams_icons/default_team_icon.png",
      },
    });

    setCurrentGameTeams({
      team1: team1 || {
        fullName: "Team 1",
        logoUrl: "/teams_icons/default_team_icon.png",
      },
      team2: team2 || {
        fullName: "Team 2",
        logoUrl: "/teams_icons/default_team_icon.png",
      },
    });

    setShowGameDropdown(false);

    // Pass teams directly to fetchWinLossHistory
    fetchWinLossHistory(team1.fullName, team2.fullName);
  };

  const renderGameOptions = () => {
    return games.map(({ game, game_id }) => {
      const [team1, team2] = game.split("-");
      return (
        <div
          key={game_id}
          className={`${styles.gameOption} ${
            selectedGame === game_id ? styles.selectedGame : ""
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

  return (
    <div className={styles.containerWrapper}>
      <div className={styles.container}>
        <div className={styles.initialView}>
          {!selectedGame && (
            <h2>Choose a game to compare the performance of both teams!</h2>
          )}
          <div className={styles.selectors}>
            <div className={styles.selectWrapper}>
              <select
                value={selectedSeason}
                onChange={(e) => setSelectedSeason(e.target.value)}
                className={selectedSeason ? styles.filled : ""}
                onMouseLeave={() => setShowGameDropdown(false)}
              >
                <option value="">Select a Season</option>
                {seasons.map((season) => (
                  <option key={season} value={season}>
                    {season}-{season + 1}
                  </option>
                ))}
              </select>
              <span className={styles.selectLabel}>Season</span>
            </div>
            <div className={styles.customSelect} ref={gameDropdownRef}>
              <div
                className={`${styles.selectedGame} ${
                  selectedGame ? styles.filled : ""
                } ${!selectedSeason ? styles.disabledGame : ""}`}
                onClick={() =>
                  selectedSeason && setShowGameDropdown(!showGameDropdown)
                }
              >
                {selectedGame && typeof selectedGame === "object" ? (
                  <>
                    <div className={styles.teamInfo}>
                      <Image
                        src={selectedGame.team1.logoUrl}
                        alt={`${selectedGame.team1.fullName} logo`}
                        width={30}
                        height={30}
                        className={styles.teamLogo}
                      />
                      <span className={styles.teamName}>
                        {selectedGame.team1.fullName}
                      </span>
                    </div>
                    <span className={styles.vsText}>vs</span>
                    <div className={`${styles.teamInfo} ${styles.rightTeam}`}>
                      <span className={styles.teamName}>
                        {selectedGame.team2.fullName}
                      </span>
                      <Image
                        src={selectedGame.team2.logoUrl}
                        alt={`${selectedGame.team2.fullName} logo`}
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
                <div
                  className={styles.gameDropdown}
                  // onMouseLeave={() => setShowGameDropdown(false)} // Optional: Hide dropdown on mouse leave
                >
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
              <div className={styles.comparisonView}>
                {currentGameTeams.team1 && currentGameTeams.team2 ? (
                  comparisonData ? (
                    <div>
                      <div className={styles.gameInfo}>
                        <h3>GAME DETAILS</h3>
                        <div className={styles.detailsRow}>
                          <span className={styles.detail}>
                            <strong>🚩 Round:</strong>{" "}
                            <span style={{ color: "black" }}>
                              {comparisonData.round_of_game}
                            </span>
                          </span>
                          <span className={styles.detail}>
                            <strong>📌 Phase:</strong>{" "}
                            <span style={{ color: "black" }}>
                              {comparisonData.phase}
                            </span>
                          </span>
                          {selectedSeason && ( // Conditionally render if season is selected
                            <span className={styles.detail}>
                              <strong>🏆 Season:</strong>{" "}
                              <span style={{ color: "black" }}>
                                {selectedSeason}-{parseInt(selectedSeason) + 1}
                              </span>
                            </span>
                          )}
                        </div>
                      </div>

                      <h3>
                        Comparison between {currentGameTeams.team1.fullName} &{" "}
                        {currentGameTeams.team2.fullName}
                      </h3>
                      <table className={styles.comparisonTable}>
                        <thead>
                          <tr>
                            <th style={{ fontSize: "18px" }}>Statistic</th>
                            <th>
                              <div className={styles.teamHeader}>
                                <div className={styles.teamLogoWrapper}>
                                  <Image
                                    src={
                                      currentGameTeams.team1.logoUrl ||
                                      "/teams_icons/default_team_icon.png"
                                    }
                                    alt={`${currentGameTeams.team1.fullName} logo`}
                                    width={30}
                                    height={30}
                                    className={styles.teamLogo}
                                  />
                                </div>
                                <div className={styles.teamNameWrapper}>
                                  {currentGameTeams.team1.fullName}
                                </div>
                              </div>
                            </th>
                            <th>
                              <div className={styles.teamHeader}>
                                <div className={styles.teamLogoWrapper}>
                                  <Image
                                    src={
                                      currentGameTeams.team2.logoUrl ||
                                      "/teams_icons/default_team_icon.png"
                                    }
                                    alt={`${currentGameTeams.team2.fullName} logo`}
                                    width={30}
                                    height={30}
                                    className={styles.teamLogo}
                                  />
                                </div>
                                <div className={styles.teamNameWrapper}>
                                  {currentGameTeams.team2.fullName}
                                </div>
                              </div>
                            </th>
                          </tr>
                        </thead>
                        <tbody>
                          {Object.entries(categories).map(
                            ([category, keys], categoryIndex) => (
                              <React.Fragment key={`category-${categoryIndex}`}>
                                <tr>
                                  <td
                                    colSpan="3"
                                    className={styles.categoryHeader}
                                  >
                                    {category + " STATS:"}
                                  </td>
                                </tr>
                                {keys.map((key) => {
                                  const baseKey = key;

                                  // Use the emojiMap for the table labels
                                  const label =
                                    emojiMap[baseKey] ||
                                    baseKey.replace(/_/g, " ");

                                  const formatValue = (val) =>
                                    val === null ||
                                    val === undefined ||
                                    (typeof val === "string" &&
                                      val.trim() === "")
                                      ? "N/A"
                                      : typeof val === "string"
                                      ? val.trim()
                                      : val;

                                  return (
                                    <tr key={`row-${category}-${baseKey}`}>
                                      <td>{label}</td>
                                      <td>
                                        {formatValue(
                                          comparisonData[`${baseKey}_a`]
                                        )}
                                      </td>
                                      <td>
                                        {formatValue(
                                          comparisonData[`${baseKey}_b`]
                                        )}
                                      </td>
                                    </tr>
                                  );
                                })}
                                {/* Add chart for this category */}
                                <tr>
                                  <td colSpan="3">
                                    {comparisonData &&
                                      renderCategoryChart(category, keys)}
                                  </td>
                                </tr>
                              </React.Fragment>
                            )
                          )}
                        </tbody>
                      </table>
                      {isWinLossLoading ? (
                        <p>Loading win-loss history...</p>
                      ) : (
                        comparisonData && renderWinLossHistory()
                      )}
                    </div>
                  ) : (
                    <div className={styles.comingSoon}>
                      <p>Loading comparison data...</p>
                    </div>
                  )
                ) : (
                  <div className={styles.comingSoon}>
                    <p>Under Maintenance...</p>
                  </div>
                )}
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default ComparisonUserView;
