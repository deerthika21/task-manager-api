const API_URL = "https://task-manager-api-jne7.onrender.com"


// REGISTER
async function register() {

    const username =
        document.getElementById("register-username").value

    const email =
        document.getElementById("register-email").value

    const password =
        document.getElementById("register-password").value


    const response = await fetch(
        `${API_URL}/register`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                username,
                email,
                password
            })
        }
    )

    const data = await response.json()

    alert(data.message)
}


// LOGIN
async function login() {

    const email =
        document.getElementById("login-email").value

    const password =
        document.getElementById("login-password").value


    const response = await fetch(
        `${API_URL}/login`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                email,
                password
            })
        }
    )

    const data = await response.json()

    localStorage.setItem(
        "token",
        data.access_token
    )

    alert("Login successful")

    getTasks()
}


// CREATE TASK
async function createTask() {

    const title =
        document.getElementById("task-title").value

    const token =
        localStorage.getItem("token")


    try {
        const res = await fetch(
            `${API_URL}/tasks`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json",

                    "Authorization": `Bearer ${token}`
                },

                body: JSON.stringify({
                    title
                })
            }
        )

        const data = await res.json().catch(() => ({}))

        if (!res.ok) {
            console.error('Create task failed', data)
            alert(data.detail || data.message || 'Failed to create task')
            return
        }

        // clear input and refresh tasks
        document.getElementById("task-title").value = ""
        getTasks()
    } catch (err) {
        console.error(err)
        alert('Network error creating task')
    }
}


// GET TASKS
async function getTasks() {

    const token =
        localStorage.getItem("token")


    try {
        const response = await fetch(
            `${API_URL}/tasks`,
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        )

        const payload = await response.json().catch(() => null)

        const tasksDiv = document.getElementById("tasks")
        tasksDiv.innerHTML = ""

        if (!response.ok) {
            console.error('Get tasks failed', payload)
            tasksDiv.innerHTML = `<p style="color:#666">${payload?.detail || payload?.message || 'Failed to load tasks'}</p>`
            return
        }

        if (!Array.isArray(payload)) {
            console.error('Unexpected tasks payload', payload)
            tasksDiv.innerHTML = `<p style="color:#666">No tasks to show</p>`
            return
        }

        payload.forEach(task => {
            const completed = task.completed ? "✅" : ""

            tasksDiv.innerHTML += `
                <div class="task">

                    <p>
                        ${task.title} ${completed}
                    </p>

                    <button onclick="completeTask(${task.id})">
                        Complete
                    </button>

                    <button onclick="deleteTask(${task.id})">
                        Delete
                    </button>

                </div>
            `
        })
    } catch (err) {
        console.error(err)
        const tasksDiv = document.getElementById("tasks")
        tasksDiv.innerHTML = `<p style="color:#666">Network error loading tasks</p>`
    }
}


// COMPLETE TASK
async function completeTask(id) {

    const token =
        localStorage.getItem("token")


    await fetch(
        `${API_URL}/tasks/${id}`,
        {
            method: "PUT",

            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    )

    getTasks()
}


// DELETE TASK
async function deleteTask(id) {

    const token =
        localStorage.getItem("token")


    await fetch(
        `${API_URL}/tasks/${id}`,
        {
            method: "DELETE",

            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    )

    getTasks()
}