var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var multer = require('multer');
var storage = multer.diskStorage({
  destination: function(req, file, cb) {
    cb(null, __dirname + "/uploads/");
  },
  filename: function(req, file, cb) {
    cb(null, file.fieldname + '-' + Date.now());
  }
});
var upload = multer({storage: storage});
var stream = require("stream");

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

var searchFields = upload.fields([{name: "image-upload", maxCount: 1},
                                  {name: "sorting-method", maxCount: 1},
                                  {name: "lat"},
                                  {name: "lon"},
                                  {name: "address", maxCount: 1}]);
app.post('/search/analyze', searchFields, function(req, res, next) {
  /* Cover form data to JSON, upload image
   * Run python script with JSON input
   * Get JSON with list of matches
   * Use this JSON on template
   */
  res.json({"image-url": req.files["image-upload"][0]["path"],
            "sorting-method": req.body["sorting-method"],
            "latitude": req.body["lat"],
            "longitutde": req.body["lon"],
            "address": req.body["address"]});
});

app.post('/add/analyze', upload.fields([{name: "image-upload", maxCount: 1}, {name: "restaurant-name", maxCount: 1}, {name: "restaurant-address", maxCount: 1}]), function(req, res, next) {
  /* Convert form data to JSON, upload image
   * Run python script with JSON input
   * Get JSON with success
   * Load success page
   */
  res.json({"image-url": req.files["image-upload"][0]["path"],
            "restaurant-name": req.body["restaurant-name"],
            "restaurant-address": req.body["restaurant-address"]});
})

app.use('/', indexRouter);
app.use('/users', usersRouter);

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

module.exports = app;
