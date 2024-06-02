const axios = require('axios')
require("dotenv").config()

const main = async (req, res) => {

    const {stock} = req.query

    try {
    
        if(!stock) throw new Error('Please send a stock code.')
        const stockCode = stock
        
        const financial_table_res = await axios.get(`${process.env.WEB_SCRAPE_HOST}:5002/financial-table?stock_code=${stockCode}`);
        const financial_table_data = financial_table_res.data

        console.log(financial_table_data, 'financial_table_data')

        const news_res = await axios.post(`${process.env.WEB_SCRAPE_HOST}:5002/news`, 
            {
                'stock_code': financial_table_data['stock_code'],
                'periods': financial_table_data['periods']
            }
        );
        const news_data = news_res.data

        const nlp_res = await axios.post(`${process.env.NLP_HOST}:5003/nlp`,
            {
                'news': news_data
            }
        );
        const nlp_data = nlp_res.data

        financial_table_data['first_period_news_value'] = nlp_data['first_period_news_value']
        financial_table_data['second_period_news_value'] = nlp_data['second_period_news_value']
        financial_table_data['third_period_news_value'] = nlp_data['third_period_news_value']

        const ai_res = await axios.post(`${process.env.NLP_HOST}:5003/ai`,
            {
                'data': [financial_table_data]
            }
        );
        const ai_data = ai_res.data

        financial_table_data['guessed_fouth_period_price'] = ai_data['guessed_value']

        res.json(financial_table_data).status(200)
        
    } catch (error) {
        console.error('Error fetching data:', error);
        res.send('hata').status(400)
    }

}


module.exports = main