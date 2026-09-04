const mongoose = require("mongoose");

async function connectDB() {
    const mongoUri = process.env.MONGODB_URI || "mongodb://localhost:27017/edumind";
    await mongoose.connect(mongoUri);
    console.log("Connected to DB");
}

module.exports = connectDB;