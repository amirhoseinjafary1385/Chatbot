function sendMessage() {
    var userInput = document.getElementById("user-input").value;
    if (userInput !== "") {
        var chatBox = document.getElementById("chat-box");
        var userMessage = document.createElement("div");
        userMessage.className = "user-message";
        userMessage.innerHTML = "<strong>You:</strong> " + userInput;
        chatBox.appendChild(userMessage);
        document.getElementById("user-input").value = "";

        // Send user message to the server
        fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                message: userInput,
            }),
        })
        .then(response => response.json())
        .then(data => {
            setTimeout(() => {
                var botMessage = document.createElement("div");
                botMessage.className = "bot-message";
                botMessage.innerHTML = "<strong>Bot:</strong> " + data.message;
                chatBox.appendChild(botMessage);
                chatBox.scrollTop = chatBox.scrollHeight;
            }, 1000);
        })
        .catch(error => console.error("Error:", error));
    }
}
