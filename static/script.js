const chatToggleBtn = document.getElementById("chatToggleBtn");
const chatWidget = document.getElementById("chatWidget");
const closeChatBtn = document.getElementById("closeChatBtn");

const chatMessages = document.getElementById("chatMessages");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");

let sessionId = crypto.randomUUID();

/* Toggle chat */
chatToggleBtn.onclick = () => {
  chatWidget.style.display = "flex";
  chatToggleBtn.style.display = "none";
};

closeChatBtn.onclick = () => {
  chatWidget.style.display = "none";
  chatToggleBtn.style.display = "flex";
};

/* Add message */
function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = `message ${sender}`;
  div.innerHTML = marked.parse(text);
  chatMessages.appendChild(div);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

/* Send message */
async function sendMessage() {
  const text = userInput.value.trim();
  if (!text) return;

  addMessage(text, "user");
  userInput.value = "";

  addMessage("Thinking...", "bot");

  try {
    const res = await fetch("/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        text,
        session_id: sessionId
      })
    });

    const data = await res.json();

    chatMessages.lastChild.remove();

    addMessage(data.response || "No response", "bot");
  } catch (err) {
    chatMessages.lastChild.remove();
    addMessage("Error connecting to server", "bot");
  }
}

/* Events */
sendBtn.onclick = sendMessage;
userInput.addEventListener("keydown", e => {
  if (e.key === "Enter") sendMessage();
});
