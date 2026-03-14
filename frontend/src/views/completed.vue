<template>
  <div class="inbox-page">

    <TaskStatus :tasks="tasks" />

    <TaskList
      title="Completed"
      subtitle="Tasks you've accomplished"
      :tasks="completedTasks"
      @toggle="handleToggle"
      @select="handleSelect"
      @delete="deleteTask"
    />

    <TaskModal
      v-if="selectedTask"
      :name="selectedTask.name"
      :date="selectedTask.due_date || ''"
      :status="selectedTask.status || 'Not started'"
      :description="selectedTask.description || ''"
      :time="selectedTask.due_time || ''"
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

const filteredTasks = computed(() => {
  let data = tasks.value
  if (props.search) {
    const q = props.search.toLowerCase()
    data = data.filter(t => (t.name || '').toLowerCase().includes(q))
  }
  return data
})

const completedTasks = computed(() => filteredTasks.value.filter(t => t.done))

async function handleToggle(task) {
  await fetch(`${API}/api/tasks/${task.id}/complete`, { method: 'PATCH', headers: getHeaders() })
  await loadTasks()
  window.dispatchEvent(new Event("tasks-updated"))
}

function handleSelect(task) {
  selectedTask.value = task
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

onMounted(loadTasks)
</script>

<style scoped>
.inbox-page {
  padding: 32px 24px;
}
</style>