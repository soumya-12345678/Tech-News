const chat = document.getElementById("chat");
const form = document.getElementById("chat-form");
const msgInput = document.getElementById("msg");
const refreshBtn = document.getElementById("refreshBtn");

function addUserBubble(text){
  const d = document.createElement("div");
  d.className = "user-message";
  d.innerText = text;
  chat.appendChild(d);
  chat.scrollTop = chat.scrollHeight;
}

function addBotBubble(html){
  const d = document.createElement("div");
  d.className = "bot-message";
  d.innerHTML = html;
  chat.appendChild(d);
  chat.scrollTop = chat.scrollHeight;
}

async function sendMessage(){
  const text = msgInput.value.trim();
  if(!text) return false;
  addUserBubble(text);
  msgInput.value = "";
  addBotBubble("⏳ Fetching news...");
  try{
    const res = await fetch(`/api/query?date=${encodeURIComponent(text)}&summarize=1`);
    const data = await res.json();
    // remove last bot placeholder
    const bots = document.querySelectorAll(".bot-message");
    if(bots.length) bots[bots.length-1].remove();
    if(data.error){ addBotBubble("⚠️ " + data.error); return false; }
    if(!data.items || data.items.length === 0){
      addBotBubble("No technical news found for that date. Try 'today' or 'yesterday'.");
      return false;
    }
    // build HTML
    let html = "<ul style='padding-left:20px'>";
data.items.forEach(item => {
  html += `<li style="margin-bottom:12px">
    <div style="font-size:0.95rem; color:#333; margin-bottom:4px;">${item.summary}</div>
    <a href="${item.link}" target="_blank" style="font-size:0.85rem; color:#0057ff;">${item.link}</a>
  </li>`;
});
html += "</ul>";


    addBotBubble(html);
  }catch(e){
    // remove placeholder
    const bots = document.querySelectorAll(".bot-message");
    if(bots.length) bots[bots.length-1].remove();
    addBotBubble("Network error. Is the server running?");
  }
  return false;
}

refreshBtn.onclick = async ()=>{
  addBotBubble("⏳ Refreshing news from RSS...");
  try{
    const r = await fetch("/refresh");
    const j = await r.json();
    const bots = document.querySelectorAll(".bot-message");
    if(bots.length) bots[bots.length-1].remove();
    addBotBubble("Fetched " + j.count + " articles.");
  }catch(e){
    const bots = document.querySelectorAll(".bot-message");
    if(bots.length) bots[bots.length-1].remove();
    addBotBubble("Failed to refresh. Check server.");
  }
}

// allow enter to send
msgInput.addEventListener("keydown", (e)=>{
  if(e.key === "Enter" && !e.shiftKey){
    e.preventDefault();
    sendMessage();
  }
});
