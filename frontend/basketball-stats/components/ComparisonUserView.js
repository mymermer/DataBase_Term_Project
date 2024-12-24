"use client";

import React, { useState, useEffect, useRef } from "react";
import Image from "next/image";
import styles from "../styles/ComparisonUserView.module.css";

const ComparisonUserView = ({ league }) => {
  const [selectedSeason, setSelectedSeason] = useState("");
  const [games, setGames] = useState([]);
  const [selectedGame, setSelectedGame] = useState("");
  const [loading, setLoading] = useState(false);
  const [teamInfo, setTeamInfo] = useState({});
  const [showGameDropdown, setShowGameDropdown] = useState(false);
  const [currentGameTeams, setCurrentGameTeams] = useState({
    team1: null,
    team2: null,
  });
  const [comparisonData, setComparisonData] = useState(null); // New state for fetched comparison data

  const seasons = Array.from({ length: 2016 - 2007 + 1 }, (_, i) => 2007 + i);
  const tournament = league === "euroleague" ? "lig" : "cup";

  const gameDropdownRef = useRef(null);

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
      console.error("Error fetching games:", error);
    } finally {
      setLoading(false);
    }
  };

  const fetchTeamInfo = async (abbreviations) => {
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
      console.error("Error fetching team info:", error);
    }
  };

  const fetchComparisonData = async () => {
    if (!selectedGame || !selectedGame.gameId) {
      console.error("Invalid selectedGame:", selectedGame);
      return;
    }

    setLoading(true);
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
      console.error("Error fetching comparison data:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleGameClick = (game_id) => {
    const selectedGameData = games.find((g) => g.game_id === game_id);
    setSelectedGame({
      gameId: game_id,
      team1: {
        fullName:
          teamInfo[selectedGameData?.game.split("-")[0]]?.fullName || "Team 1",
        logoUrl:
          teamInfo[selectedGameData?.game.split("-")[0]]?.logoUrl ||
          "/teams_icons/default_team_icon.png",
      },
      team2: {
        fullName:
          teamInfo[selectedGameData?.game.split("-")[1]]?.fullName || "Team 2",
        logoUrl:
          teamInfo[selectedGameData?.game.split("-")[1]]?.logoUrl ||
          "/teams_icons/default_team_icon.png",
      },
    });

    setCurrentGameTeams({
      team1: teamInfo[selectedGameData?.game.split("-")[0]] || {
        fullName: "Team 1",
        logoUrl: "/teams_icons/default_team_icon.png",
      },
      team2: teamInfo[selectedGameData?.game.split("-")[1]] || {
        fullName: "Team 2",
        logoUrl: "/teams_icons/default_team_icon.png",
      },
    });
    setShowGameDropdown(false);
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
            <h2>
              Select a game to view the comparison between the 2 teams in that
              game
            </h2>
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
        {selectedGame && (
          <div className={styles.comparisonView}>
            {currentGameTeams.team1 && currentGameTeams.team2 ? (
              comparisonData ? (
                <div>
                  <div className={styles.gameInfo}>
                    <h3>Game Details</h3>
                    <div className={styles.detailsRow}>
                      <span className={styles.detail}>
                        <strong>Round:</strong>{" "}
                        <span style={{ color: "black" }}>
                          {comparisonData.round_of_game}
                        </span>
                      </span>
                      <span className={styles.detail}>
                        <strong>Phase:</strong>{" "}
                        <span style={{ color: "black" }}>
                          {comparisonData.phase}
                        </span>
                      </span>
                      {selectedSeason && ( // Conditionally render if season is selected
                        <span className={styles.detail}>
                          <strong>Season:</strong>{" "}
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
                        <th>Statistic</th>
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
                      {Object.entries(comparisonData || {})
                        .filter(([key]) => key.endsWith("_a"))
                        .map(([key, value]) => {
                          const baseKey = key.replace(/_a$/, "");
                          const formatValue = (val) => {
                            const trimmedVal = val?.trim ? val.trim() : val; // Trim the value if it's a string
                            console.log(
                              `Processing trimmed value for key "${key}":`,
                              trimmedVal
                            ); // Debugging output
                            return trimmedVal === null ||
                              trimmedVal === undefined ||
                              trimmedVal === ""
                              ? "N/A"
                              : trimmedVal;
                          };

                          const formattedValueA = formatValue(value);
                          const formattedValueB = formatValue(
                            comparisonData[`${baseKey}_b`]
                          );

                          console.log(
                            `Formatted value for "${key}":`,
                            formattedValueA
                          ); // Debug statement
                          console.log(
                            `Formatted value for "${baseKey}_b":`,
                            formattedValueB
                          ); // Debug statement

                          return (
                            <tr key={baseKey}>
                              <td>{baseKey.replace(/_/g, " ")}</td>
                              <td>{formattedValueA}</td>
                              <td>{formattedValueB}</td>
                            </tr>
                          );
                        })}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className={styles.comingSoon}>
                  <p>Loading comparison data...</p>
                </div>
              )
            ) : (
              <div className={styles.comingSoon}>
                <p>Coming soon or being updated...</p>
              </div>
            )}
          </div>
        )}
        {loading && <p>Loading...</p>}
      </div>
    </div>
  );
};

export default ComparisonUserView;
