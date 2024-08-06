const express = require("express")
const axios = require("axios")
const cron = require("node-cron")

const api_link = "https://shoe-price-api.onrender.com/data"
const app_link = "https://shoe-price-app.onrender.com" //For refreshing the server

const app = express()
app.set("view engine", "ejs")
app.use(express.static(__dirname + "/public"))


axios.get(api_link).then(res => {
    console.log(res.data)
})

app.get('/', (req, res) => {
    axios.get(api_link).then(api_res => {
        console.log(api_res.data)
        res.render("index", {data : JSON.stringify(api_res.data)})
    }).catch(err => {
        res.render("index", {data : {"Error" : err}})
    })
})

cron.schedule('* */5 * * *', () => {
    axios.get(app_link).then(res => {
        console.log("Pinged server")
    })
});


app.listen(5000, () => {
    console.log("Server listening on http://127.0.0.1:5000")
})
