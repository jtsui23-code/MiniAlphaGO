'use client';
import "./page.css";
import React, { useRef, useState, useEffect } from 'react';
import Nav from '@/components/nav';
import Board from '@/components/board';

export default function PlayPage() {
  const boardRef = useRef(null);
  const moveAudio = useRef(typeof Audio !== "undefined" ? new Audio('/play/impact.mp3') : null);

  const [boardData, setBoardData] = useState(
    Array(9).fill(null).map(() => Array(9).fill(null))
  );
  const [playerTurn, setPlayerTurn] = useState('black');
  const [waitingForAI, setWaitingForAI] = useState(false);
  const [gameId, setGameId] = useState(null);
  const [opponent, setOpponent] = useState(null);
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const uid = localStorage.getItem("fakeUser");
    setIsLoggedIn(!!uid);
  }, []);

  const handleStartGame = async () => {
    const uid = localStorage.getItem("fakeUser");
    if (!uid) {
      alert("Please log in first.");
      return;
    }

    try {
      const res = await fetch('http://localhost:8000/newgame', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ opponent: 'CPU', uid }),
      });

      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

      const data = await res.json();
      setBoardData(data.board);
      setGameId(data.game_id);
      setOpponent(data.opponent);
      setPlayerTurn('black');
      setWaitingForAI(false);
      boardRef.current?.setBoardFromJSON(data.board);
      boardRef.current?.setPlayerTurn('black');
      alert(`New game started vs ${data.opponent}`);
    } catch (err) {
      alert('Failed to start game: ' + err.message);
    }
  };

  const handleCellClick = async ({ x, y }) => {
    if (waitingForAI || !gameId) return;
    if (boardData[y]?.[x]) return;

    moveAudio.current?.play();

    const updatedBoard = boardData.map((row, rowIndex) =>
      row.map((cell, colIndex) =>
        rowIndex === y && colIndex === x ? 'black' : cell
      )
    );
    setBoardData(updatedBoard);
    boardRef.current?.setBoardFromJSON(updatedBoard);

    setWaitingForAI(true);

    setTimeout(async () => {
      try {
        const res = await fetch(`http://localhost:8000/move?game_id=${gameId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ x, y }),
        });

        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

        const data = await res.json();
        setBoardData(data);
        boardRef.current?.setBoardFromJSON(data);

        setPlayerTurn('black');
        boardRef.current?.setPlayerTurn('black');
      } catch (err) {
        alert('Failed to send move: ' + err.message);
      } finally {
        setWaitingForAI(false);
      }
    }, 1000);
  };

  const handleSignOut = () => {
    localStorage.removeItem("fakeUser");
    window.location.reload();
  };

  return (
    <>
      <Nav />

      <div className="play-container">
        <p className="play-intro">
          Ready to challenge the Go AI? Click “Start Game” and enjoy a classic game of strategy.
        </p>

        {!isLoggedIn ? (
          <p style={{ color: 'red' }}>You must be logged in to play.</p>
        ) : (
          <>
            <button
              className="play-button"
              onClick={handleStartGame}
              disabled={waitingForAI}
            >
              Start Game
            </button>
            <button onClick={handleSignOut} className="play-button" style={{ marginLeft: '1rem' }}>
              Sign Out
            </button>
          </>
        )}

        <p>Opponent: {opponent || 'None'}</p>
        <p>Game ID: {gameId || 'None'}</p>

        <div className="board-wrapper">
          <Board ref={boardRef} onCellClick={handleCellClick} />
        </div>
      </div>
    </>
  );
}
