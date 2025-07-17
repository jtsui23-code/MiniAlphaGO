'use client';

import { useState, useImperativeHandle, forwardRef } from 'react';

const BOARD_SIZE = 19;
const CELL_SIZE = 30;
const STONE_RADIUS = 10;

const Board = forwardRef((props, ref) => {
  const [board, setBoard] = useState(
    Array.from({ length: BOARD_SIZE }, () => Array(BOARD_SIZE).fill(null))
  );
  const [currentPlayer, setCurrentPlayer] = useState('black');

  const handleClick = (x, y) => {
    if (board[y][x]) return;

    const newBoard = board.map((row, j) =>
      row.map((cell, i) => (i === x && j === y ? currentPlayer : cell))
    );
    setBoard(newBoard);
    setCurrentPlayer(currentPlayer === 'black' ? 'white' : 'black');
  };

  useImperativeHandle(ref, () => ({
    setBoardFromJSON: (jsonBoard) => {
      const validated = jsonBoard.map((row = []) =>
        Array.from({ length: BOARD_SIZE }, (_, i) => row[i] ?? null)
      );
      setBoard(validated);
    },
  }));

  return (
    <svg
      width={CELL_SIZE * (BOARD_SIZE - 1)}
      height={CELL_SIZE * (BOARD_SIZE - 1)}
      style={{ backgroundColor: '#deb887', display: 'block' }}
    >
      {Array.from({ length: BOARD_SIZE }).map((_, i) => (
        <g key={`grid-${i}`}>
          <line
            x1={i * CELL_SIZE}
            y1={0}
            x2={i * CELL_SIZE}
            y2={(BOARD_SIZE - 1) * CELL_SIZE}
            stroke="black"
          />
          <line
            x1={0}
            y1={i * CELL_SIZE}
            x2={(BOARD_SIZE - 1) * CELL_SIZE}
            y2={i * CELL_SIZE}
            stroke="black"
          />
        </g>
      ))}

      {board.map((row, y) =>
        row.map((cell, x) =>
          cell ? (
            <circle
              key={`${x}-${y}`}
              cx={x * CELL_SIZE}
              cy={y * CELL_SIZE}
              r={STONE_RADIUS}
              fill={cell}
              stroke="black"
            />
          ) : (
            <circle
              key={`${x}-${y}-click`}
              cx={x * CELL_SIZE}
              cy={y * CELL_SIZE}
              r={CELL_SIZE / 2}
              fill="transparent"
              onClick={() => handleClick(x, y)}
              style={{ cursor: 'pointer' }}
            />
          )
        )
      )}
    </svg>
  );
});

export default Board;
