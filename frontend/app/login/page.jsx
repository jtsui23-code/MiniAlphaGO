"use client";
import { useState } from "react";
import Nav from "@/components/nav";
import "./page.css";

export default function Login() {
  const [msg, setMsg] = useState("");

  async function login(e) {
    e.preventDefault();
    const form = new FormData(e.target);
    const res = await fetch("http://localhost:8080/api/login", {
      method: "POST",
      body: JSON.stringify({
        username: form.get("username"),
        password: form.get("password"),
      }),
      headers: { "Content-Type": "application/json" },
    });
    const text = await res.text();
    setMsg(text);
  }

  return (
    <>
      <Nav />
      <form onSubmit={login} className="login-form">
        <input name="username" placeholder="Username" required />
        <input name="password" placeholder="Password" type="password" required />
        <button>Login</button>
      </form>
      <p>{msg}</p>
    </>
  );
}
