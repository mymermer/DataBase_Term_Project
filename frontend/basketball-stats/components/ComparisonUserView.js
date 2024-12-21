"use client";

import React, { useState, useEffect } from "react";
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

  const seasons = Array.from({ length: 2016 - 2007 + 1 }, (_, i) => 2007 + i);
  const tournament = league === "euroleague" ? "lig" : "cup";

  useEffect(() => {
    if (selectedSeason) {
      fetchGames();
    }
  }, [selectedSeason]);

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
      setGames(data);

      // Extract unique team abbreviations for fetching team info
      const allTeams = new Set(data.flatMap((game) => game.split("-")));
      await fetchTeamInfo(Array.from(allTeams));
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

  const updateCurrentGameTeams = () => {
    if (selectedGame) {
      const [team1, team2] = selectedGame.split("-");
      setCurrentGameTeams({
        team1: teamInfo[team1] || {
          fullName: team1,
          logoUrl: "/teams_icons/default_team_icon.png",
        },
        team2: teamInfo[team2] || {
          fullName: team2,
          logoUrl: "/teams_icons/default_team_icon.png",
        },
      });
    }
  };

  const renderGameOptions = () => {
    return games.map((game) => {
      const [team1, team2] = game.split("-");
      return (
        <div
          key={game}
          className={`${styles.gameOption} ${
            selectedGame === game ? styles.selectedGame : ''
          }`}
          onClick={() => {
            setSelectedGame(game);
            setShowGameDropdown(false);
            updateCurrentGameTeams();
          }}
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
            <h2>Select a game to view the comparison between the 2 teams in that game</h2>
          )}
          <div className={styles.selectors}>
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
                        src={currentGameTeams.team1.logoUrl}
                        alt={`${currentGameTeams.team1.fullName} logo`}
                        width={30}
                        height={30}
                        className={styles.teamLogo}
                      />
                      <span className={styles.teamName}>
                        {currentGameTeams.team1.fullName}
                      </span>
                    </div>
                    <span className={styles.vsText}>vs</span>
                    <div className={`${styles.teamInfo} ${styles.rightTeam}`}>
                      <span className={styles.teamName}>
                        {currentGameTeams.team2.fullName}
                      </span>
                      <Image
                        src={currentGameTeams.team2.logoUrl}
                        alt={`${currentGameTeams.team2.fullName} logo`}
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
        {loading && <p>Loading...</p>}
      </div>
    </div>
  );
};

export default ComparisonUserView;
