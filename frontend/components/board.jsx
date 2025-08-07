'use client';

import { useState, useImperativeHandle, forwardRef } from 'react';

const BOARD_SIZE = 9;
const CELL_SIZE = 40;
const STONE_RADIUS = 18;

function cloneBoard(board) {
  return board.map(row => [...row]);
}

function isOnBoard(x, y) {
  return x >= 0 && x < BOARD_SIZE && y >= 0 && y < BOARD_SIZE;
}

function getGroup(board, x, y, color, visited = new Set()) {
  const key = `${x},${y}`;
  if (!isOnBoard(x, y) || board[y][x] !== color || visited.has(key)) return [];

  visited.add(key);
  let group = [[x, y]];

  [[1, 0], [-1, 0], [0, 1], [0, -1]].forEach(([dx, dy]) => {
    group = group.concat(getGroup(board, x + dx, y + dy, color, visited));
  });

  return group;
}

function hasLiberty(board, group) {
  return group.some(([x, y]) =>
    [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([dx, dy]) => {
      const nx = x + dx;
      const ny = y + dy;
      return isOnBoard(nx, ny) && board[ny][nx] === null;
    })
  );
}

function removeGroup(board, group) {
  group.forEach(([x, y]) => {
    board[y][x] = null;
  });
}

const Board = forwardRef(({ onCellClick }, ref) => {
  const [board, setBoard] = useState(
    Array.from({ length: BOARD_SIZE }, () => Array(BOARD_SIZE).fill(null))
  );
  const [currentPlayer, setCurrentPlayer] = useState('black');

  useImperativeHandle(ref, () => ({
    setBoardFromJSON: (jsonBoard) => {
      const validated = jsonBoard.map((row = []) =>
        Array.from({ length: BOARD_SIZE }, (_, i) => row[i] ?? null)
      );
      setBoard(validated);
    },
    setPlayerTurn: (player) => {
      setCurrentPlayer(player);
    },
    playMove: (x, y, player) => {
      setBoard(prev => {
        if (prev[y][x] !== null) return prev;

        const newBoard = cloneBoard(prev);
        const color = player === 1 ? 'black' : 'white';
        const enemy = player === 1 ? 'white' : 'black';

        newBoard[y][x] = color;

        // Check and remove enemy groups with no liberties
        [[1,0], [-1,0], [0,1], [0,-1]].forEach(([dx, dy]) => {
          const nx = x + dx;
          const ny = y + dy;
          if (isOnBoard(nx, ny) && newBoard[ny][nx] === enemy) {
            const group = getGroup(newBoard, nx, ny, enemy);
            if (!hasLiberty(newBoard, group)) {
              removeGroup(newBoard, group);
            }
          }
        });

        // Suicide check (optional, not implemented here)

        return newBoard;
      });
    },
  }));

  const svgSize = CELL_SIZE * (BOARD_SIZE - 1);
  const halfCell = CELL_SIZE / 2;

  return (
    <svg
      width={svgSize + CELL_SIZE}
      height={svgSize + CELL_SIZE}
      viewBox={`-${halfCell} -${halfCell} ${svgSize + CELL_SIZE} ${svgSize + CELL_SIZE}`}
      style={{ display: 'block' }}
    >
      <defs>
        <pattern id="woodGrain" patternUnits="userSpaceOnUse" width="40" height="40">
          <rect width="40" height="40" fill="#deb887" />
          <rect y="0" width="1" height="40" fill="#d0a060" />
          <rect y="10" width="1" height="40" fill="#c89b56" />
          <rect y="20" width="1" height="40" fill="#b88540" />
        </pattern>
        <filter id="boardNoise">
          <feTurbulence type="fractalNoise" baseFrequency="0.6" numOctaves="1" result="turb" />
          <feColorMatrix type="saturate" values="0.2" />
          <feComposite in="turb" in2="SourceGraphic" operator="in" />
          <feBlend in="SourceGraphic" in2="turb" mode="multiply" />
        </filter>
        <filter id="stoneNoise">
          <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2" result="turbulence" />
          <feDisplacementMap in="SourceGraphic" in2="turbulence" scale="1" />
        </filter>
        <filter id="whiteStoneShadow" x="-50%" y="-50%" width="200%" height="200%">
          <feDropShadow dx="0" dy="0" stdDeviation="1" floodColor="#555" floodOpacity="0.6" />
        </filter>
        <radialGradient id="blackStone" cx="30%" cy="30%" r="70%">
          <stop offset="0%" stopColor="#777" />
          <stop offset="40%" stopColor="#222" />
          <stop offset="100%" stopColor="#000" />
        </radialGradient>
        <radialGradient id="whiteStone" cx="30%" cy="30%" r="70%">
          <stop offset="0%" stopColor="#fefefe" />
          <stop offset="40%" stopColor="#ddd" />
          <stop offset="100%" stopColor="#aaa" />
        </radialGradient>
      </defs>

      <rect
        x={-halfCell}
        y={-halfCell}
        width={svgSize + CELL_SIZE}
        height={svgSize + CELL_SIZE}
        fill="url(#woodGrain)"
        filter="url(#boardNoise)"
      />

      {Array.from({ length: BOARD_SIZE }).map((_, i) => (
        <g key={`grid-${i}`}>
          <line
            x1={i * CELL_SIZE}
            y1={0}
            x2={i * CELL_SIZE}
            y2={(BOARD_SIZE - 1) * CELL_SIZE}
            stroke="#000"
            strokeWidth="1"
          />
          <line
            x1={0}
            y1={i * CELL_SIZE}
            x2={(BOARD_SIZE - 1) * CELL_SIZE}
            y2={i * CELL_SIZE}
            stroke="#000"
            strokeWidth="1"
          />
        </g>
      ))}

      {board.map((row, y) =>
        row.map((cell, x) =>
          cell ? (
            <circle
              key={`stone-${x}-${y}`}
              cx={x * CELL_SIZE}
              cy={y * CELL_SIZE}
              r={STONE_RADIUS}
              fill={cell === 'black' ? 'url(#blackStone)' : 'url(#whiteStone)'}
              stroke={cell === 'black' ? '#222' : '#444'}
              strokeWidth="1.5"
              filter={cell === 'black' ? 'url(#stoneNoise)' : 'url(#whiteStoneShadow)'}
            />
          ) : (
            <circle
              key={`clickable-${x}-${y}`}
              cx={x * CELL_SIZE}
              cy={y * CELL_SIZE}
              r={CELL_SIZE / 2}
              fill="transparent"
              onClick={() => onCellClick && onCellClick({ x, y })}
              style={{ cursor: 'pointer' }}
            />
          )
        )
      )}
    </svg>
  );
});

export default Board;
