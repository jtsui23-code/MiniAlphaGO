import Image from "next/image";
import Nav from "@/components/nav";
import Board
 from "@/components/board";

export default function Stats() {
  return (

  // <> Allows to return multiple jsx components i.e the div's etc
  <>
    <Nav/> 

    {/* max-6xl gives content a max width of 6xl  */}
    {/* mx-auto centers the container */}
    {/* p-8 creates a padding of 2rem */}
    <div  className="max-6xl mx-auto p-8">

      {/* flex makes a flex container */}
      {/* flex-col uses vertical stacking */}
      {/* md:flex-w switches to horizontal layout on medium+ screens */}
      {/* item-center centers items vertically by default */}
      {/* md:items-start aligns to the top on larger screens */}
      {/* gap-6 1.5rem space between each item */}
      <div className="flex flex-col md:flex-row items-center md:items-start gap-6 mb-10">

        <Image
          // src is temporary and will be replaced when have real user avatars
          src="/profile-placeholder.png"

          alt="ProfilePage"
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

      {/* grid-cols-1 means that by default there is only 1 column */}
      {/* sm:grid-cols-3 whenever there screen is small and up it uses 3 columns */}
      {/* gap-4 puts spacing between stats card */}
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

       {/* Recent Games Table */}
          
          <div className="flex justify-center">

          
          {/* Full-width table with soft padding and white card-style background */}
          <div className="w-full max-w-4xl mx-auto bg-white shadow-md rounded-lg overflow-hidden">

            <table className="min-w-full text-sm">

              {/* thead is table header */}
              <thead className="bg-gray-100 text-gray-700">

                  {/* tr - table row */}
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

                {/* Creates array with 5 items that are all undefined at the start */}
                {/* The _ in .map((_, i)) is the contend in the Array so like Array[1] or Array[3] etc 
                which is going to be undefined at first so its just a _  */}
                {/* This loops through the array and returns 5 <tr> elements */}

                {[...Array(5)].map((_, i) =>(

                    // Need a key for rendering the <tr> elements that are returned from the loop
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
