"use client";
import { useState, useRef, useEffect } from "react";
import Nav from "@/components/nav";
import "./setting.css";

import { initializeApp, getApps } from "firebase/app";
import {
  getAuth,
  onAuthStateChanged,
  updatePassword,
  reauthenticateWithCredential,
  EmailAuthProvider,
} from "firebase/auth";
import {
  getFirestore,
  doc,
  getDoc,
  setDoc,
} from "firebase/firestore";
import {
  getStorage,
  ref as storageRef,
  uploadBytes,
  getDownloadURL,
} from "firebase/storage";

const firebaseConfig = {
  apiKey: "AIzaSyDqKCESJu7FZd3j7ca42wUEb3TE7WD5iCA",
  authDomain: "chat-app-e8cf4.firebaseapp.com",
  projectId: "chat-app-e8cf4",
  storageBucket: "chat-app-e8cf4.firebasestorage.app",
  messagingSenderId: "55633371026",
  appId: "1:55633371026:web:c30bef35bf194a4a262b4b",
  measurementId: "G-WMNG5PQZ9B",
};

const app = !getApps().length ? initializeApp(firebaseConfig) : getApps()[0];
const auth = getAuth(app);
const db = getFirestore(app);
const storage = getStorage(app);

export default function Home() {
  const [user, setUser] = useState(null);
  const [username, setUsername] = useState("Player");
  const [avatar, setAvatar] = useState("/default-avatar.png");
  const avatarInput = useRef(null);

<<<<<<< HEAD
  const [username, setUsername] = useState("Player")
  const [password, setPassword] = useState("Password")

  const [avatar, setAvatar] = useState("/default-avatar.png")
  const avatarInput = useRef<HTMLInputElement>(null);
=======
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [passwordMsg, setPasswordMsg] = useState("");
  const [msg, setMsg] = useState("");
>>>>>>> e2cba215e293b539c3695253b5935d5db339bb66

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (usr) => {
      if (!usr) {
        // redirect or show login
        setUser(null);
        setUsername("Player");
        setAvatar("/default-avatar.png");
        return;
      }
      setUser(usr);

<<<<<<< HEAD
  const handleSavedPassword = () => {
    //Implement backend for changing password here later.

    console.log("Saving new password", password);
  }
  const handleSaveUsername = () => {
      //Implement backend for changing username here later.

      console.log("Saving new username:", username);
  };
=======
      // Load username & avatar from Firestore
      const docRef = doc(db, "users", usr.uid);
      const docSnap = await getDoc(docRef);
      if (docSnap.exists()) {
        const data = docSnap.data();
        if (data.username) setUsername(data.username);
        if (data.avatarURL) setAvatar(data.avatarURL);
      } else {
        setUsername(usr.email.split("@")[0]);
      }
    });

    return () => unsubscribe();
  }, []);

  async function handleSaveUsername() {
    if (!user) return;
    try {
      await setDoc(
        doc(db, "users", user.uid),
        { username, avatarURL: avatar },
        { merge: true }
      );
      setMsg("Settings saved.");
    } catch (e) {
      setMsg("Failed to save: " + e.message);
    }
  }

  async function handleAvatarChange(e) {
    if (!user) return;
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      const avatarRef = storageRef(storage, `avatars/${user.uid}`);
      await uploadBytes(avatarRef, file);
      const url = await getDownloadURL(avatarRef);
      setAvatar(url);
      setMsg("Avatar updated.");
    } catch (e) {
      setMsg("Avatar upload failed: " + e.message);
    }
  }

  async function handleChangePassword(e) {
    e.preventDefault();
    if (!user) return;

    setPasswordMsg("");

    const credential = EmailAuthProvider.credential(
      user.email,
      currentPassword
    );

    try {
      await reauthenticateWithCredential(user, credential);
      await updatePassword(user, newPassword);
      setPasswordMsg("Password changed.");
      setCurrentPassword("");
      setNewPassword("");
    } catch (e) {
      setPasswordMsg("Password change failed: " + e.message);
    }
  }
>>>>>>> e2cba215e293b539c3695253b5935d5db339bb66

  return (
    <>
      <Nav />

      <div className="setting-page">
        <h1 className="setting-header">Settings</h1>

        <div className="setting-container">
          <div className="setting-box">
            <div className="avatar-section">
              <span className="avatar-label">Profile</span>
              <img src={avatar} alt="avatar" className="avatar-image" />

              <input
                type="file"
                accept="image/*"
                style={{ display: "none" }}
                ref={avatarInput}
                onChange={handleAvatarChange}
              />
              <button
                onClick={() => avatarInput.current?.click()}
                className="primary-button"
              >
                Change Avatar
              </button>
            </div>
          </div>

<<<<<<< HEAD
          

              <div className="setting-box">

                <label className="input-label">Username</label>

                <div className="input-with-button">
                    {/* This is where the player user name can be changed */}
                    <input 
                      type="text" 
                      value={username}
                      onChange = { (e) => setUsername(e.target.value)}
                      className="styled-input"
                      placeholder={username}

                      />

                      <button 
                        onClick={handleSaveUsername}
                        className="secondary-button"
                      >
                        Save
                      </button>



                </div>


                <label className="input-label">Password</label>

                <div className="input-with-button">
                    {/* This is where the player user name can be changed */}
                    <input 
                      type="text" 
                      value={password}
                      onChange = { (e) => setUsername(e.target.value)}
                      className="styled-input"
                      placeholder={password}

                      />

                      <button 
                        onClick={handleSavedPassword}
                        className="secondary-button"
                      >
                        Save
                      </button>



                </div>
            
=======
          <div className="setting-box">
            <label className="input-label">Username</label>
            <div className="input-with-button">
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="styled-input"
              />
              <button
                onClick={handleSaveUsername}
                className="secondary-button"
              >
                Save
              </button>
>>>>>>> e2cba215e293b539c3695253b5935d5db339bb66
            </div>
            <p>{msg}</p>
          </div>

          <div className="setting-box">
            <h3>Change Password</h3>
            <form onSubmit={handleChangePassword}>
              <input
                type="password"
                placeholder="Current Password"
                value={currentPassword}
                onChange={(e) => setCurrentPassword(e.target.value)}
                className="styled-input"
                required
              />
              <input
                type="password"
                placeholder="New Password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                className="styled-input"
                required
              />
              <button type="submit" className="secondary-button">
                Change Password
              </button>
            </form>
            <p>{passwordMsg}</p>
          </div>
        </div>
      </div>
    </>
  );
}
