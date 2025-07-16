"use client";
import { useState } from "react";

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
      <form onSubmit={login}>
        <input name="username" placeholder="Username" required />
        <input name="password" placeholder="Password" type="password" required />
        <button>Login</button>
      </form>
      <p>{msg}</p>
    </>
  );
}
