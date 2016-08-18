var http = require('http');
var url = require('url');
var fs = require('fs');
var path = require('path');
var baseDirectory = __dirname;

var MongoClient = require('mongodb').MongoClient;
var assert = require('assert');
var ObjectId = require('mongodb').ObjectID;
var MONGO_URI = process.env.MONGO_URI;

var port = 9615;

var GOOGLE_MAPS_API_KEY = process.env.GOOGLE_MAPS_API_KEY;

function findConcerts(db, callback) {
    var cursor = db.collection('concerts').find();
    cursor.each(function(err, doc) {
        assert.equal(err, null);
        if (doc != null) {
            console.dir(doc);
        } else {
            callback();
        }
    });
};

http.createServer(function (request, response) {
   try {
     var requestUrl = url.parse(request.url);

     // need to use path.normalize so people can't access directories underneath baseDirectory
     var fsPath = baseDirectory + path.normalize(requestUrl.pathname);
     
     //MongoClient.connect(MONGO_URI, function(err, db) {
     //  assert.equal(null, err);
     //   findConcerts(db, function() {
     //       db.close();
     //   });
     //});

     response.writeHead(200);
     var fileStream = fs.createReadStream(fsPath);
     fileStream.pipe(response);
     fileStream.on('error',function(e) {
         response.writeHead(404)     // assume the file doesn't exist
         response.end()
     });
   } catch(e) {
     response.writeHead(500);
     response.end();     // end the response so browsers don't hang
     console.log(e.stack);
   }
}).listen(port);

console.log("listening on port " + port);
