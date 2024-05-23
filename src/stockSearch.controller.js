const fs = require('fs')
const path = require('path');


const stockSearch = async (req, res) => {

    const { stock } = req.query

    try {

        if(!stock) throw new Error('Please send stock.')

        const stockCodes = fs.readFileSync('./data/stock_codes.json', 'utf-8')
        const stockCodes_ = new Object(JSON.parse(stockCodes))
    
        const avaliableStockCodes = fs.readFileSync('./data/avaliable_stock_codes.json', 'utf-8')
        const avaliableStockCodes_ = JSON.parse(avaliableStockCodes)
        
    
        const stockKeys = Object.keys(stockCodes_)
        
        var output = []
        stockKeys.forEach(item => {
            var stock_ = new Object()
            if(stockCodes_[item].toLowerCase().startsWith(stock.toLowerCase()) || item.toLowerCase().startsWith(stock.toLowerCase())) {
                stock_['code'] = item
                stock_['name'] = stockCodes_[item]
    
                stock_['state'] = (avaliableStockCodes_.includes(item)) ? 1 : 0
    
                output.push(stock_)
            } 
        });

    } catch(error) {
        res.json({'message': error.message}).status(400)
    }


    res.json(output).status(200)
}

module.exports = stockSearch