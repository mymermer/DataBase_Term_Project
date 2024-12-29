import { useState } from "react";
import Link from "next/link";
import {
  BarChart2,
  Users,
  Scale,
  FileText,
  Play,
  Box,
  UserCheck,
} from "lucide-react";
import styles from "../styles/StatOptionsGrid.module.css";
import LoadingOverlayGeneral from "./LoadingOverlay_general";

const statOptions = [
  { id: "POINTS", icon: BarChart2, label: "Points", color: "#FF6B6B" },
  { id: "TEAMS", icon: Users, label: "Teams", color: "#4ECDC4" },
  { id: "COMPARISON", icon: Scale, label: "Comparison", color: "#45B7D1" },
  { id: "HEADER", icon: FileText, label: "Header", color: "#F9C80E" },
  { id: "PLAY_BY_PLAY", icon: Play, label: "Play by Play", color: "#FF8C42" },
  { id: "BOX_SCORE", icon: Box, label: "Box Score", color: "#662E9B" },
  { id: "PLAYERS", icon: UserCheck, label: "Players", color: "#5FAD56" },
];

export default function StatOptionsGrid({ league }) {
  const [isLoading, setIsLoading] = useState(false);

  return (
    <div className={styles.statOptionsContainer}>
      <LoadingOverlayGeneral isLoading={isLoading} />
      <div className={styles.optionsGrid}>
        {statOptions.map((option, index) => (
          <Link
            key={option.id}
            href={league ? `/${league}/${option.id.toLowerCase()}` : "#"}
            className={`${styles.optionCard} ${!league ? styles.disabled : ""}`}
            style={{
              "--delay": `${index * 0.1}s`,
              "--color": option.color,
            }}
            onClick={(e) => {
              if (!league) {
                e.preventDefault();
                return;
              }
              setIsLoading(true); // Show the loading overlay
            }}
          >
            <div className={styles.iconWrapper}>
              <option.icon className={styles.icon} size={32} />
            </div>
            <span className={styles.label}>{option.label}</span>
          </Link>
        ))}
      </div>
    </div>
  );
}
