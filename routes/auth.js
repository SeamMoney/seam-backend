const express = require("express");
const router = express.Router();

// Require controller modules.
const auth_controller = require("../controllers/authController");

// signin
router.post('/login', auth_controller.signin);

// signup
router.post('/register', auth_controller.signup);

module.exports = router;