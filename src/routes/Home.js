import { useEffect } from "react"
import { useNavigate } from "react-router-dom"

export default function Home(){

    //Navigator
    const nav = useNavigate()

    //Custom routes for each brand button
    useEffect(() => {
        Array.from(document.getElementsByClassName("brand")).forEach(button => {
            button.addEventListener("click", (e) => {
                let brand = e.target.src.replace(".png", "")
                let split = brand.split("/")
                brand = split[split.length - 1]
                nav("/shoes", {state: {searchTerm: brand}})
            })
        })
    }, [])

    return (
        <div className = "content-center m-auto overflow-clip">

            <div className = "slidingHeader w-full h-fit p-6 pt-8 content-center relative">
                <div id = "headerInner" className = "content-center text-center bg-white w-fit h-fit m-auto border-black blackShadow px-4">
                    <div className = "hover">
                        <p className = "text-2xl header">Welcome to </p>
                        <img src = "shoetitle.png"></img>
                    </div>
                </div>

            </div>
            <div id = "headerBorder" className = "slidingBorder bg-black h-2"></div>

            <h1 className = "w-4/5 p-4 m-auto center text-center text-3xl header">
            A site to help you find the best new shoe releases from the most popular brands to resell and grow your profit</h1>

            <div className = "flex flex-column w-full m-auto p-12 items-center overflow-clip">
                <p className = "text-2xl w-1/2 pl-20">
                    Use our shoe listings scraped from your <span className = "text-red-500 font-bold italic"> favorite brand sites</span> and 
                    view our <span className = "text-red-500 font-bold italic"> machine-learning powered predictions </span>
                    on which shoes will profit you the most and help you get success as a reseller
                </p>
                <div className = "fade w-1/2 center ml-8">
                    <div className = "flex flex-row slide">
                        <img className = "brand transition-all border-black border-b-0 hover:border-b-4" src = "nike.png"></img>
                        <img className = "brand transition-all border-black border-b-0 hover:border-b-4" src = "adidas.png"></img>
                        <img className = "brand transition-all border-black border-b-0 hover:border-b-4" src = "jordan.png"></img>
                        <img className = "brand transition-all border-black border-b-0 hover:border-b-4" src = "nb.png"></img>
                    </div>
                </div>
            </div>

            <div class="flex justify-center items-center h-32">
               
            <button
                class="bg-red-500 blackShadow w-64 h-24 text-3xl transition-all hover:bg-white header"
                onClick={(e) => {
                    nav("/shoes", {state: {searchTerm: ''}})
                }}
            >
                See shoes
            </button>
            
            </div>





        </div>
    )
}