'use client';
import "./page.css";
import React, { useRef, useState } from 'react';
import Nav from '@/components/nav';
import Board from '@/components/board';

export default function PlayPage() {
  const boardRef = useRef(null);
  const [boardData, setBoardData] = useState(
    Array(9).fill(null).map(() => Array(9).fill(null))
  );
  const [playerTurn, setPlayerTurn] = useState('black');

  const handleStartGame = async () => {
    alert("sent POST request to server ['start game vs cpu]");
    try {
      const res = await fetch('http://localhost:8000/newgame', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ opponent: 'CPU' }),
      });

      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
      
      const data = await res.json();
      setBoardData(data);
      setPlayerTurn('black');
      boardRef.current?.setBoardFromJSON(data);
      boardRef.current?.setPlayerTurn('black');
    } catch (err) {
      alert('Failed to start game: ' + err.message);
    }
  };

const handleCellClick = async ({ x, y }) => {
  if (boardData[y]?.[x]) return;

  // Optimistically show the player's move on the board
  const updatedBoard = boardData.map((row, rowIndex) =>
    row.map((cell, colIndex) =>
      rowIndex === y && colIndex === x ? playerTurn : cell
    )
  );
  setBoardData(updatedBoard);
  boardRef.current?.setBoardFromJSON(updatedBoard);

  // Wait 1 second before sending move to backend
  setTimeout(async () => {
    try {
      const res = await fetch('http://localhost:8000/move', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ x, y }),
      });

      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

      const data = await res.json();
      setBoardData(data);
      boardRef.current?.setBoardFromJSON(data);

      const next = playerTurn === 'black' ? 'white' : 'black';
      setPlayerTurn(next);
      boardRef.current?.setPlayerTurn(next);
    } catch (err) {
      alert('Failed to send move: ' + err.message);
    }
  }, 1000); // 1000ms = 1 second
};


  return (
    <>
      <Nav />
      
      <div className="play-container">
        <p className="play-intro">
          Ready to challenge the Go AI? Click “Start Game” and enjoy a classic game of strategy.
        </p>
        <button
          className="play-button"
          onClick={handleStartGame}
        >
          Start Game
        </button>
        <div className="board-wrapper">
          <Board ref={boardRef} onCellClick={handleCellClick} />
        </div>
      </div>
    </>
  );
}
