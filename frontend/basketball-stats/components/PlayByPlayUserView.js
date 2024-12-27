"use client";

import React, { useState, useEffect } from "react";
import Image from "next/image";
import styles from "../styles/PlayByPlayUserView.module.css";
import LoadingSkeleton from "./LoadingSkeleton"; 
import ErrorDisplay from "./ErrorDisplay";       

const PlayByPlayUserView = ({ league }) => {
  // Seasons: 2007..2016
  const seasons = Array.from({ length: 2016 - 2007 + 1 }, (_, i) => 2007 + i);

  // "lig" for euroleague, "cup" otherwise
  const tournament = league === "euroleague" ? "lig" : "cup";

  // State
  const [selectedSeason, setSelectedSeason] = useState("");
  const [games, setGames] = useState([]);
  const [selectedGame, setSelectedGame] = useState("");
  const [playByPlayData, setPlayByPlayData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Team info (logos, full names)
  const [teamInfo, setTeamInfo] = useState({});
  const [currentGameTeams, setCurrentGameTeams] = useState({
    team1: null,
    team2: null,
  });
  const [showGameDropdown, setShowGameDropdown] = useState(false);

  // Pagination
  const [offset, setOffset] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(25);

  useEffect(() => {
    if (selectedSeason) {
      fetchGames();
    }
    setOffset(0);
    setSelectedGame("");
    setPlayByPlayData([]);
  }, [selectedSeason]);

  useEffect(() => {
    if (selectedGame) {
      fetchPlayByPlayData();
      updateCurrentGameTeams();
    }
  }, [selectedGame, offset, rowsPerPage]);

  const fetchGames = async () => {
    setLoading(true);
    setError(null);
    const yearPrefix = tournament === "cup" ? "U" : "E";
    const year = `${yearPrefix}${selectedSeason}`;

    try {
      const resp = await fetch(
        `http://127.0.0.1:5000/api/v1/${tournament}_play_by_play/year_distinct_games?likePattern=${year}`
      );
      if (!resp.ok) {
        throw new Error(`HTTP error! status: ${resp.status}`);
      }
      const data = await resp.json(); // array of game strings: ["BOS-LAL", "CHI-PHX", etc.]
      setGames(data);

      const allTeams = new Set(data.flatMap((g) => g.split("-")));
      await fetchTeamInfo(Array.from(allTeams));
    } catch (err) {
      console.error("Error fetching games:", err);
      setError("Unable to fetch game list. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  const fetchPlayByPlayData = async () => {
    setLoading(true);
    setError(null);

    const yearPrefix = tournament === "cup" ? "U" : "E";
    const year = `${yearPrefix}${selectedSeason}`;

    const columnsParam = [
      "game_play_id",
      "player",
      "team",
      "minute",
      "play_info",
      "points_a",
      "points_b",
      "game",
    ].join(",");

    const url = 
      `http://127.0.0.1:5000/api/v1/${tournament}_play_by_play/with_year_like` +
      `?likePattern=${year}` +
      `&offset=${offset}` +
      `&limit=${rowsPerPage}` +
      `&columns=${columnsParam}` +
      `&filters=game:${selectedGame}` +
      `&sortBy=minute&order=asc`;

    try {
      const resp = await fetch(url);
      if (!resp.ok) {
        throw new Error(`HTTP error! status: ${resp.status}`);
      }
      const data = await resp.json();
      setPlayByPlayData(data);
    } catch (err) {
      console.error("Error fetching play-by-play data:", err);
      setError("Unable to fetch play-by-play data. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  
  const fetchTeamInfo = async (abbreviations) => {
    if (!abbreviations.length) return;
    try {
      const resp = await fetch(
        `http://127.0.0.1:5000/api/v1/team?abbreviation=${abbreviations.join(",")}`
      );
      if (!resp.ok) {
        console.warn("No /team endpoint or no team data found.");
        return;
      }
      const data = await resp.json();
      const infoMap = {};
      data.forEach((team) => {
        infoMap[team.abbreviation] = {
          fullName: team.full_name,
          logoUrl:
            team.logo_url && team.logo_url.trim() !== ""
              ? `/teams_icons${team.logo_url.trimEnd()}`
              : "/teams_icons/default_team_icon.png",
        };
      });
      setTeamInfo((prev) => ({ ...prev, ...infoMap }));
    } catch (err) {
      console.error("Error fetching team info:", err);
    }
  };

  const updateCurrentGameTeams = () => {
    if (!selectedGame) return;
    const [team1, team2] = selectedGame.split("-");
    setCurrentGameTeams({
      team1:
        teamInfo[team1] || {
          fullName: team1,
          logoUrl: "/teams_icons/default_team_icon.png",
        },
      team2:
        teamInfo[team2] || {
          fullName: team2,
          logoUrl: "/teams_icons/default_team_icon.png",
        },
    });
  };

  const handleGameClick = (game) => {
    setSelectedGame(game);
    setOffset(0); // reset to first page
    setShowGameDropdown(false);
  };

  const renderGameOptions = () => {
    return games.map((game) => {
      const [team1, team2] = game.split("-");
      const fullName1 = teamInfo[team1]?.fullName || team1;
      const fullName2 = teamInfo[team2]?.fullName || team2;

      return (
        <div
          key={game}
          className={`${styles.gameOption} ${
            selectedGame === game ? styles.selectedGame : ""
          }`}
          onClick={() => handleGameClick(game)}
        >
          <div className={styles.teamInfo}>
            <Image
              src={
                teamInfo[team1]?.logoUrl || "/teams_icons/default_team_icon.png"
              }
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
              src={
                teamInfo[team2]?.logoUrl || "/teams_icons/default_team_icon.png"
              }
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

  // Pagination handlers
  const handlePrevious = () => {
    if (offset >= rowsPerPage) {
      setOffset(offset - rowsPerPage);
    }
  };

  const handleNext = () => {
    setOffset(offset + rowsPerPage);
  };

  return (
    <div className={styles.containerWrapper}>
      <div className={styles.container}>
        {/* Initial View */}
        <div className={styles.initialView}>
          {!selectedGame && (
            <h2>Select a game to view the play-by-play comparison</h2>
          )}
          <div className={styles.selectors}>
            {/* Season */}
            <div className={styles.selectWrapper}>
              <select
                value={selectedSeason}
                onChange={(e) => {
                  setSelectedSeason(e.target.value);
                }}
                className={selectedSeason ? styles.filled : ""}
              >
                <option value="">Season</option>
                {seasons.map((season) => (
                  <option key={season} value={season}>
                    {season}-{season + 1}
                  </option>
                ))}
              </select>
              <span className={styles.selectLabel}>Season</span>
            </div>

            {/* Game */}
            <div className={styles.customSelect}>
              <div
                className={`${styles.selectedGame} ${
                  selectedGame ? styles.filled : ""
                } ${!selectedSeason ? styles.disabledGame : ""}`}
                onClick={() =>
                  selectedSeason && setShowGameDropdown(!showGameDropdown)
                }
              >
                {selectedGame ? (
                  <>
                    <div className={styles.teamInfo}>
                      <Image
                        src={
                          currentGameTeams.team1?.logoUrl ||
                          "/teams_icons/default_team_icon.png"
                        }
                        alt={`${currentGameTeams.team1?.fullName} logo`}
                        width={30}
                        height={30}
                        className={styles.teamLogo}
                      />
                      <span className={styles.teamName}>
                        {currentGameTeams.team1?.fullName}
                      </span>
                    </div>
                    <span className={styles.vsText}>vs</span>
                    <div className={`${styles.teamInfo} ${styles.rightTeam}`}>
                      <span className={styles.teamName}>
                        {currentGameTeams.team2?.fullName}
                      </span>
                      <Image
                        src={
                          currentGameTeams.team2?.logoUrl ||
                          "/teams_icons/default_team_icon.png"
                        }
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
                <div className={styles.gameDropdown}>{renderGameOptions()}</div>
              )}
            </div>
          </div>
        </div>

        {/* Show errors */}
        {error && <ErrorDisplay message={error} onRetry={fetchGames} />}

        {/* Show PBP data */}
        {selectedGame && (
          <>
            {loading ? (
              <LoadingSkeleton rows={5} columns={3} />
            ) : (
              <div className={styles.playByPlayDetails}>
                {playByPlayData.length === 0 ? (
                  <p>No play-by-play data available for this game.</p>
                ) : (
                  playByPlayData.map((play, index) => (
                    <div key={play.game_play_id || index} className={styles.playRow}>
                      <div className={styles.minuteDisplay}>
                        {play.minute}'
                      </div>
                      <div className={styles.playInfo}>
                        <span>{play.play_info}</span>
                      </div>
                      <div className={styles.playerInfo}>
                        <span>{play.player} ({play.team})</span>
                      </div>
                      <div className={styles.pointsInfo}>
                        <span
                          className={
                            play.points_a > play.points_b ? styles.leadingPoints : ""
                          }
                        >
                          {play.points_a}
                        </span>
                        <span
                          className={
                            play.points_b > play.points_a ? styles.leadingPoints : ""
                          }
                        >
                          {play.points_b}
                        </span>
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}

            {/* Pagination Controls */}
            <div className={styles.paginationControls}>
              <button onClick={handlePrevious} disabled={offset === 0}>
                Previous
              </button>
              <select
                value={rowsPerPage}
                onChange={(e) => {
                  setRowsPerPage(Number(e.target.value));
                  setOffset(0); // reset to page 1
                }}
              >
                <option value={25}>25 rows</option>
                <option value={50}>50 rows</option>
                <option value={100}>100 rows</option>
              </select>
              <button onClick={handleNext}>
                Next
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default PlayByPlayUserView;
