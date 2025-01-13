export default function ShoeCard(shoe){
    const data = shoe.shoe

    //Fitting name
    let name = "", split = data.name.split(" "), length = 0, max = 20
    let i = 0
    while(length < max){
        if(name.length + split[i].length + 1 <= max){
            name += split[i] + " "
            length = name.length
            i ++
        }
        else{
            length = max
        }
    }

    return (
        <div 
        className = "hover:cursor-pointer w-56 h-56 blackShadow border-slate-300 border-2 m-4 overflow-clip center text-center slideOnHover transition-all duration-175 hover:scale-105">
            <img src = {data.img_link} className = "w-40 h-40 m-auto border-slate-100 border-2"></img>
            <p className = "header text-md w-48 m-auto">{name}</p>
            <div className = "flex flex-row mx-2">
                <img src = {data.brand.toLowerCase() + ".png"} className = "w-8 h-8"></img>
                <div className = "w-44 m-auto"></div>
                <p className = "text-green-600">{`$${parseInt(data.predicted_price - data.price)}`}</p>
            </div>
        </div>
    )
}