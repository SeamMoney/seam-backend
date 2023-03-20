const express = require("express");
const router = express.Router();

// Require controller modules.
const user_controller = require("../controllers/userController");

// get all users
router.get('/', user_controller.get_all_users);

// get one user
router.get('/:id', user_controller.get_user_by_id);

module.exports = router;