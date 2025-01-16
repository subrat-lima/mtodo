let add_form = document.querySelector("form");
let ul = document.querySelector("ul");
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

function loadTodos(e) {
    todos = localStorage.getItem("todos");
    if(!todos) {
        todos = {};
        return;
    }
    todos = JSON.parse(todos);
    for(let [id, v] of Object.entries(todos)) {
        addTodoToUI(id, v.text, v.checked);
    }
}

function updateTodos() {
    localStorage.setItem("todos", JSON.stringify(todos));
}

function addTodoToUI(id, text, checked=false) {
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

    input.addEventListener("click", (e) => {
        todos[id]["checked"] = input.checked;
        updateTodos();
    });

    button.addEventListener("click", (e) => {
        li.remove();
        delete todos[id];
        updateTodos();
    });
}

function todoItemExists(text) {
    for(let [k, v] of Object.entries(todos)) {
        if(v.text.toLowerCase() == text.toLowerCase()) {
            return true;
        }
    }
    return false;
}

function addTodoItem(e) {
    e.preventDefault();
    let text = e.target.todo.value;
    let id = generateId(); 

    e.target.todo.value = "";
    if(text.trim().length == 0) {
        showToast("text empty, please enter text...");
        return;
    }

    if(todoItemExists(text)) {
        showToast("item already exists!!!");
        return;
    }

    addTodoToUI(id, text);
    todos[id] = {
        "text": text,
        "checked": false
    };
    updateTodos();
}

document.addEventListener("DOMContentLoaded", loadTodos);
add_form.addEventListener("submit", addTodoItem);
