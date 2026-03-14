<template>
  <div class="project-page">
    <div class="project-head">
      <div class="head-lef">
        <div class="project-icon" :style="{ backgroundColor: project.color || '#e8eaef' }">
          {{ project.emoji || '💡' }}
        </div>
        <div class="project-info">
          <h1>{{ project.name }}</h1>
          <div class="project-meta">
            <span class="type-project">{{ project.type }}</span>
            <span class="updated-text">Updated 2 mins ago</span>
          </div>
        </div>
      </div>
      <button class="settings-btn" @click="showEditModal = true">
        <Settings :size="20" />
      </button>
    </div>

    <EditProjectModal
      v-model="showEditModal"
      :project="project"
      @updated="onProjectUpdated"
    />

    <div class="card-container">
      <StatCard label="Completion" :percent="percent" :completed="completed" :total="total" />
      <BaseCard msg="Due Today" :total="dueTodayCount" icon="📅" iconBg="#e3f2fd" />
      <BaseCard msg="Overdue"   :total="overdueCount"  icon="⏰" iconBg="#fce4ec" />
      <BaseCard msg="Total"     :total="total"          icon="🏁" iconBg="#f3e5f5" />
    </div>
    
    

    <Filterbar @view-change="v => currentView = v" />

    <KanbanBoard v-show="currentView === 'board'"
      :todo-tasks="todoTasks"
      :in-progress-tasks="inProgressTasks"
      :done-tasks="doneTasks"
      :members="members"
      @add="createTask"
      @move="handleMove"
      @edit="handleEdit"
    />
    <KanbanList v-show="currentView === 'list'"
      :todo-tasks="todoTasks"
      :in-progress-tasks="inProgressTasks"
      :done-tasks="doneTasks"
      :me="me"
      @move="handleMove"
    />

    <TaskModal
    v-if="selectedTask"
    :name="selectedTask.title"
    :date="selectedTask.due_date || ''"
    :time="selectedTask.due_time || ''"
    :status="selectedTask.status || 'Not started'"
    :description="selectedTask.description || ''"
    @update="handleUpdate"
    @close="selectedTask = null"
    />

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Settings } from 'lucide-vue-next'
import BaseCard from '../components/Basecard.vue'
import StatCard from '../components/StatCard.vue'
import Filterbar from '../components/project/Filterbar.vue'
import KanbanBoard from '../components/project/KanbanBoard.vue'
import KanbanList from '../components/project/KanbanList.vue'
import EditProjectModal from '../components/overview/modal/EditProjectModal.vue'
import TaskModal from '../components/TaskModal.vue'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const showEditModal = ref(false)
const project       = ref({})
const currentView   = ref('board')
const tasks         = ref([])
const me = ref(null)
const route     = useRoute()
const projectId = computed(() => route.params.id)

const members = computed(() => me.value ? [{
  user_id:    me.value.id,
  name:       me.value.name,
  email:      me.value.email,
  avatar_url: me.value.avatar_url || ''}] : [])

function getHeaders() {
  const token = localStorage.getItem('token')
  return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
}

const overdueCount = computed(() => {
  const today = new Date().toISOString().split('T')[0]
  return tasks.value.filter(t => !t.is_completed && t.due_date && t.due_date < today).length
})

const dueTodayCount = computed(() => {
  const today = new Date()
  const todayStr = `${today.getFullYear()}-${String(today.getMonth()+1).padStart(2,'0')}-${String(today.getDate()).padStart(2,'0')}`
  return tasks.value.filter(t => !t.is_completed && t.due_date === todayStr).length
})
const selectedTask = ref(null)
function handleEdit(task) { selectedTask.value = task }
async function handleUpdate(fields) {
    await fetch(`${API}/api/tasks/${selectedTask.value.id}`, {
        method: 'PATCH', headers: getHeaders(), body: JSON.stringify(fields)
    })
    fetchTasks()
    const updated = tasks.value.find(t => t.id === selectedTask.value.id)
    if (updated) selectedTask.value = updated
}

// ── Computed ──
const todoTasks       = computed(() => tasks.value.filter(t => t.status === 'Not started'))
const inProgressTasks = computed(() => tasks.value.filter(t => t.status === 'In progress'))
const doneTasks       = computed(() => tasks.value.filter(t => t.status === 'Completed'))

const completed = computed(() => doneTasks.value.length)
const total     = computed(() => tasks.value.length)
const percent   = computed(() => total.value ? Math.round(completed.value / total.value * 100) : 0)

// ── Fetch ──
async function fetchTasks() {
  try {
    const res  = await fetch(`${API}/api/projects/${projectId.value}/tasks`, { headers: getHeaders() })
    tasks.value = await res.json()
  } catch (err) {
    console.error('Failed to fetch tasks', err)
  }
}
async function fetchMe() {
  const res = await fetch(`${API}/api/me`, { headers: getHeaders() })
  me.value = await res.json()
}


async function fetchProject() {
  const res = await fetch(`${API}/api/projects/${projectId.value}`, { headers: getHeaders() })
  project.value = await res.json()
}

async function onProjectUpdated() {
  await fetchProject()
  window.dispatchEvent(new Event('projects-updated'))
}

async function createTask(taskData) {
  try {
    await fetch(`${API}/api/tasks`, {
      method:  'POST',
      headers: getHeaders(),
      body:    JSON.stringify({
        ...taskData,
        project_id:   Number(projectId.value),
        project_type: project.value.type || 'personal'
      })
    })
    fetchTasks()
    window.dispatchEvent(new Event('tasks-updated'))
  } catch (err) {
    alert('Failed to create task')
  }
}



async function handleMove({ taskId, newStatus }) {
  try {
    await fetch(`${API}/api/tasks/${taskId}`, {
      method:  'PATCH',
      headers: getHeaders(),
      body:    JSON.stringify({ status: newStatus })
    })
    fetchTasks()
  } catch (err) {
    console.error('Failed to move task', err)
  }
}

onMounted(() => {
  fetchTasks()
  fetchProject()
  fetchMe()
})

watch(projectId, () => {
  fetchTasks()
  fetchProject()
})


</script>



<style scoped>
.project-page {
  padding: 32px 24px;
  width: 100%;           
  box-sizing: border-box; 
}

.card-container {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.project-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  /* padding: 16px 20px;
  border: 1px solid #e2e8f0;
  border-radius: 12px; */
}

.head-lef {
  display: flex;
  align-items: center;
  gap: 16px;
}

.project-icon {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: #e8eaef;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 35px;
}

.project-info h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
}

.project-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 4px;
}

.type-project {
  background-color: #3b82f6;
  color: #fff;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.updated-text {
  color: #94a3b8;
  font-size: 13px;
}

.settings-btn {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #64748b;
  transition: all 0.2s;
}
.settings-btn:hover {
  background: #f1f5f9;
  color: #334155;
}
</style>