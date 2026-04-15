const messages = document.getElementById("messages");
const inputField = document.getElementById("userInput");
const micBtn = document.getElementById("micBtn");

function addMessage(text, className) {
    const messageDiv = document.createElement("div");
    messageDiv.className = "message " + className;
    messageDiv.textContent = text;
    messages.appendChild(messageDiv);
    messages.scrollTop = messages.scrollHeight;
}

function sendMessage() {
    const input = inputField.value.trim();
    if (input === "") return;

    addMessage(input, "user-message");

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: input })
    })
        .then(response => response.json())
        .then(data => {
            addMessage(data.response, "bot-message");
            speak(data.response);
        })
        .catch(error => {
            addMessage("Error connecting to server.", "bot-message");
            console.error("Error:", error);
        });

    inputField.value = "";
}

function startListening() {
    if (!('webkitSpeechRecognition' in window)) {
        alert("Speech recognition is not supported in this browser.");
        return;
    }

    const recognition = new webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    micBtn.innerHTML = "🎙️";
    micBtn.style.backgroundColor = "rgb(77, 255, 77)";
    micBtn.style.color = "#fff";
    micBtn.style.boxShadow = "0 0 15px rgba(77, 255, 77, 0.8)";
    micBtn.style.transform = "scale(1.1)";

    recognition.start();

    recognition.onresult = function (event) {
        const speechText = event.results[0][0].transcript;
        inputField.value = speechText;

        setTimeout(() => {
            sendMessage();
        }, 300);
    };

    recognition.onend = function () {
        resetMicButton();
    };

    recognition.onerror = function (event) {
        console.error("Speech recognition error:", event.error);
        resetMicButton();
    };
}

function resetMicButton() {
    micBtn.innerHTML = "🎤";
    micBtn.style.backgroundColor = "#2f4f88";
    micBtn.style.color = "#fff";
    micBtn.style.boxShadow = "none";
    micBtn.style.transform = "scale(1)";
}

function speak(text) {
    const speech = new SpeechSynthesisUtterance(text);

    function setVoice() {
        const voices = speechSynthesis.getVoices();
        speech.voice = voices.find(v => v.lang === "en-US") || voices[0];
        speech.rate = 0.95;
        speech.pitch = 1.05;

        speechSynthesis.cancel();
        speechSynthesis.speak(speech);
    }

    if (speechSynthesis.getVoices().length === 0) {
        speechSynthesis.onvoiceschanged = setVoice;
    } else {
        setVoice();
    }
}

window.onload = function () {
    const welcomeMessage = "Welcome to BingoAI! How may I assist you today?";
    addMessage(welcomeMessage, "bot-message");
    speak(welcomeMessage);
};

inputField.addEventListener("keypress", function (event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});