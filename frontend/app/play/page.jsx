'use client';
import "./page.css";
import React, { useRef, useState, useEffect } from 'react';
import Nav from '@/components/nav';
import Board from '@/components/board';
// import { json } from "stream/consumers";

export default function PlayPage() {


  const [mode, setMode] = useState('AI');
  const [inviteCode, setInviteCode] = useState('');



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


  // For PvP ----------------------------------------------------
  const handlePvpStart = async () => {

    // Retrieves browser local storage to see if user is login
    // If the user is not login, then they will have a fakeUser value.
    const uid = localStorage.getItem("fakeUser")

    if (!uid) return alert("Please login")
    
    // Sending POST request to api/pvp/pvpStart endpoint
    const res = await fetch('http://localhost:8000/api/pvp/pvpStart', {
        method: 'POST',

        // Tells server we are sending json data.
        headers: {'Content-Type': 'application/json'},

        // Specificies the content of the JSON which is the user ID.
        body: JSON.stringify({uid}),
    });
  
  // Parse the JSON returned from the backend pvp/pvpStart endpoint
  const data = await res.json();
  const inviteCode = data.invite_code || '';
  const board = data.board || Array(9).fill(null).map(() => Array(9).fill(null));

  
  // Update components based off of the Parsed JSON
  setGameId(data.game_id);
  setInviteCode(inviteCode);
  setBoardData(board);
  setPlayerTurn("black");
  
  // Checks if boardRef.current exist before calling method from <board> to set the board up
  boardRef.current?.setBoardFromJSON(data.board);
  alert(`PvP Game Created. Share this invite code: ${inviteCode}`);

  };
  



  const handlePvpJoin = async () => {

    // Checks if the user is login based off of the browser local storage
    const uid = localStorage.getItem("fakeUser");
    if (!uid || !inviteCode) return alert("Missing user or invite code");

    
    const res = await fetch(`http://localhost:8000/api/pvp/join?inviteCode=${inviteCode}`, {
        method:'POST',
        headers:{ 'Content-Type': 'application/json' },
        body: JSON.stringify({uid}),
    
    });

    const result = await res.json();
    if(result?.Success){
      alert("Successfully joined game")

    }



  };

  // ------------------------------------------------------------


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

    if(mode == 'AI') {

        // boardData[y]?.[x] prevents placing stone on occupied position.
        if (boardData[y]?.[x]) return;
        moveAudio.current?.play();


        const updatedBoard = boardData.map((row, rowIndex) =>
            row.map((cell, colIndex) =>
            rowIndex === y && colIndex === x ? 'black' : cell
          ));


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
      }, 1000); // Adds 1 seconds delay from the AI's move so the user can tell what the AI's move was.

      return;  // AI mode is done

    }


    // PVP Mode

    if(boardData[y]?.[x]) return;

    const uid = localStorage.getItem("fakeUser");
    moveAudio.current?.play();

    // Using setWatingForAI to prevent player from doing multiple moves per turn and 
    // waits for backend server to update the viusals of the board.
    setWaitingForAI(true);

    try {
      const res = await fetch(`http://localhost:8000/api/pvp/pvpMove?inviteCode=${inviteCode}`, {

        method: 'PUT',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({uid, x, y, passTurn: false}),

    });

    if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);

    const data = await res.json();

    setBoardData(data);
    boardRef.current?.setBoardFromJSON(data);

    // Keeps track of whose turn it is logically and visually
    setPlayerTurn(prev => (prev == 'black' ? 'white': 'black'));

    boardRef.current?.setPlayerTurn(prev => (prev === 'black' ? 'white' : 'black'));

    } catch(err) {
        alert('Failed to send PvP move: ' + err.message);

    } finally {
      setWaitingForAI(false);
    }

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
          <p style={{ color: '#B8860B', fontWeight: '600' }}>You must be logged in to play.</p>
        ) : (
          <>
            <div className="pvp-controls" style={{marginBottom: '1rem'}}>
                <label htmlFor="mode">Mode: </label>
                <select
                  id="mode"
                  value={mode}
                  onChange={(e) => setMode(e.target.value)}
                  style={{marginRight: '1rem'}}
                >
                  <option value="AI">Play vs AI</option>
                  <option value="PVP">Play vs Player</option>

                </select>

                {mode === 'AI' && (
                  <button onClick={handleStartGame} disabled={waitingForAI} className="play-button">
                    Start Game
                  </button>
                )}

                {mode === 'PVP' && (
                  <>
                    <button onClick={handlePvpStart} className="play-button">
                      Create PVP Game
                    </button>
                    <input
                      type="text"
                      value={inviteCode}
                      onChange={(e) => setInviteCode(e.target.value)}
                      placeholder="Enter Invite Code"
                      style={{marginLeft: '0.5rem', marginRight: '0.5rem'}}
                    />

                    <button onClick={handlePvpJoin} className="play-button">
                      Join PVP Game
                    </button>

                  
                  </>
                )}

                <button onClick={handleSignOut} className="play-button" style={{marginleft: '1rem'}}>

                  Sign Out
                </button>

            </div>
            
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
