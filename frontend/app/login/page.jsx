"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Nav from "@/components/nav";
import "./page.css";

import { initializeApp } from "firebase/app";
import { getAuth, signInWithEmailAndPassword } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyDqKCESJu7FZd3j7ca42wUEb3TE7WD5iCA",
  authDomain: "chat-app-e8cf4.firebaseapp.com",
  projectId: "chat-app-e8cf4",
  storageBucket: "chat-app-e8cf4.firebasestorage.app",
  messagingSenderId: "55633371026",
  appId: "1:55633371026:web:c30bef35bf194a4a262b4b",
  measurementId: "G-WMNG5PQZ9B",
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export default function Login() {
  const [msg, setMsg] = useState("");
  const router = useRouter();

  async function login(e) {
    e.preventDefault();
    const form = new FormData(e.target);
    const email = form.get("username");
    const password = form.get("password");

    try {
      await signInWithEmailAndPassword(auth, email, password);
      alert("Login successful!");
      setTimeout(() => router.push("/play"), 1000);
    } catch (error) {
      setMsg("Login failed: " + error.message);
    }
  }

  return (
    <>
      <Nav />
      <h2 className="login-heading">Login</h2>
      <form onSubmit={login} className="login-form">
        <input name="username" type="email" placeholder="Email" required />
        <input name="password" placeholder="Password" type="password" required />
        <button>Login</button>
      </form>
      <p>{msg}</p>
    </>
  );
}
