let add_form = document.querySelector("form");
let ul = document.getElementById("todos");
let toast = document.getElementById("toast");
let todos;

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
    await updateTodoInBackend(id, input.checked);
    todos[id]["checked"] = input.checked;
  });

  button.addEventListener("click", async (e) => {
    li.remove();
    delete todos[id];
    await deleteTodoFromBackend(id);
  });
}

async function updateTodoInBackend(id, done) {
  let resp = await fetch(`/api/todos/${id}`, {
    method: "PUT",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ done: done }),
  });
  console.log("resp: ", resp);
}

async function getTodosFromBackend() {
  let resp = await fetch(`/api/todos/`, {
    method: "GET",
  }).then((resp) => resp.json());
  console.log("resp: ", resp);
  if (resp.status == true) {
    return resp.data;
  } else {
    return null;
  }
}

async function deleteTodoFromBackend(id) {
  let resp = await fetch(`/api/todos/${id}`, {
    method: "DELETE",
  });
  console.log("resp: ", resp);
}

async function addTodoInBackend(text, done) {
  let resp = await fetch("/api/todos/", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ text: text, done: done }),
  }).then((resp) => resp.json());
  console.log("resp: ", resp);
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
