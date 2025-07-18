import Image from "next/image";
import Nav from "@/components/nav";
import Board from "@/components/board";
import "./page.css";

export default function Stats() {
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
            <h1 className="username">Your Username</h1>
            <p className="rank">Rank: Dan 5</p>
            <p className="joined">Member since July 8th 2025</p>
          </div>
        </div>

        <div className="stats-grid">
          <div className="card green">
            <h3>Wins</h3>
            <p>12</p>
          </div>
          <div className="card red">
            <h3>Losses</h3>
            <p>8</p>
          </div>
          <div className="card blue">
            <h3>Win Rate</h3>
            <p>60%</p>
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
              {[...Array(5)].map((_, i) => (
                <tr key={i}>
                  <td>AI v{i}</td>
                  <td className={i % 2 === 0 ? "win" : "loss"}>
                    {i % 2 === 0 ? "Win" : "Loss"}
                  </td>
                  <td>{40 + i}</td>
                  <td>2025-07-0{i + 1}</td>
                  <td><button className="replay-btn">View</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <Board />
      </div>
    </>
  );
}
