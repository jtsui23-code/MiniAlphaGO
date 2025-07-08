import Image from "next/image";
import Nav from "@/components/nav";
import Board
 from "@/components/board";

export default function Stats() {
  return (
  <>
    <Nav/> 
    <div  className="max-6xl mx-auto p-8">
      <div className="flex flex-col md:flex-ro items-center md:items-start gap-6 mb-10">

        <Image
          src="/profile-placeholder.png"
          alt="Profile"
          width={100}
          height={100}
          className="rounded-full border-2 border-gray-300"
        />

        <div>

          <h1 className="text-3x1 font-bold">
            Your Username

          </h1>

          <p className="text-gray-600"> 
            Rank: Dan 5
          </p>

          <p className="text-gray-500 text-sm">

            Member since July 8th 2025

          </p>
        </div>
      </div>

 
      {/* Stats Summary */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-center mb-10">
          <div className="bg-white shadow-md p-4 rounded-lg">

            <h3 className="text-xl font-semibold text-green-700">
              Wins
            </h3>

            <p className="text-2x1 font-bold">12</p>

          </div>


          <div className="bg-white shadow-md p-4 rounded-lg">


            <h3 className="text-xl font-semibold text-red-700">
              Losses
            </h3>

            <p className="text-2xl font-bold">8</p>

          </div>

          <div className="bg-white shadow-md p-4 rounded-lg">

            <h3 className="text-xl font-semibold text-indigo-700">
              Win Rate

            </h3>

            <p className="text-2xl font-bold">
              60%
            </p>
          </div>



      </div>






      
      <Board/>
    </div>
    </>
  );
}
