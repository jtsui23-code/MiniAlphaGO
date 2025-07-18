'use client';
import Image from "next/image";
import './setting.css'
import Nav from "@/components/nav";
import {useState} from 'react';


export default function Home() {

  const [avatar, setAvatar] = useState("/default-avatar.png")

  return (
  <>
    <Nav/> 

    {/* Add justify-center here to center vertically */}
    <div className="setting-page">

      <h1 className="setting-header">Settings</h1>
      <p className="setting-header">Customize your Go Journey</p>


      <div className="setting-container">
            <div className="setting-box">

              {/* Avatar Section */}
              <div className="avatar-section">

                <img 
                  src={avatar}
                  alt="User Avatar"
                  className="avatar-image"
                />

                <input
                  type="file"

                  // '/*' allows any file type that is an iamge 
                  accept="image/*"

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



            </div>
            
          </div>


      </div>
      
     
    </div>


    </>
  );
}