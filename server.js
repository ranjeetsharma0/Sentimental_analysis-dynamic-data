const express = require('express');
const run = require('./JJ');
const app = express();
const port = 8000;
app.use(express.text())
const serveSTAT = (req, res) => {
    res.send("Hello")
}
const serveSRAT = (req, res) => {
    res.sendFile("D:/FLT/index.html")
}
app.get("/", serveSTAT)
app.get("/Stues", serveSRAT)
app.post("/Stues", async (req, res) => {

    console.log("====================================")
    console.log(req.body)
    const ans = await run(req.body)
    console.log(ans)
    
    res.send(ans)
})

app.use(express.static("D:/FLT"))
app.listen(port, () => { console.log(`listening on port${port}`); });