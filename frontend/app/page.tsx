import Image from "next/image";
import Nav from "@/components/nav";
import Board
 from "@/components/board";
export default function Home() {
  return (
   
    <div  className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
       <Nav></Nav> 
      <h1>Daniel (The legendary Programmer) and Jack (The talented vibe coder) went hand in hand to create this powerful product.</h1>
      <p>It's blank now. let's get to work</p>

      
      <Board></Board>
    </div>

  );
}
