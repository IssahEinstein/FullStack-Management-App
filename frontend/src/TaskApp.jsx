import { useState, useEffect } from "react";
import { api } from "./api.js";

function TaskApp () {
    const [ tasks, setTasks ] = useState([]);
    const [ singleTask, setsingleTask ] = useState();
    const [ delTask, setdelTask ] = useState();
    const [ form, setForm ] = useState({
        title: "",
        description: ""
    });

    async function fetchAllTasks () {
        const response = await api.get("/tasks");
        setTasks(response.data);
    }

    async function fetchSingleTask (taskId) {
        const response = await api.get(`/tasks/${taskId}`);
        setsingleTask(response.data);
    }

    async function deletesingleTask(taskId) {
        const respnonse = await api.delete(`/tasks/${id}/delete`)
        setdelTask(respnonse.data);
    }


    async function completeTask(id) {
        const response = await api.put(`/tasks/${id}/complete`);
        const updated = response.data;

        setTasks(prev =>
            prev.map( t => t.id === updated.id ? updated : t )
        );
    }

    async function createTask(e) {
        e.preventDefault();

        const payload = {
            title: form.title,
            description: form.description
        }

        const response = await api.post("/tasks", payload);
        const newTask = response.data;

        setTasks(prev => [ ...prev, newTask]);
        
        setForm({id: "", title: "", description: ""});
    }

    useEffect( () => 
        { fetchAllTasks();
         }, []);

    return (

        <div>
      <h1>Tasks</h1>

      <form onSubmit={createTask} style={{ marginBottom: "1rem" }}>
        <input
          type="text"
          placeholder="Title"
          value={form.title}
          onChange={e => setForm({ ...form, title: e.target.value })}
        />
        <input
          type="text"
          placeholder="Description"
          value={form.description}
          onChange={e => setForm({ ...form, description: e.target.value })}
        />
        <button type="submit">Add Task</button>
      </form>

      {tasks.length === 0 && <p>No tasks yet.</p>}
      {tasks.map(task => (
        <div key={task.id}>
          <span>
            {task.title} {task.description} {task.completed ? "(done)" : ""}
          </span>
          {!task.completed && (
            <button onClick={() => completeTask(task.id)}>
              Complete
            </button>
          )}
        </div>
      ))}
    </div>
  );


};

export default TaskApp;