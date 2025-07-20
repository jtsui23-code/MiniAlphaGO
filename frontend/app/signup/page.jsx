"use client";
import { useState } from "react";
import Nav from "@/components/nav";
import "./page.css";

import { initializeApp } from "firebase/app";
import { getAuth, createUserWithEmailAndPassword } from "firebase/auth";

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

export default function Signup() {
  const [msg, setMsg] = useState("");

  async function handleSignup(e) {
    e.preventDefault();
    const form = new FormData(e.target);
    const email = form.get("username");
    const password = form.get("password");

    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      setMsg("Signup successful! You can now log in.");
    } catch (error) {
      setMsg("Signup failed: " + error.message);
    }
  }

  return (
    <>
      <Nav />
      <h2 className="signup-heading">Sign Up</h2>
      <form onSubmit={handleSignup} className="signup-form">
        <input name="username" type="email" placeholder="Email" required />
        <input name="password" placeholder="Password" type="password" required />
        <button>Sign Up</button>
      </form>
      <p>{msg}</p>
    </>
  );
}
