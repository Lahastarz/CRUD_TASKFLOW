const API_BASE = "http://localhost:8000";

// Kept as a plain JS variable, never localStorage — lost on refresh by design.
// See the auth footnote in index.html for why.
let accessToken = null;
let currentEmail = null;

const $ = (id) => document.getElementById(id);

function showToast(message, isError = false) {
  const toast = $("toast");
  toast.textContent = message;
  toast.classList.toggle("error", isError);
  toast.classList.remove("hidden");
  setTimeout(() => toast.classList.add("hidden"), 3000);
}

async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (accessToken) headers["Authorization"] = `Bearer ${accessToken}`;

  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (response.status === 204) return null;

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    const message = data.detail || (Array.isArray(data.detail) ? data.detail[0]?.msg : "Something went wrong");
    throw new Error(typeof message === "string" ? message : "Request failed");
  }
  return data;
}

// ---------- Auth ----------

function switchTab(tab) {
  document.querySelectorAll(".tab").forEach((t) => t.classList.toggle("active", t.dataset.tab === tab));
  $("loginForm").classList.toggle("hidden", tab !== "login");
  $("registerForm").classList.toggle("hidden", tab !== "register");
}

document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => switchTab(tab.dataset.tab));
});

$("registerForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const note = $("registerNote");
  note.textContent = "";
  note.className = "form-note";

  try {
    await api("/auth/register", {
      method: "POST",
      body: JSON.stringify({
        email: $("registerEmail").value,
        password: $("registerPassword").value,
      }),
    });
    note.textContent = "Account created — you can log in now.";
    note.classList.add("success");
    switchTab("login");
    $("loginEmail").value = $("registerEmail").value;
  } catch (err) {
    note.textContent = err.message;
    note.classList.add("error");
  }
});

$("loginForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const note = $("loginNote");
  note.textContent = "";
  note.className = "form-note";

  try {
    const data = await api("/auth/login", {
      method: "POST",
      body: JSON.stringify({
        email: $("loginEmail").value,
        password: $("loginPassword").value,
      }),
    });
    accessToken = data.access_token;
    currentEmail = $("loginEmail").value;
    enterBoard();
  } catch (err) {
    note.textContent = err.message;
    note.classList.add("error");
  }
});

$("logoutBtn").addEventListener("click", () => {
  accessToken = null;
  currentEmail = null;
  $("authView").classList.remove("hidden");
  $("boardView").classList.add("hidden");
  $("userBadge").classList.add("hidden");
  $("loginForm").reset();
  $("loginNote").textContent = "";
});

function enterBoard() {
  $("authView").classList.add("hidden");
  $("boardView").classList.remove("hidden");
  $("userBadge").classList.remove("hidden");
  $("userEmail").textContent = currentEmail;
  loadTasks();
}

// ---------- Tasks ----------

function formatDate(iso) {
  const d = new Date(iso);
  return d.toLocaleDateString(undefined, { month: "short", day: "numeric" });
}

function taskCard(task) {
  const card = document.createElement("div");
  card.className = "task-card";

  const nextActions = {
    todo: [["Start", "in_progress"]],
    in_progress: [["Mark done", "done"], ["Back to to-do", "todo"]],
    done: [["Reopen", "todo"]],
  }[task.status];

  card.innerHTML = `
    <p class="task-title"></p>
    ${task.description ? '<p class="task-desc"></p>' : ""}
    <p class="task-meta">Updated ${formatDate(task.updated_at)}</p>
    <div class="task-actions"></div>
  `;
  card.querySelector(".task-title").textContent = task.title;
  if (task.description) card.querySelector(".task-desc").textContent = task.description;

  const actions = card.querySelector(".task-actions");
  nextActions.forEach(([label, newStatus]) => {
    const btn = document.createElement("button");
    btn.textContent = label;
    btn.addEventListener("click", () => updateStatus(task.id, newStatus));
    actions.appendChild(btn);
  });

  const delBtn = document.createElement("button");
  delBtn.textContent = "Delete";
  delBtn.className = "delete";
  delBtn.addEventListener("click", () => deleteTask(task.id));
  actions.appendChild(delBtn);

  return card;
}

async function loadTasks() {
  try {
    const tasks = await api("/tasks/");
    render(tasks);
  } catch (err) {
    showToast(err.message, true);
  }
}

function render(tasks) {
  const columns = { todo: $("col-todo"), in_progress: $("col-in_progress"), done: $("col-done") };
  Object.values(columns).forEach((col) => (col.innerHTML = ""));

  const counts = { todo: 0, in_progress: 0, done: 0 };
  tasks.forEach((task) => {
    counts[task.status]++;
    columns[task.status].appendChild(taskCard(task));
  });

  Object.entries(counts).forEach(([status, count]) => {
    $(`count-${status}`).textContent = count;
  });

  Object.entries(columns).forEach(([status, col]) => {
    if (counts[status] === 0) {
      const empty = document.createElement("div");
      empty.className = "empty-column";
      empty.textContent = "Nothing here";
      col.appendChild(empty);
    }
  });
}

$("newTaskForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const title = $("newTaskTitle").value.trim();
  const description = $("newTaskDesc").value.trim();
  if (!title) return;

  try {
    await api("/tasks/", {
      method: "POST",
      body: JSON.stringify({ title, description: description || null }),
    });
    $("newTaskForm").reset();
    loadTasks();
  } catch (err) {
    showToast(err.message, true);
  }
});

async function updateStatus(taskId, status) {
  try {
    await api(`/tasks/${taskId}`, {
      method: "PATCH",
      body: JSON.stringify({ status }),
    });
    loadTasks();
  } catch (err) {
    showToast(err.message, true);
  }
}

async function deleteTask(taskId) {
  try {
    await api(`/tasks/${taskId}`, { method: "DELETE" });
    loadTasks();
  } catch (err) {
    showToast(err.message, true);
  }
}
