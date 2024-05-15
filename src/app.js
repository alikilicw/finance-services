const express = require('express')
const app = express()
const cors = require('cors')

app.use(express.json())
app.use(cors())


const router = require('./router')
app.use('/', router)

app.listen((5000), () => {
    console.log('Server started.');
})