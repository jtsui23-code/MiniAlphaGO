"use client";
import { useState } from "react";
import Nav from "@/components/nav";

export default function Signup() {
  const [msg, setMsg] = useState("");

  async function handleSignup(e) {
    e.preventDefault();

    const form = new FormData(e.target);

    const res = await fetch("http://localhost:8080/api/signup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: form.get("username"),
        password: form.get("password"),
      }),
    });

    const text = await res.text();
    setMsg(text);
  }

  return (
    <>
    <Nav/>
      <h2>Sign Up</h2>
      <form onSubmit={handleSignup}>
        <input name="username" placeholder="Username" required />
        <input name="password" placeholder="Password" type="password" required />
        <button>Sign Up</button>
      </form>
      <p>{msg}</p>
    </>
  );
}
