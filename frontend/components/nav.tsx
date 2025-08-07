
import "./nav.css"

export default function Nav() {
  return (
    <nav>
      <div className="navbar">
        <a href="/">Home</a>

        <div className="navbar-right">
          <a href="/play">Play</a>
          <a href="/stats">Stats</a>
          <a href="/settings">Settings</a>
          <a href="/login">Login</a>
          <a href="/signup">Signup</a>

          
        </div>
      </div>
    </nav>
  );
}
