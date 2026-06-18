// Game routes code goes here
const express = require('express');
const router = express.Router();

router.get('/status', (req, res) => {
  res.json({ status: 'Game is running' });
});

module.exports = router;