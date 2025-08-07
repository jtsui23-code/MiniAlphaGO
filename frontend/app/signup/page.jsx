"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Nav from "@/components/nav";
import "./page.css";

export default function Signup() {
  const [msg, setMsg] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  async function handleSignup(e) {
    e.preventDefault();
    setMsg("");
    try {
      const res = await fetch("http://localhost:8000/signup", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();

      if (data.success) {
        localStorage.setItem("fakeUser", email);
        alert("Signup successful! Redirecting...");
        router.push("/play");
      } else {
        setMsg(data.error || "Signup failed");
      }
    } catch (err) {
      setMsg("Signup failed: " + err.message);
    }
  }

  return (
    <>
      <Nav />
      <h2 className="signup-heading">Sign Up</h2>
      <form onSubmit={handleSignup} className="signup-form">
        <input
          name="username"
          type="email"
          placeholder="Email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          name="password"
          placeholder="Password"
          type="password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Sign Up</button>
      </form>
      <p>{msg}</p>
    </>
  );
}
