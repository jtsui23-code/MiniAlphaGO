
export default function Nav(){
    // Minit color nav bar
    // return (<nav className="bg-gradient-to-r from-green-300 via-teal-300 to-emerald-400">


    // Dark blue nav bar
    // return (<nav className="bg-gradient-to-r from-gray-900 via-indigo-800 to-blue-700>


    // return (<nav className="bg-gradient-to-r from-orange-500 via-pink-500 to-red-500">
    {/* // return (<nav className="bg-gradient-to-r from-blue-800 via-blue-600 to-indigo-500">
    // return (<nav className="bg-gradient-to-r from-indigo-800 via-purple-700 to-fuchsia-600">
    // return (<nav className="bg-gradient-to-r from-yellow-800 via-yellow-700 to-yellow-600 shadow-md sticky top-0 z-50 w-full"> */}

    
    // Zen theme
    return (<nav className="bg-gradient-to-r from-stone-200 via-amber-100 to-stone-300 text-gray-800">

    {/* // return (<nav className="bg-gradient-to-r from-gray-900 via-gray-800 to-gray-700 text-lime-400"> */}
    
    {/* dawn theme */}
    {/* return (<nav className="bg-gradient-to-r from-yellow-700 via-rose-300 to-red-300 text-white"> */}

    
    {/* Dark theme
    return (<nav className="bg-gradient-to-r from-zinc-900 via-zinc-700 to-neutral-600 text-white">*/}





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