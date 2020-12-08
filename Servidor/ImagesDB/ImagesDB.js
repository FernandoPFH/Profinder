var express = require('express');
var socket = require("socket.io");
var fs = require('fs');
var path = require('path');
const { exec } = require("child_process");

var app = express();
var server = app.listen(5000);

console.log(`My socket server is running`);

var io = socket(server);

app.use('/', express.static(__dirname + '/public'));

app.use('/static', express.static(__dirname + '/public/images'));

io.sockets.on('connection', (socket) => {
    console.log("New Connection: " + socket.id);

    socket.on('ImageSend', (data)=>{
        var tryingFile = true;
        var filename = data.filename;

        while (tryingFile) {
            if(fs.existsSync(path.join(__dirname,'/public/images',filename))) {
                filename = `a${filename}`;
            } else {
                tryingFile = false;
                fs.writeFile(path.join(__dirname,'/public/images',filename),new Buffer.from(data.filedata.replace(/^data:image\/\w+;base64,/, ""),"base64"),()=>{});
            }
        }

        var data = {
            IP : "192.168.15.181",
            urlprefix: 'static',
            filename : filename
        };

        socket.emit('Response', data);
    });

    socket.on('ImageDelete', (data) => {
        if(fs.existsSync(path.join(__dirname,'/public/images',data.filename))) {
            fs.unlink(path.join(__dirname,'/public/images',data.filename),()=>{})
        }
    });
});