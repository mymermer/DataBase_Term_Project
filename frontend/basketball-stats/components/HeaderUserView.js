"use client";

import React, { useState, useEffect, useRef } from "react";
import Image from "next/image";
import styles from "../styles/HeaderUserView.module.css";
import { Fireworks } from "fireworks-js";

const HeaderUserView = ({ league }) => {
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
  const [HeaderData, setHeaderData] = useState(null); // New state for fetched header data
  const [isFireworksActive, setIsFireworksActive] = useState(false); // Declare at the top
  const winnerSectionRef = useRef(null); // Ref for the winner section

  // Define categories for dividing the stats
  const categories = {
    DETAILS: [
      "coach",
      "timeouts",
      "fouls",
      "score",
      "score_quarter_1",
      "score_quarter_2",
      "score_quarter_3",
      "score_quarter_4",
      "score_extra_time_1",
      "score_extra_time_2",
      "score_extra_time_3",
      "score_extra_time_4",
    ],
  };

  const emojiMap = {
    coach: "🧑‍🎓 Coach",
    timeouts: "⏱️ Timeouts",
    fouls: "🚫 Fouls",
    score: "🏀 Score",
    score_quarter_1: "1️⃣ Score (Quarter 1)",
    score_quarter_2: "2️⃣ Score (Quarter 2)",
    score_quarter_3: "3️⃣ Score (Quarter 3)",
    score_quarter_4: "4️⃣ Score (Quarter 4)",
    score_extra_time_1: "🕒 Score (Extra Time 1)",
    score_extra_time_2: "🕕 Score (Extra Time 2)",
    score_extra_time_3: "🕘 Score (Extra Time 3)",
    score_extra_time_4: "🕛 Score (Extra Time 4)",
  };

  const seasons = Array.from({ length: 2023 - 2007 + 1 }, (_, i) => 2007 + i);
  const tournament = league === "euroleague" ? "lig" : "cup";

  const gameDropdownRef = useRef(null);

  useEffect(() => {
    if (selectedSeason) {
      // Reset the selected game, current game teams, and header data
      setSelectedGame("");
      setCurrentGameTeams({ team1: null, team2: null });
      setHeaderData(null);
      fetchGames();
    }
  }, [selectedSeason]);

  useEffect(() => {
    if (selectedGame) {
      fetchHeaderData();
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

  // Functions for manipulating header data

  const triggerFireworks = () => {
    if (isFireworksActive) return;

    setIsFireworksActive(true);

    const fireworksContainer = document.createElement("div");
    fireworksContainer.style.position = "fixed";
    fireworksContainer.style.top = "0";
    fireworksContainer.style.left = "0";
    fireworksContainer.style.width = "100%";
    fireworksContainer.style.height = "100%";
    fireworksContainer.style.pointerEvents = "none";
    fireworksContainer.style.zIndex = "9999";
    document.body.appendChild(fireworksContainer);

    const fireworks = new Fireworks(fireworksContainer, {
      hue: { min: 0, max: 360 },
      acceleration: 1.05,
      friction: 0.98,
      gravity: 1.5,
      particles: 50,
      traceLength: 3,
      explosion: 5,
      boundaries: { top: 50, bottom: fireworksContainer.clientHeight },
    });

    fireworks.start();

    setTimeout(() => {
      fireworks.stop();
      document.body.removeChild(fireworksContainer);
      setIsFireworksActive(false);
    }, 3500); // duration of fireworks = 3.5 seconds
  };

  useEffect(() => {
    const handleScroll = () => {
      if (!winnerSectionRef.current) return;

      const sectionPosition = winnerSectionRef.current.getBoundingClientRect();
      const isVisible =
        sectionPosition.top >= 0 && sectionPosition.top <= window.innerHeight;

      if (isVisible) {
        if (HeaderData?.winner !== "draw") {
          triggerFireworks();
        }
        window.removeEventListener("scroll", handleScroll); // Fireworks only trigger once
      }
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, [HeaderData]); // Add `HeaderData` as a dependency to re-run when a new game is selected

  const formatRefereeName = (referee) => {
    if (
      referee === undefined ||
      referee === null ||
      referee === "N/D" ||
      referee === "" ||
      !referee
    ) {
      return "undefined"; // Fallback for invalid or missing referee names
    }

    // Split the name by comma and trim whitespace
    const [lastName, firstName] = referee.split(",").map((name) => name.trim());

    // Capitalize the first letter of each name part
    const capitalize = (name) => {
      if (
        name === undefined ||
        name === null ||
        name === "N/D" ||
        name === "" ||
        !name
      )
        return "None";
      return name.charAt(0).toUpperCase() + name.slice(1).toLowerCase();
    };

    // Return the formatted name as "FirstName_LastName"
    return `${capitalize(firstName)}_${capitalize(lastName)}`;
  };

  // --------------------------------------

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

  const fetchHeaderData = async () => {
    if (!selectedGame || !selectedGame.gameId) {
      console.error("Invalid selectedGame:", selectedGame);
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/${tournament}_header/${selectedGame.gameId}`
      );

      if (response.status === 404) {
        console.error("Game data not found");
        setHeaderData(null);
        return;
      }

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("API Response Data:", data); // Log the API response
      setHeaderData(data);
    } catch (error) {
      console.error("Error fetching header data:", error);
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
    //triggerFireworks(); // Call the fireworks here
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
            <h2>Choose a game to explore its detailed stats and highlights!</h2>
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
          <div className={styles.headerView}>
            {currentGameTeams.team1 && currentGameTeams.team2 ? (
              HeaderData ? (
                <div>
                  <div className={styles.gameInfo}>
                    <h3>GAME DETAILS</h3>
                    <div className={styles.detailsGrid}>
                      <div className={styles.detail}>
                        <strong>📅 Date:</strong>
                        <span>{HeaderData.date_of_game}</span>
                      </div>
                      <div className={styles.detail}>
                        <strong>🕐 Time:</strong>
                        <span>{HeaderData.time_of_game?.slice(0, -3)}</span>
                      </div>
                      <div className={styles.detail}>
                        <strong>⏲ Duration:</strong>
                        <span>{HeaderData.game_time} mins</span>
                      </div>
                      <div className={styles.detail}>
                        <strong>🏟️ Stadium (capacity):</strong>
                        <span>
                          {HeaderData.stadium} ({HeaderData.capacity})
                        </span>
                      </div>
                      <div className={styles.detail}>
                        <strong>👨🏻‍⚖️ Referees:</strong>
                        <div className={styles.refereeList}>
                          <div>
                            {HeaderData.referee_1 !==
                            ("N/D" || null || undefined || "None" || "") ? (
                              <a
                                href={`https://en.wikipedia.org/wiki/${formatRefereeName(
                                  HeaderData.referee_1
                                )}`}
                                target="_blank"
                                rel="noopener noreferrer"
                                style={{
                                  textDecoration: "none",
                                  color: "#000",
                                }}
                              >
                                {HeaderData.referee_1}{" "}
                                <sup style={{ color: "#8b0000" }}>1</sup>
                              </a>
                            ) : (
                              <span style={{ color: "#555" }}>
                                undefined{" "}
                                <sup style={{ color: "#8b0000" }}>1</sup>
                              </span>
                            )}
                          </div>
                          <div>
                            {HeaderData.referee_2 !==
                            ("N/D" || null || undefined || "None" || "") ? (
                              <a
                                href={`https://en.wikipedia.org/wiki/${formatRefereeName(
                                  HeaderData.referee_2
                                )}`}
                                target="_blank"
                                rel="noopener noreferrer"
                                style={{
                                  textDecoration: "none",
                                  color: "#000",
                                }}
                              >
                                {HeaderData.referee_2}{" "}
                                <sup style={{ color: "#8b0000" }}>2</sup>
                              </a>
                            ) : (
                              <span style={{ color: "#555" }}>
                                undefined{" "}
                                <sup style={{ color: "#8b0000" }}>2</sup>
                              </span>
                            )}
                          </div>
                          <div>
                            {HeaderData.referee_3 !==
                            ("N/D" || null || undefined || "None" || "") ? (
                              <a
                                href={`https://en.wikipedia.org/wiki/${formatRefereeName(
                                  HeaderData.referee_3
                                )}`}
                                target="_blank"
                                rel="noopener noreferrer"
                                style={{
                                  textDecoration: "none",
                                  color: "#000",
                                }}
                              >
                                {HeaderData.referee_3}{" "}
                                <sup style={{ color: "#8b0000" }}>3</sup>
                              </a>
                            ) : (
                              <span style={{ color: "#555" }}>
                                undefined{" "}
                                <sup style={{ color: "#8b0000" }}>3</sup>
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                      <div className={styles.detail}>
                        <strong>📌 Phase:</strong>
                        <span>{HeaderData.phase}</span>
                      </div>
                      <div className={styles.detail}>
                        <strong>🚩 Round:</strong>
                        <span>{HeaderData.round_of_game}</span>
                      </div>
                      {selectedSeason && (
                        <div className={styles.detail}>
                          <strong>🏆 Season:</strong>
                          <span>
                            {selectedSeason}-{parseInt(selectedSeason) + 1}
                          </span>
                        </div>
                      )}
                    </div>
                  </div>

                  <h3>
                    Details of the game between{" "}
                    {currentGameTeams.team1.fullName} &{" "}
                    {currentGameTeams.team2.fullName}
                  </h3>
                  <table className={styles.headerTable}>
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
                            {keys.map((key) => {
                              const baseKey = key;

                              // Use the emojiMap for the table labels
                              const label =
                                emojiMap[baseKey] || baseKey.replace(/_/g, " ");

                              // Enhanced formatValue function with debug logs
                              const formatValue = (val) => {
                                if (
                                  [
                                    "score_extra_time_1",
                                    "score_extra_time_2",
                                    "score_extra_time_3",
                                    "score_extra_time_4",
                                  ].includes(baseKey)
                                ) {
                                  // Check specifically for null or undefined, return "None" only if invalid
                                  return val === null ||
                                    val === undefined ||
                                    isNaN(val) ||
                                    (typeof val === "string" &&
                                      val.trim() === "") ||
                                    val === 0
                                    ? "None"
                                    : val;
                                }

                                // General case for other keys
                                return val === null ||
                                  val === undefined ||
                                  (typeof val === "string" && val.trim() === "")
                                  ? "N/A"
                                  : val;
                              };

                              // Enhanced percentage calculation function with debug logs
                              const calculatePercentage = (
                                score,
                                totalScore
                              ) => {
                                console.log(
                                  `Calculating percentage for score: ${score}, totalScore: ${totalScore}`
                                );
                                if (
                                  score === null ||
                                  totalScore === null ||
                                  isNaN(score) ||
                                  isNaN(totalScore) ||
                                  totalScore === 0
                                ) {
                                  return ""; // Return empty if invalid or zero total score
                                }
                                return ` (${(
                                  (score / totalScore) *
                                  100
                                ).toFixed(2)}%)`;
                              };

                              const totalScoreA = HeaderData?.score_a ?? 0; // Team A total score
                              const totalScoreB = HeaderData?.score_b ?? 0; // Team B total score

                              const isScoreKey =
                                baseKey.startsWith("score_quarter_") ||
                                baseKey.startsWith("score_extra_time_");

                              return (
                                <tr key={`row-${category}-${baseKey}`}>
                                  <td>{label}</td>
                                  <td>
                                    {formatValue(HeaderData?.[`${baseKey}_a`])}
                                    {isScoreKey &&
                                      HeaderData[`${baseKey}_a`] !== null &&
                                      HeaderData[`${baseKey}_a`] !==
                                        undefined &&
                                      formatValue(
                                        HeaderData[`${baseKey}_a`]
                                      ) !== "None" &&
                                      calculatePercentage(
                                        parseFloat(HeaderData[`${baseKey}_a`]),
                                        parseFloat(totalScoreA)
                                      )}
                                  </td>
                                  <td>
                                    {formatValue(HeaderData?.[`${baseKey}_b`])}
                                    {isScoreKey &&
                                      HeaderData[`${baseKey}_b`] !== null &&
                                      HeaderData[`${baseKey}_b`] !==
                                        undefined &&
                                      formatValue(
                                        HeaderData[`${baseKey}_b`]
                                      ) !== "None" &&
                                      calculatePercentage(
                                        parseFloat(HeaderData[`${baseKey}_b`]),
                                        parseFloat(totalScoreB)
                                      )}
                                  </td>
                                </tr>
                              );
                            })}
                          </React.Fragment>
                        )
                      )}
                    </tbody>
                  </table>
                  <div ref={winnerSectionRef} className={styles.winnerSection} onClick={() => triggerFireworks()}>
                    {HeaderData?.winner === "team_a" && (
                      <div className={styles.winner}>
                        <Image
                          src={currentGameTeams.team1.logoUrl}
                          alt={`${currentGameTeams.team1.fullName} logo`}
                          width={50}
                          height={50}
                          className={styles.winnerLogo}
                        />
                        <p>
                          <strong>{currentGameTeams.team1.fullName}</strong> Won
                          the Game! 🎉
                        </p>
                      </div>
                    )}
                    {HeaderData?.winner === "team_b" && (
                      <div className={styles.winner}>
                        <Image
                          src={currentGameTeams.team2.logoUrl}
                          alt={`${currentGameTeams.team2.fullName} logo`}
                          width={50}
                          height={50}
                          className={styles.winnerLogo}
                        />
                        <p>
                          <strong>{currentGameTeams.team2.fullName}</strong> Won
                          the Game! 🎉
                        </p>
                      </div>
                    )}
                    {HeaderData?.winner === "draw" && (
                      <div className={styles.winner}>
                        <p>🤝 It's a Draw! Both Teams Fought Hard! ⚡</p>
                      </div>
                    )}
                  </div>
                </div>
              ) : (
                <div className={styles.comingSoon}>
                  <p>Loading header data...</p>
                </div>
              )
            ) : (
              <div className={styles.comingSoon}>
                <p>Under Maintenance...</p>
              </div>
            )}
          </div>
        )}
        {loading && <p>Loading...</p>}
      </div>
    </div>
  );
};

export default HeaderUserView;
