const express = require("express");
const app = express();

// Configuring port
const port = process.env.PORT || 9000;

// respond with "hello world" when a GET request is made to the homepage
app.get("/", (req, res) => {
  res.send("hello world trigger");
});

// Listening to port
app.listen(port);
console.log(`Listening On http://localhost:${port}/api`);

module.exports = app;
