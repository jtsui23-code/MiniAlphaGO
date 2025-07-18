import Nav from "@/components/nav";
import './page.css';
import Link from "next/link";

export default function Home() {
  return (
    <>
      <Nav />
      <div className="hero">
        <h1>Go</h1>

        <div className="page-content">
          <p>
            Welcome to the Go website. Explore the ancient strategy game of Go. Play against our advanced Go AI, create an account to track your progress, and soon challenge your friends!
          </p>

          <section>
            <h2>Why Play Go?</h2>
            <ul>
              <li>Simple rules, endless strategic depth.</li>
              <li>Improve problem-solving and critical thinking.</li>
              <li>Join a global community of players.</li>
              <li>Compete in ranked matches or casual games.</li>
            </ul>
          </section>

          <section>
            <h2>Features</h2>
            <ul>
              <li>Play against AI with multiple difficulty levels.</li>
              <li>Save and review your game history.</li>
              <li>Secure account system with profiles and stats.</li>
            </ul>
          </section>

          <section>
            <h2>Get Started</h2>
            <p>
              Use the navigation menu to sign up or log in. Start a new game anytime.
            </p>
            <Link href="/play">
              <button className="cta-button">Start Playing Now</button>
            </Link>
          </section>

          <section className="footer-note">
            <p>
              We are continuously improving the site. Stay tuned for multiplayer features and tournaments.
            </p>
          </section>
        </div>
      </div>
    </>
  );
}
