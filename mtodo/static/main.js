let add_form = document.querySelector("form");
let ul = document.getElementById("todos");
let toast = document.getElementById("toast");
let todos;

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

function showToast(text) {
  let text_node = document.createTextNode(text);
  toast.innerHTML = "";
  toast.appendChild(text_node);
  setTimeout(() => {
    text_node.remove();
  }, 2000);
}

async function loadTodos(e) {
  todos = await getTodosFromBackend();
  if (!todos) {
    return;
  }
  for (let todo of todos) {
    addTodoToUI(todo.id, todo.text, todo.done);
  }
}

async function addTodoToUI(id, text, checked = false) {
  let li = document.createElement("li");
  let label = document.createElement("label");
  let input = document.createElement("input");
  let span = document.createElement("span");
  let button = document.createElement("button");

  li.setAttribute("data-id", id);
  input.setAttribute("data-id", id);
  input.setAttribute("type", "checkbox");
  input.checked = checked;
  span.appendChild(document.createTextNode(text));
  button.appendChild(document.createTextNode("×"));
  label.appendChild(input);
  label.appendChild(span);
  li.appendChild(label);
  li.appendChild(button);
  ul.appendChild(li);

  input.addEventListener("click", async (e) => {
    todos[id]["checked"] = input.checked;
    let resp = await updateTodoInBackend(id, input.checked);
    if (resp.status == False) {
      showToast(`update failed: ${resp.text}`);
    }
  });

  button.addEventListener("click", async (e) => {
    li.remove();
    delete todos[id];
    let resp = await deleteTodoFromBackend(id);
    if (resp.status == False) {
      showToast(`delete failed: ${resp.text}`);
    }
  });
}

async function updateTodoInBackend(id, done) {
  let resp = await fetch(`/api/todos/${id}`, {
    method: "PUT",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ done: done }),
  }).then((resp) => resp.json());
  return resp;
}

async function getTodosFromBackend() {
  let resp;
  try {
    resp = await fetch(`/api/todos/`, {
      method: "GET",
    }).then((resp) => resp.json());
    if (resp.status == true) {
      return resp.data;
    } else {
      return null;
    }
  } catch (e) {
    return null;
  }
}

async function deleteTodoFromBackend(id) {
  let resp = await fetch(`/api/todos/${id}`, {
    method: "DELETE",
  }).then((resp) => resp.json());
  return resp;
}

async function addTodoInBackend(text, done) {
  let resp = await fetch("/api/todos/", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ text: text, done: done }),
  }).then((resp) => resp.json());
  return resp.id;
}

function todoItemExists(text) {
  for (let [k, v] of Object.entries(todos)) {
    if (v.text.toLowerCase() == text.toLowerCase()) {
      return true;
    }
  }
  return false;
}

async function addTodoItem(e) {
  e.preventDefault();
  let text = e.target.todo.value;
  let id = await addTodoInBackend(text, false);

  e.target.todo.value = "";
  if (text.trim().length == 0) {
    showToast("text empty, please enter text...");
    return;
  }

  if (todoItemExists(text)) {
    showToast("item already exists!!!");
    return;
  }

  addTodoToUI(id, text, false);
  todos[id] = {
    text: text,
    checked: false,
  };
}

document.addEventListener("DOMContentLoaded", loadTodos);
add_form.addEventListener("submit", addTodoItem);

var socket = io();
socket.on("connect", function () {
  socket.emit("join", { data: "todo" });
});

socket.on("add-todo", async (data) => {
  await sleep(100);
  todo = JSON.parse(data);
  if (todos[todo.id]) {
    return;
  } else {
    addTodoToUI(todo.id, todo.text, todo.done);
    todos[todo.id] = {
      text: todo.text,
      checked: todo.done,
    };
  }
});

socket.on("update-todo", (data) => {
  todo = JSON.parse(data);
  document.querySelector(`input[data-id="${todo.id}"]`).checked = todo.done;
  todos[todo.id]["checked"] = todo.done;
});

socket.on("delete-todo", (data) => {
  todo = JSON.parse(data);
  if (todos[todo.id]) {
    document.querySelector(`li[data-id="${todo.id}"]`).remove();
    delete todos[todo.id];
  }
});
