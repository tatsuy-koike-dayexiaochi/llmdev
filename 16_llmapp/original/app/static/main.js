const STORAGE_KEY = "chat-bot-lesson-16";

function loadMessages() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
  } catch {
    return [];
  }
}

function saveMessages(messages) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
}

function scrollToBottom() {
  const chat = document.getElementById("chat-box");
  chat.scrollTop = chat.scrollHeight;
}

function render(messages) {
  const chat = document.getElementById("chat-box");
  chat.innerHTML = "";

  for (const m of messages) {
    const div = document.createElement("div");
    div.className = `msg ${m.role}`;

    if (m.role === "user") {
      div.textContent = m.content;
    } else {
      // Markdown -> HTML -> sanitize
      const html = marked.parse(m.content || "");
      div.innerHTML = DOMPurify.sanitize(html);
      div.classList.add("markdown");
    }

    chat.appendChild(div);
  }

  scrollToBottom();
}

async function postJson(url, body) {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body || {}),
  });

  const data = await res.json().catch(() => ({}));
  return { res, data };
}

document.addEventListener("DOMContentLoaded", async function () {
    const inputEl = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-button");
    const clearBtn = document.getElementById("clear-button");

  let messages = loadMessages();

  // ---------- 初期状態チェック ----------
  const EPOCH_KEY = STORAGE_KEY + ":epoch";
  try {
    const statusRes = await fetch("/app/status");
    const statusData = await statusRes.json();

    const prevEpoch = localStorage.getItem(EPOCH_KEY);
    if (prevEpoch && prevEpoch !== statusData.server_epoch) {
      // サーバー再起動を検知 → ローカル履歴を消す
      localStorage.removeItem(STORAGE_KEY);
      messages = [];
    }
    localStorage.setItem(EPOCH_KEY, statusData.server_epoch);

    if (!statusData.rag_ready) {
      messages.push({
        role: "system",
        content:
          "RAG index が未作成です。CLIで ingest を実行してください。",
      });
    }
  } catch (err) {
    console.error("Failed to fetch rag status:", err);
  }
  saveMessages(messages);
  render(messages);

  // ---------- 送信処理 ----------
  async function sendMessage() {
    const text = (inputEl.value || "").trim();
    if (!text) return;

    // ユーザー表示
    messages.push({ role: "user", content: text });
    saveMessages(messages);
    render(messages);

    inputEl.value = "";

    // ローディング表示
    messages.push({ role: "assistant", content: "..." });
    render(messages);

    const loadingIndex = messages.length - 1;

    const { res, data } = await postJson("/ask", { query: text });

    if (res.status === 409) {
      messages[loadingIndex] = {
        role: "system",
        content:
          "RAG index が未作成です。CLIで ingest を実行してください。",
      };
      saveMessages(messages);
      render(messages);
      return;
    }

    if (!res.ok) {
      messages[loadingIndex] = {
        role: "system",
        content: data.error || "エラーが発生しました。",
      };
      saveMessages(messages);
      render(messages);
      return;
    }

    // 正常応答
    messages[loadingIndex] = {
      role: "assistant",
      content: data.answer || "",
    };

    saveMessages(messages);
    render(messages);
  }
  sendBtn.addEventListener("click", sendMessage);

  // Ctrl + Enterが押された場合
  inputEl.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && e.ctrlKey) {
      e.preventDefault();
      sendMessage();
    }
  });


  // ---------- クリア処理 ----------
  clearBtn.addEventListener("click", async function () {
    messages = [];
    saveMessages(messages);
    render(messages);

    try {
      await postJson("/clear", {});
    } catch (err) {
      console.error("Failed to clear session:", err);
    }
  });
});
