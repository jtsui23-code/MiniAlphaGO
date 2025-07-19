'use client';
import Image from "next/image";
import './setting.css'
import Nav from "@/components/nav";
import {useState, useRef} from 'react';


export default function Home() {

  const [avatar, setAvatar] = useState("/default-avatar.png")
  const avatarInput = useRef<HTMLInputElement>(null);

  return (
  <>
    <Nav/> 

    {/* Add justify-center here to center vertically */}
    <div className="setting-page">

      <h1 className="setting-header">Settings</h1>


      <div className="setting-container">
            <div className="setting-box">

              {/* Avatar Section */}
              <div className="avatar-section">

                <span className="avatar-label">Profile</span>
                <img 
                  src={avatar}
                  className="avatar-image"
                />

                <input
                  type="file"

                  // '/*' allows any file type that is an iamge 
                  accept="image/*"
                  style={{display: 'none'}}
                  ref={avatarInput}

                  onChange = {(e) => {

                    // Error handling for if the user selects multiple image files for their avatar
                    // this will just pick the first one.
                    const file = e.target.files?.[0];

                    if (file) {

                      //Creating url for the image so it can be displayed.
                      setAvatar(URL.createObjectURL(file))
                    }
                  }}

                />
                <button 
                  onClick={ ()=> avatarInput.current?.click()}
                  style={{
                    backgroundColor: '#6B4829',
                    color: 'white',
                    padding: '0.5rem 1rem',
                    border: 'none',
                    borderRadius: '8px',
                    cursor: 'pointer'
                  }}

                >Change Avatar</button>

            
            </div>

          </div>

          <div className="setting-box">

              <label>Username</label>
              {/* This is where the player user name can be changed */}
              <input type="text" defaultValue="PlayerUser"/>


          </div>


      </div>
      
     
    </div>


    </>
  );
}