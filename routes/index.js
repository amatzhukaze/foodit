var express = require('express');
var router = express.Router();

router.get('/', function(req, res, next) {
  /* Home/landing page */
  res.render("index", { "title": "foodit" });
});

router.get('/search', function(req, res, next) {
  /* image analysis page */
  res.render("search", { "title": "foodit" });
});

router.get('/add', function(req, res, next) {
  /* user contribution page */
  res.render("add", { "title": "foodit"} );
});

router.post('/add/analyze', function(req, res, next) {
  res.send("/add/analyze")
})

module.exports = router;
