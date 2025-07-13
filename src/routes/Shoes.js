import { useState, useEffect } from "react"
import { useLocation } from "react-router-dom"
import axios from "axios"
import ShoeCard from "../components/ShoeCard"
import ShoeModal from "../components/ShoeModal"

export default function Shoes(){

    //Location
    const loc = useLocation()
    const content = loc.state.searchTerm

    //Fetching data and storing it in state
    const [shownShoeData, setShownShoeData] = useState([])
    const [allShoeData, setAllShoeData] = useState([])
    const [modalShoeData, setModalShoeData] = useState({})
    
    let shoeData = []
    const uri = "/api/data"
    //const uri = "http://52.201.252.200:80/data"

    useEffect(() => {

        //Fetchcing 
        axios.get(uri).then(res => {
            if(res.data){ res = res.data }
            delete res.Unnamed
            for(let i = 0; i < Object.keys(res.brand).length; i ++){
                let data = {
                    brand: res.brand[i],
                    img_link: res.img_link[i],
                    link: res.link[i],
                    name: res.name[i],
                    price: res.price[i],
                    predicted_price: res.predicted_prices[i],
                    release_date: res.release_date[i]
                }
                if(data.brand == "adidas"){
                    data.link = "https://adidas.com" + data.link
                }
                shoeData.push(data)
            }
            setShownShoeData(shoeData)
            setAllShoeData(shoeData) //This is just for a constant reference of the data

            //Using the filter from brand 
            if(content.length != 0){
                document.getElementById("searchBar").value = content
                setShownShoeData(allShoeData.filter(x => x.name.toLowerCase().includes(content.toLowerCase())))
            }
    

        }).catch(err => {
           console.log(err)
        })
        
    }, [])
    


    return (
        <div>
            <div id = "page">
                <div className = "slidingHeader w-full h-fit p-6 pt-8 content-center relative">
                    <div id = "headerInner" className = "content-center text-center bg-white w-fit h-fit m-auto border-black blackShadow px-4">
                        <div className = "hover">
                            <img src = "allShoes.png"></img>
                        </div>
                    </div>

                </div>
                <div id = "headerBorder" className = "slidingBorder bg-black h-2"></div>

                <input type = "text" id = "searchBar" className = "w-3/4 h-12 border-2 border-black m-4 p-4" onChange={(e) => {
                    //Handling filter
                    if(e.target.value.length == 0){
                        setShownShoeData(allShoeData)
                    }
                    else{
                        setShownShoeData(allShoeData.filter(x => x.name.toLowerCase().includes(e.target.value)))
                    }
                }}></input>

                <div id = "allShoes" className = "px-8 flex flex-row flex-wrap">
                {shownShoeData.map((shoe, index) => (
                    <div key = {index} onClick={(e) => {
                        document.getElementById('page').style.opacity = '20%'
                        window.scrollTo(0, 0)
                        setModalShoeData(shoe)
                    }}>
                     <ShoeCard shoe = {shoe}></ShoeCard>
                    </div>
                ))}

                </div>
            </div>

            <ShoeModal shoe = {modalShoeData} revert = {() => {
                document.getElementById("page").style.opacity = '100%'
                setModalShoeData({})
                }}></ShoeModal>
        </div>
    )
}
