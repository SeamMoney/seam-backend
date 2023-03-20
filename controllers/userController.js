const User = require('../models/user');

// get all users
exports.get_all_users = async (req, res) => {
    const users = await User.find();

    res.json(users);
};

// get specific user
exports.get_user_by_id = async (req, res) => {
    const user = await User.findById(req.params.id);
    
    res.json(user);
};