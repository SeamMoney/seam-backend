const User = require('../models/user');
const bcrypt = require("bcrypt");
const owasp = require('owasp-password-strength-test');
const jwt = require("jsonwebtoken");
require('dotenv').config();

// check user credentials and return token
exports.signin = async (req, res) => {
    const { username, password } = req.body;
    
    // Check if user exists in database
    const user = await User.findOne({ username });
    if (!user) {
        return res.json({ error: 'No username registered!' });
    }
    
    // Check if password is correct
    const passwordMatch = await bcrypt.compare(password, user.password);
    if (!passwordMatch) {
        return res.json({ error: 'Invalid login credentials!' });
    }
    
    // Generate token and send it back to client
    const token = jwt.sign({ userId: user._id }, process.env.JWT_SECRET_KEY);
    
    res.json({ token });
};

// create a new user
exports.signup = async (req, res) => {
    const { username, password, confirmPassword } = req.body;
    
    if (!username || !password) {
        return res.json({ message: 'Username and password are required' });
    }
    // Check if user exists in database
    const userCheck = await User.findOne({ username });
    if (userCheck) {
        return res.json({ error: 'Username already exists!' });
    }
    
    // Check if passwords match
    if (password !== confirmPassword) {
        return res.json({ error: 'Passwords do not match!' });
    }
    
    // Check password strength
    if (!owasp.test(password).strong) {
        return res.json({ error: 'Password is not strong enough!' });
    }
    
    const user = new User({ username, password });
    await user.save();
    
    res.json({ message: 'User created successfully' });
};