
export default function Nav(){
    return (<nav className="bg-gradient-to-r from-indigo-300 via-purple-300 to-pink-300 shadow-lg sticky top-0 z-50 w-full">


            <div className="flex justify-between items-center px-10 py-6 w-full text-black font-semibold text-lg">
                    <a href="/" className = "hover:text-white transition-colors"> Home </a>

                <div className="space-x-6 text-black-600 font-medium"> 
                    

                    <a href="https://online-go.com/play" className = "hover:text-white transition-colors"> Play </a>
                    <a href="/stats" className= "hover:text-white transition-colors"> Stats </a>
                    <a href="/settings" className = "hover:text-white transition-colors"> Settings </a>

                </div>
            </div>

        
    </nav>
    
    );
}