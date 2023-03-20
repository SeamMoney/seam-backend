const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const db = require('./db/connection');
const authRouter = require("./routes/auth");
const userRouter = require("./routes/user");
const defaultRouter = require("./routes/index");

const app = express();
const port = process.env.PORT || 3030;

app.use(cors({
  origin: '*',
  methods: ['GET', 'POST']
}));
app.use(bodyParser.json());

app.use("/", defaultRouter);
app.use("/auth", authRouter);
app.use("/users", userRouter);

db.connectToDatabase();
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});

module.exports = app;