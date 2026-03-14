<template>
  <div class="inbox-page">

    <TaskStatus :tasks="tasks" />

    <AddTask msg="Add New Task" @add="handleAdd" />
        

    <TaskList
      title="Upcoming"
      subtitle="Tasks scheduled for the next 7 days"
      :tasks="upcoming"
      @toggle="handleToggle"
      @delete="deleteTask"
      @edit="handleEdit"
    />

    <TaskModal
      v-if="selectedTask"
      :name="selectedTask.name"
      :date="selectedTask.due_date || ''"
      :status="selectedTask.status || 'Not started'"
      :time="selectedTask.due_time || ''"
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
import AddTask   from '../components/AddTask.vue'
import TaskList  from '@/components/TaskList.vue'
import TaskModal from '../components/TaskModal.vue'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const tasks        = ref([])
const selectedTask = ref(null)
const props        = defineProps({ search: String })
const now          = new Date()
const today        = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`

function getHeaders() {
    const token = localStorage.getItem('token')
    return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
}

async function loadTasks() {
    const res = await fetch(`${API}/api/tasks`, { headers: getHeaders() })
    const data = await res.json()
    tasks.value = data.map(t => ({
        id: t.id, name: t.title, tag: t.tag || '', done: t.is_completed,
        due_date: t.due_date ? t.due_date.slice(0, 10) : null, status: t.status,
        due_time: t.due_time, description: t.description, project_type: t.project_type, project_id: t.project_id
    }))
}

const upcoming = computed(() => {
    const todayDate    = new Date()
    const nextWeekDate = new Date()
    nextWeekDate.setDate(todayDate.getDate() + 7)
    let data = tasks.value.filter(t => {
        if (!t.due_date || t.done) return false
        const d = new Date(t.due_date)
        return d >= todayDate && d <= nextWeekDate
    })
    if (props.search) {
        const q = props.search.toLowerCase()
        data = data.filter(t => t.name.toLowerCase().includes(q))
    }
    return data
})

async function handleAdd(data) {
    await fetch(`${API}/api/tasks`, { method: 'POST', headers: getHeaders(), body: JSON.stringify({ title: data.title, due_date: data.due_date || null, due_time: data.due_time || null }) })
    await loadTasks()
    window.dispatchEvent(new Event("tasks-updated"))
}

async function handleToggle(task) {
    await fetch(`${API}/api/tasks/${task.id}/complete`, { method: 'PATCH', headers: getHeaders() })
    await loadTasks()
    window.dispatchEvent(new Event("tasks-updated"))
}

async function handleUpdate(fields) {
    await fetch(`${API}/api/tasks/${selectedTask.value.id}`, { method: 'PATCH', headers: getHeaders(), body: JSON.stringify(fields) })
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

function handleEdit(task) { selectedTask.value = task }

onMounted(loadTasks)
</script>

<style scoped>
.inbox-page {
  padding: 32px 24px;
}

.card-container {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}
</style>