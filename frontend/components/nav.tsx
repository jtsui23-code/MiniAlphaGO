export default function Nav(){
    return (<nav className="bg-white shadow-md sticky top-0 z-50 w-full">


            <div className="flex justify-between items-center px-10 py-10 w-full">

            
                <div className="space-x-6 text-gray-600 font-medium"> 
                    
                    <a href="/" className = "hover:text-black transition-colors"> Home </a>

                    <a href="https://online-go.com/play" className = "hover:text-black transition-colors"> Play </a>
                    <a href="/stats" className= "hover:text-black transition-colors"> Stats </a>
                    <a href="/Settings" className = "hover:text-black transition-colors"> Settings </a>

                </div>
            </div>

        
    </nav>
    
    );
}