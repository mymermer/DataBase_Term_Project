"use client";

import React, { useState, useEffect } from "react";
import Image from "next/image";
import styles from "../styles/BoxScoreUserView.module.css";
import LoadingSkeleton from "./LoadingSkeleton";
import ErrorDisplay from "./ErrorDisplay";

const BoxScoreUserView = ({ league }) => {
  // Determine "lig" vs "cup"
  const tournament = league === "euroleague" ? "lig" : "cup";

  // Seasons array: 2007..2016
  const seasons = Array.from({ length: 2016 - 2007 + 1 }, (_, i) => 2007 + i);

  // Main state
  const [selectedSeason, setSelectedSeason] = useState("");
  const [games, setGames] = useState([]);
  const [selectedGame, setSelectedGame] = useState("");
  const [boxScores, setBoxScores] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Team info
  const [teamInfo, setTeamInfo] = useState({});
  const [showGameDropdown, setShowGameDropdown] = useState(false);
  const [currentGameTeams, setCurrentGameTeams] = useState({
    team1: null,
    team2: null,
  });

  // Pagination
  const [offset, setOffset] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(25);

  useEffect(() => {
    if (selectedSeason) {
      fetchGames();
    }
    setOffset(0);
    setSelectedGame("");
    setBoxScores([]);
  }, [selectedSeason]);

  useEffect(() => {
    if (selectedGame) {
      fetchBoxScores();
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
        `http://127.0.0.1:5000/api/v1/${tournament}_box_score/year_distinct_games?likePattern=${year}`
      );
      if (!resp.ok) {
        throw new Error(`HTTP error! status: ${resp.status}`);
      }
      const data = await resp.json() || [];
      // Filter out null or undefined items
      const filteredData = data.filter((g) => typeof g === "string");
      
      setGames(filteredData);
      
      // Then do the set of teams from only valid strings
      const allTeams = new Set(
        filteredData.flatMap((g) => g.split("-"))
      );
      await fetchTeamInfo(Array.from(allTeams));
      
    } catch (err) {
      console.error("Error fetching games:", err);
      setError("Unable to fetch game list for box scores. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const fetchBoxScores = async () => {
    setLoading(true);
    setError(null);
  
    const yearPrefix = tournament === "cup" ? "U" : "E";
    const year = `${yearPrefix}${selectedSeason}`;
  
    const columnsParam = [
      "game_player_id",
      "game",
      "player",
      "is_starter",
      "is_playing",
      "points",
      "two_points_made",
      "two_points_attempted",
      "three_points_made",
      "three_points_attempted",
      "free_throws_made",
      "free_throws_attempted",
      "offensive_rebounds",
      "defensive_rebounds",
      "total_rebounds",
      "assists",
      "steals",
      "turnovers",
      "blocks_favour",
      "blocks_against",
      "fouls_committed",
      "fouls_received",
      "valuation",
    ].join(",");
  
    const url = 
      `http://127.0.0.1:5000/api/v1/${tournament}_box_score/with_year_like` +
      `?likePattern=${year}` +
      `&columns=${columnsParam}` +
      `&filters=game:${selectedGame}` +
      `&sortBy=player&order=asc`; 
  
    try {
      const resp = await fetch(url);
      if (!resp.ok) {
        throw new Error(`HTTP error! status: ${resp.status}`);
      }
      const data = await resp.json();
  
      // Deduplicate data
      const uniqueBoxScores = data.filter(
        (player, index, self) =>
          index ===
          self.findIndex(
            (p) => p.game_player_id === player.game_player_id
          )
      );
  
      setBoxScores(uniqueBoxScores); // Save all deduplicated scores
    } catch (err) {
      console.error("Error fetching box scores:", err);
      setError("Unable to fetch box score data. Please try again.");
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
    setOffset(0); // Reset pagination
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

  const renderBoxScores = () => {
    if (!boxScores.length) {
      return <p>No box score data for this game.</p>;
    }
  
    const validBoxScores = boxScores.filter((playerStats) => {
      const t = playerStats.player_team?.trim();
      return t && t !== "N/A";
    });
  
    if (!validBoxScores.length) {
      return <p>No box score data for players with valid teams.</p>;
    }
  
    return validBoxScores.map((playerStats, index) => (
      <div
        key={`${playerStats.game_player_id || "unknown"}-${index}`} 
        className={styles.playerStatsRow}
      >
        <div className={styles.playerName}>
          <strong>{playerStats.player}</strong>
          {playerStats.is_starter ? <span> (Starter)</span> : ""}
          <p className={styles.playerTeam}>
            Team: {playerStats.player_team}
          </p>
        </div>
        <div className={styles.stats}>
          <p>Points: {playerStats.points}</p>
          <p>
            2PT: {playerStats.two_points_made}/{playerStats.two_points_attempted}
          </p>
          <p>
            3PT: {playerStats.three_points_made}/{playerStats.three_points_attempted}
          </p>
          <p>
            FT: {playerStats.free_throws_made}/{playerStats.free_throws_attempted}
          </p>
          <p>
            Rebounds: {playerStats.total_rebounds} (Off{" "}
            {playerStats.offensive_rebounds}/Def {playerStats.defensive_rebounds})
          </p>
          <p>Assists: {playerStats.assists}</p>
          <p>Steals: {playerStats.steals}</p>
          <p>Turnovers: {playerStats.turnovers}</p>
          <p>
            Blocks For/Against: {playerStats.blocks_favour}/
            {playerStats.blocks_against}
          </p>
          <p>
            Fouls (Committed/Received): {playerStats.fouls_committed}/
            {playerStats.fouls_received}
          </p>
          <p>Valuation: {playerStats.valuation}</p>
        </div>
      </div>
    ));
  };

const handlePrevious = () => {
  if (offset >= rowsPerPage) {
    setOffset(offset - rowsPerPage);
  }
};

const handleNext = () => {
  if (offset + rowsPerPage < boxScores.length) {
    setOffset(offset + rowsPerPage);
  }
};

return (
  <div className={styles.containerWrapper}>
    <div className={styles.container}>
      {/* Season & Game Selectors */}
      <div className={styles.initialView}>
        {!selectedGame && (
          <h2>Select a game to view the box score of players</h2>
        )}
        <div className={styles.selectors}>
          {/* Season dropdown */}
          <div className={styles.selectWrapper}>
            <select
              value={selectedSeason}
              onChange={(e) => setSelectedSeason(e.target.value)}
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
          {/* Game dropdown */}
          <div className={styles.customSelect}>
            <div
              className={`${styles.selectedGame} ${
                selectedGame ? styles.filled : ""
              } ${!selectedSeason ? styles.disabledGame : ""}`}
              onClick={() => selectedSeason && setShowGameDropdown(!showGameDropdown)}
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

      {/* Error Display */}
      {error && <ErrorDisplay message={error} onRetry={fetchGames} />}

      {/* Loading or the final box score output */}
      {selectedGame && (
        <>
          {loading ? (
            <LoadingSkeleton rows={5} columns={4} />
          ) : (
            <div className={styles.boxScoreDetails}>
              {renderBoxScores()}
            </div>
          )}
        </>
      )}
    </div>
  </div>
);
};

export default BoxScoreUserView;
