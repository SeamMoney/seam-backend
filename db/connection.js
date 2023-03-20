const mongoose = require('mongoose');
require('dotenv').config();

function connectToDatabase() {
    mongoose.connect(process.env.MONGODB_URI, {
        useNewUrlParser: true,
        useUnifiedTopology: true,
    });
    console.log('MongoDB successfully connected')
}

module.exports = {
    connectToDatabase: connectToDatabase,
};