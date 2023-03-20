const express = require("express");
const router = express.Router();

// GET home page.
router.get("/", function (req, res) {
    res.send("This is SeamMoney backend!");
});

module.exports = router;