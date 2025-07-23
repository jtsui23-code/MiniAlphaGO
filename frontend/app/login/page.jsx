"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Nav from "@/components/nav";
import "./page.css";

export default function Login() {
  const [msg, setMsg] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  async function login(e) {
    alert("Login attempt started");
    e.preventDefault();
    setMsg("");
    try {
      const res = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      const data = await res.json();

      if (data.success) {
        localStorage.setItem("fakeUser", email);
        alert("Login successful! Redirecting...");
        router.push("/play");
      } else {
        setMsg(data.error || "Login failed");
      }
    } catch (err) {
      setMsg("Login failed: " + err.message);
    }
  }

  return (
    <>
      <Nav />
      <h2 className="login-heading">Login</h2>
      <form onSubmit={login} className="login-form">
        <input
          name="email"
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
        <button type="submit">Login</button>
      </form>
      <p>{msg}</p>
    </>
  );
}
