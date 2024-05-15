const router = require('express').Router()
const stockSearch = require('./stocks.controller')

router.get('', async (req, res) => {
    res.send({'denemeeee': 'ddwafawf'}).status(200)
})

router.get('/stock-search', stockSearch)

module.exports = router




