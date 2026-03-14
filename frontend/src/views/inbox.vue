<template>
  <div class="inbox-page">

    <TaskStatus :tasks="tasks" />

    <AddTask msg="Add New Task" @add="handleAdd" />

    <TaskList
      :title="'Inbox'"
      :subtitle="'All your pending tasks'"
      :tasks="pendingTasks"
      @toggle="handleToggle"
      @delete="deleteTask"
      @edit="handleEdit"
    />

    <TaskModal
      v-if="selectedTask"
      :name="selectedTask.name"
      :date="selectedTask.due_date || ''"
      :time="selectedTask.due_time || ''"
      :status="selectedTask.status || 'Not started'"
      :description="selectedTask.description || ''"
      :project-type="selectedTask.project_type || ''"
      :project-id="selectedTask.project_id || null"
      @update="handleUpdate"
      @close="selectedTask = null"
    />

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import TaskStatus from '@/components/TaskStatus.vue'
import AddTask    from '../components/AddTask.vue'
import TaskList   from '../components/TaskList.vue'
import TaskModal  from '../components/TaskModal.vue'

const API          = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const tasks        = ref([])
const selectedTask = ref(null)
const props        = defineProps({ search: String })

function getHeaders() {
  const token = localStorage.getItem('token')
  return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
}

async function loadTasks() {
  const res  = await fetch(`${API}/api/tasks`, { headers: getHeaders() })
  const data = await res.json()
  tasks.value = data.map(t => ({
    id:           t.id,
    name:         t.title,
    tag:          t.tag || '',
    done:         t.is_completed,
    due_date:     t.due_date,
    status:       t.status,
    due_time:     t.due_time,
    description:  t.description,
    project_type: t.project_type,
    project_id:   t.project_id
  }))
}

const pendingTasks = computed(() => {
  let data = tasks.value.filter(t => !t.done)
  if (props.search) {
    const q = props.search.toLowerCase()
    data = data.filter(t => t.name.toLowerCase().includes(q))
  }
  return data
})

async function handleAdd(data) {
  await fetch(`${API}/api/tasks`, {
    method:  'POST',
    headers: getHeaders(),
    body:    JSON.stringify({
      title:        data.title,
      due_date:     data.due_date     || null,
      due_time:     data.due_time     || null,
      project_type: data.project_type || null,
      project_id:   data.project_id   || null,
    })
  })
  await loadTasks()
  window.dispatchEvent(new Event("tasks-updated"))
}

async function handleToggle(task) {
  await fetch(`${API}/api/tasks/${task.id}/complete`, { method: 'PATCH', headers: getHeaders() })
  await loadTasks()
  window.dispatchEvent(new Event("tasks-updated"))
}

async function handleUpdate(fields) {
  await fetch(`${API}/api/tasks/${selectedTask.value.id}`, {
    method:  'PATCH',
    headers: getHeaders(),
    body:    JSON.stringify(fields)
  })
  await loadTasks()
  window.dispatchEvent(new Event("tasks-updated"))
  const updated = tasks.value.find(t => t.id === selectedTask.value.id)
  if (updated) selectedTask.value = updated
}

async function deleteTask(task) {
  tasks.value = tasks.value.filter(t => t.id !== task.id)
  await fetch(`${API}/api/tasks/${task.id}`, { method: 'DELETE', headers: getHeaders() })
  window.dispatchEvent(new Event("tasks-updated"))
}

function handleEdit(task) {
  selectedTask.value = task
}

onMounted(loadTasks)
</script>

<style scoped>
/* ── Layout ── */
.inbox-page {
  padding: 32px 24px;
  width: 100%;
  box-sizing: border-box;
}

@media (max-width: 768px) {
  .inbox-page {
    padding: 20px 16px; /* Reduce padding on smaller screens */
  }
}

/* ── Components Container ── */
.card-container {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap; /* Ensure cards wrap smoothly */
}
</style>