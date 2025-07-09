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


          {/* Recent Games Table */}
          <div className="bg-white shadow-md rounded-lg overflow-hidden">

            <table className="min-w-full text-sm">
              <thead className="bg-gray-100 text-gray-700">

                  <tr>

                    <th className="px-6 py-3 text-left">
                      Opponent
                    </th>
                  
                    <th className="px-6 py-3 text-left">
                      Result
                    </th>

                    <th className="px-6 py-3 text-left">
                      Moves
                    </th>

                    <th className="px-6 py-3 text-left">

                      Dates
                    </th>

                    <th className="px-6 py-3">

                      Replay
                    </th>


                  </tr>
              </thead>

              <tbody>
                {[...Array(5)].map((_, i) =>(
                    <tr key={i} className="border-b hover:bg-gray-50">

                      <td className="px-6 py-4">AI v{i}</td>
                      <td className={`px-6 py-4 %{i % 2 == 0 ? "text-green-600" :"text-red-600"}`}>

                        {i % 2 === 0 ? "Win" : "Loss"}
                      </td>

                      <td className="px-6 py-4">{40 + i}</td>
                      <td className="px-6 py-4">2025-07-0{i + 1}</td>
                      <td className="text-center px-6 py-4">

                        <button className="text-blue-500 hover:underline">View</button>
                      </td>
                    </tr>


                ))}


              </tbody>
            </table>
          </div>


      </div>






      
      <Board/>
    </div>
    </>
  );
}
