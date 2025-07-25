'use client';
import React, { useEffect, useState, useRef } from "react";
import Image from "next/image";
import Nav from "@/components/nav";
import Board from "@/components/board";
import { getAuth } from "firebase/auth";
import "./page.css";

export default function Stats() {
  const [games, setGames] = useState([]);
  const [replaying, setReplaying] = useState(false);
  const [user, setUser] = useState(null);
  const boardRef = useRef(null);

  useEffect(() => {
    const loggedUser = localStorage.getItem("fakeUser");
    if (!loggedUser) {
      alert("Please log in to see your stats.");
      setGames([]);
      setUser(null);
      return;
    }
    setUser(loggedUser);
    fetchGames(loggedUser);
  }, []);

  async function fetchGames(userEmail) {
    try {
      const res = await fetch(`http://localhost:8000/stats?uid=${encodeURIComponent(userEmail)}`);
      if (!res.ok) throw new Error("Failed to load games");
      const data = await res.json();
    } catch (err) {
      alert("Error fetching games: " + err.message);
      setGames([]);
    }
  }

  function replayGame(moves) {
    if (!boardRef.current) return;
    setReplaying(true);

    boardRef.current.setBoardFromJSON(
      Array(9).fill(null).map(() => Array(9).fill(null))
    );

    let i = 0;
    const interval = setInterval(() => {
      if (i >= moves.length) {
        clearInterval(interval);
        setReplaying(false);
        return;
      }
      const move = moves[i];
      boardRef.current.playMove(
        move.x,
        move.y,
        move.player === "black" ? 1 : -1
      );
      i++;
    }, 500);
  }

  async function getUserStats() {
    const auth = getAuth();
    const user = auth.currentUser;

    if(!user){
      console.error("No user logined in.");
      return;
    }

    const idToken = await user.getIdToken();

    const response = await fetch("http://localhost:8000/stats", {
      method:"GET",
      headers: {
        "Authorization": `Bearer ${idToken}`,
      },

    });

    if (!response.ok){
      const error = await response.json();
      console.error("Failed to fetch user stats", error);
      return;
    }

    const data = await response.json();
    console.log("Stats", data);
    return data;
  }

  return (
    <>
      <Nav />

      <div className="stats-container">
        <div className="profile-header">
          <Image
            src="/profile-placeholder.png"
            alt="Profile"
            width={100}
            height={100}
            className="avatar"
          />
          <div>
            <h1 className="username">{user || "Guest"}</h1>
            <p className="rank">Rank: Dan 5</p>
            <p className="joined">Member since July 8th 2025</p>
          </div>
        </div>

        <div className="stats-grid">
          <div className="card green">
            <h3>Wins</h3>
            <p>{games.filter(g => g.winner === "black").length}</p>
          </div>
          <div className="card red">
            <h3>Losses</h3>
            <p>{games.filter(g => g.winner === "white").length}</p>
          </div>
          <div className="card blue">
            <h3>Win Rate</h3>
            <p>
              {games.length === 0
                ? "0%"
                : Math.round(
                    (games.filter(g => g.winner === "black").length / games.length) *
                      100
                  ) + "%"}
            </p>
          </div>
        </div>

        <div className="recent-games">
          <table>
            <thead>
              <tr>
                <th>Opponent</th>
                <th>Result</th>
                <th>Moves</th>
                <th>Date</th>
                <th>Replay</th>
              </tr>
            </thead>
            <tbody>
              {games.length === 0 ? (
                <tr>
                  <td colSpan={5}>No games played yet</td>
                </tr>
              ) : (
                games.map((game) => {
                  const result =
                    game.winner === "black"
                      ? "Win"
                      : game.winner === "white"
                      ? "Loss"
                      : "Draw";
                  return (
                    <tr key={game.game_id}>
                      <td>{game.opponent}</td>
                      <td className={result === "Win" ? "win" : "loss"}>
                        {result}
                      </td>
                      <td>{game.moves.length}</td>
                      <td>{game.date}</td>
                      <td>
                        <button
                          className="replay-btn"
                          disabled={replaying}
                          onClick={() => replayGame(game.moves)}
                        >
                          {replaying ? "Replaying..." : "View"}
                        </button>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>

          <div className="board-wrapper" style={{ marginTop: 20 }}>
            <Board ref={boardRef} onCellClick={() => {}} />
          </div>
        </div>
      </div>
    </>
  );
}
