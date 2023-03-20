const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const userSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
    unique: true,
    trim: true
  },
  password: {
    type: String,
    required: true,
    trim: true
  }
});

//Hashing password before saving
userSchema.pre("save", function(next){
  let user = this;
  bcrypt.hash(user.password, 10, function(err, hash){
      if (err) return next(err);
      user.password = hash;
      next();
  })
});

// Compare entered password with the hashed password
userSchema.methods.comparePassword = function(candidatePassword, callback){
  bcrypt.compare(candidatePassword, this.password, function(err, isMatch){
      if (err) return callback(err);
      callback(null, isMatch);
  });
};

const User = mongoose.model('users', userSchema);
module.exports = User;