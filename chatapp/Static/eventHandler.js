var clientSocket = io();

function handleMessage(){
    var msgTextArea = document.getElementById("messageBox");
    if (!(msgTextArea.value)){
        return;
    }
    user = document.getElementById("msgButton");
    clientSocket.emit("message", {data: msgTextArea.value, sender: msgTextArea.name, reciever: user.name});
    alert("sent");
    msgTextArea.value = "";
}

clientSocket.on("connect", function(){
})

clientSocket.on("message", function(data){
    document.write(data);
})