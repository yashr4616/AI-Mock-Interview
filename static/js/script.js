function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    let chatBox = document.getElementById("chat-box");

    if (userInput.trim() === "") return;

    // Append user message
    chatBox.innerHTML += `<p class="user-msg"><strong>You:</strong> ${userInput}</p>`;

    // Send request to Flask backend
    fetch("/get_response", {
        method: "POST",
        body: JSON.stringify({ message: userInput }),
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        // Append chatbot response
        chatBox.innerHTML += `<p class="bot-msg"><strong>Bot:</strong> ${data.response}</p>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    });

    document.getElementById("user-input").value = "";
}

const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = 'en-US';
recognition.interimResults = false;
recognition.maxAlternatives = 1;

document.addEventListener("keydown", function (event) {
    // Start listening when user presses the spacebar
    if (event.code === "Space") {
        recognition.start();
    }
});

recognition.onresult = function (event) {
    const voiceInput = event.results[0][0].transcript;
    document.getElementById("user-input").value = voiceInput;
    sendMessage(); // Automatically send message after voice input
};

function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    utterance.rate = 1;
    speechSynthesis.speak(utterance);
}

function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    let chatBox = document.getElementById("chat-box");

    if (userInput.trim() === "") return;

    // Append user message
    chatBox.innerHTML += `<p class="user-msg"><strong>You:</strong> ${userInput}</p>`;

    fetch("/get_response", {
        method: "POST",
        body: JSON.stringify({ message: userInput }),
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        chatBox.innerHTML += `<p class="bot-msg"><strong>Bot:</strong> ${data.response}</p>`;
        chatBox.scrollTop = chatBox.scrollHeight;
        speak(data.response); // Speak out the bot's response
    });

    document.getElementById("user-input").value = "";
}
