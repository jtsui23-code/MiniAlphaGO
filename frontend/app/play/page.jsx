'use client';

import React, { useRef, useState } from 'react';
import Nav from '@/components/nav';
import Board from '@/components/board';

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '1rem',
  },
  button: {
    backgroundColor: '#0070f3',
    color: 'white',
    border: 'none',
    padding: '0.5rem 1rem',
    cursor: 'pointer',
    marginBottom: '1rem',
  },
};

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

  const handleCellClick = async ({ x, y }) => {  // remove player from params
    alert("sent PUT request to server. making move")
    if (boardData[y]?.[x]) return; // ignore if cell occupied

    try {
      const res = await fetch('http://localhost:8000/move', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ x, y, player: playerTurn }),  // use current player state here
      });

      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

      const data = await res.json();

      setBoardData(data);
      boardRef.current?.setBoardFromJSON(data);

      const nextPlayer = playerTurn === 'black' ? 'white' : 'black';
      setPlayerTurn(nextPlayer);
      boardRef.current?.setPlayerTurn(nextPlayer);
    } catch (err) {
      alert('Failed to send move: ' + err.message);
    }
  };


  return (
    <>
      <Nav />
      <div style={styles.container}>
        <p>This is the play page</p>
        <button
          style={styles.button}
          onClick={handleStartGame}
          onMouseOver={e => (e.currentTarget.style.backgroundColor = '#005bb5')}
          onMouseOut={e => (e.currentTarget.style.backgroundColor = '#0070f3')}
        >
          Start Game
        </button>
        <Board ref={boardRef} onCellClick={handleCellClick} />
      </div>
    </>
  );
}
