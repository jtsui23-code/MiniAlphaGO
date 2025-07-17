'use client';

import { useRef } from 'react';
import Nav from '@/components/nav';
import Board from '@/components/board'; // Make sure Board supports ref and setBoardFromJSON

export default function Home() {
  const boardRef = useRef(null);

  const handleStartGame = () => {
    const jsonBoard = [
      [null, null, null, null, null],
      [null, 'black', null, 'white', null],
      [null, null, 'black', null, null],
      [null, 'white', null, 'black', null],
      [null, null, null, null, null],
    ];

    if (boardRef.current && boardRef.current.setBoardFromJSON) {
      boardRef.current.setBoardFromJSON(jsonBoard);
    }
  };

  return (
    <>
      <Nav />
      <div
        style={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '100vh',
          padding: '20px',
          gap: '20px',
          fontFamily: 'Arial, sans-serif',
        }}
      >
        <p>This is the play page</p>

        <button
          onClick={handleStartGame}
          style={{
            padding: '10px 20px',
            backgroundColor: '#0070f3',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            fontSize: '16px',
          }}
          onMouseOver={e => (e.currentTarget.style.backgroundColor = '#005bb5')}
          onMouseOut={e => (e.currentTarget.style.backgroundColor = '#0070f3')}
        >
          Start
        </button>

        <Board ref={boardRef} />
      </div>
    </>
  );
}
