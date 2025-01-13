export default function ShoeModal(props){

    //Conditionally render an absolute position modal based on whether theres data
    const data = props.shoe, revert = props.revert
    console.log(revert)
    if(Object.keys(data).length > 0){
        return (
            <div className = "absolute inset-0 scale-75 border-black p-8 bg-white blackShadowBig border-2 overflow-clip">
                <a>
                <p className = "text-5xl transition-all text-red-500 hover:text-red-900 float-right hover:cursor-pointer" onClick={(e) => {
                    revert()
                }}>x</p>
                </a>

                <h1 className = "header w-fit h-fit bg-white text-4xl">{data.name}</h1>
                <div className="flex flex-row mt-8">
                    <img src = {data.img_link} className = "w-5/12 h-5/12 border-black blackShadow border-2 m-8"></img>
                    <div className = "ml-8 text-3xl">
                        <img src = {data.brand.toLowerCase() + ".png"} className = "w-24 h-24"></img>
                        <p>Releases {data.release_date}</p>
                        <p>Drops at ${data.price}</p>
                        <p>Predicted to resell for ${parseInt(data.predicted_price)} 
                            <span className = "text-green-600"> (${parseInt(data.predicted_price - data.price)} profit)</span></p>


                        <a className = "text-red-500 hover:text-red-900 mt-24" href = {data.link}>Go to shoe</a>
                    </div>
                </div>

            </div>
        )
    }
    else{
        return (
            <div></div>
        )
    }
}