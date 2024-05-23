const router = require('express').Router()
const stockSearch = require('./stockSearch.controller')
const main = require('./main.controller')

router.get('', async (req, res) => {
    res.send({'denemeeee': 'ddwafawf'}).status(200)
})

router.get('/stock-search', stockSearch)
router.get('/get-guessed-price', main)

module.exports = router