import Image from "next/image";
import Nav from "@/components/nav";
import Board
 from "@/components/board";
export default function Home() {
  return (
  <>
    <Nav/> 
    <div  className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-20 gap-16 sm:p-20 font-[family-name:var(--font-geist-sans)]">
      <p>This is the play page</p> 

      
      <Board/>
    </div>
    </>
  );
}
