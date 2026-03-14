<template>
  <div class="project-page">

    <!-- HEAD -->
    <div class="project-head">
      <div class="head-lef">
        <div class="project-icon" :style="{ backgroundColor: project?.color || '#7c3aed' }">
          {{ project?.emoji || '🗂️' }}
        </div>
        <div class="project-info">
          <h1>{{ project?.name || 'Corporate Project' }}</h1>
          <div class="project-meta">
            <span class="type-project">Corporate</span>
          </div>
        </div>
      </div>

      <div class="head-right">
        <div class="team-section">
          <span class="team-label">Team:</span>
          <div class="avatars">
            <div
              class="avatar"
              v-for="member in displayMembers"
              :key="member.user_id"
              :title="member.name || member.email"
            >
              <img
                v-if="member.avatar_url"
                :src="`http://localhost:8000${member.avatar_url}`"
                class="avatar-img"
              />
              <span v-else>{{ getInitials(member.name || member.email) }}</span>
            </div>
            <div v-if="members.length > 4" class="avatar avatar-more">
              +{{ members.length - 4 }}
            </div>
          </div>
          <button class="add-member" @click="showAddModal = true"><Plus :size="16" /></button>
        </div>
        <button class="settings-btn" @click="showEditModal = true"><Settings :size="20" /></button>
      </div>
    </div>

    <EditProjectModal
      v-model="showEditModal"n
      :project="project"
      @updated="onProjectUpdated"
    />

    <!-- CARDS -->
    <div class="card-container">
      <StatCard label="Completion" :percent="percent" :completed="completed" :total="total" />
      <BaseCard msg="Due Today" :total="dueTodayCount" icon="🔵" iconBg="#e3f2fd" />
      <BaseCard msg="Overdue" :total="overdueCount" icon="⚠️" iconBg="#fff3e0" />
      <BaseCard msg="Members" :total="members.length" icon="👥" iconBg="#fce4ec" />
    </div>

    <Filterbar @view-change="v => currentView = v" />

    <KanbanBoard
        v-show="currentView === 'board'"
        :todo-tasks="todoTasks"
        :in-progress-tasks="inProgressTasks"
        :done-tasks="doneTasks"
        :members="members"
        @add="createTask"
        @move="handleMove"
        @edit="handleEdit"
    />

    <TaskModal
      v-if="selectedTask"
      :name="selectedTask.title"
      :date="selectedTask.due_date || ''"
      :time="selectedTask.due_time || ''"
      :status="selectedTask.status || 'Not started'"
      :description="selectedTask.description || ''"
      :assignee-id="selectedTask.assignee_id || null"
      :project-id-for-members="projectId"
      @update="handleUpdate"
      @delete="handleDelete"
      @close="selectedTask = null"
      :assignee-ids="selectedTask.assignee_ids || []"
    />

    <CorporateList v-show="currentView === 'list'"
      :todo-tasks="todoTasks"
      :in-progress-tasks="inProgressTasks"
      :done-tasks="doneTasks"
      :members="members"
    />

    <AddMemberModal
      v-model="showAddModal"
      :project-id="projectId"
      :members="members"
      @members-changed="fetchMembers"
    />

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Plus, Settings } from 'lucide-vue-next'
import BaseCard from '../components/Basecard.vue'
import StatCard from '../components/StatCard.vue'
import Filterbar from '../components/project/Filterbar.vue'
import KanbanBoard from '../components/project/KanbanBoard.vue'
import CorporateList from '../components/project/Corporatelist.vue'
import AddMemberModal from '../components/overview/modal/AddMemberModal.vue'
import EditProjectModal from '../components/overview/modal/EditProjectModal.vue'
import TaskModal from '../components/TaskModal.vue'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const route     = useRoute()
const projectId = computed(() => route.params.id)

const project       = ref(null)
const members       = ref([])
const currentView   = ref('board')
const tasks         = ref([])
const showAddModal  = ref(false)
const showEditModal = ref(false)
const selectedTask  = ref(null)

function getHeaders() {
  const token = localStorage.getItem('token')
  return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
}

// ── Computed ──
const todoTasks       = computed(() => tasks.value.filter(t => t.status === 'Not started'))
const inProgressTasks = computed(() => tasks.value.filter(t => t.status === 'In progress'))
const doneTasks       = computed(() => tasks.value.filter(t => t.status === 'Completed' || t.is_completed))

const completed    = computed(() => doneTasks.value.length)
const total        = computed(() => tasks.value.length)
const percent      = computed(() => total.value ? Math.round(completed.value / total.value * 100) : 0)


const displayMembers = computed(() => members.value.slice(0, 4))

function getInitials(name) {
  if (!name) return '?'
  return name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase()
}

const overdueCount = computed(() => {
  const today = new Date().toISOString().split('T')[0]
  return tasks.value.filter(t => !t.is_completed && t.due_date && t.due_date.slice(0, 10) < today).length
})

const dueTodayCount = computed(() => {
  const today = new Date()
  const todayStr = `${today.getFullYear()}-${String(today.getMonth()+1).padStart(2,'0')}-${String(today.getDate()).padStart(2,'0')}`
  return tasks.value.filter(t => !t.is_completed && t.due_date?.slice(0, 10) === todayStr).length
})

// ── Fetch ──
async function fetchProject() {
  try {
    const res = await fetch(`${API}/api/projects/${projectId.value}`, { headers: getHeaders() })
    project.value = await res.json()
  } catch (err) {
    console.error('Failed to fetch project', err)
  }
}

async function fetchMembers() {
  try {
    const res = await fetch(`${API}/api/projects/${projectId.value}/members`, { headers: getHeaders() })
    const data = await res.json()
    
    // เพิ่ม owner เข้าไปด้วย
    const meRes  = await fetch(`${API}/api/me`, { headers: getHeaders() })
    const me     = await meRes.json()
    const isOwner = project.value?.user_id === me.id
    
    if (isOwner) {
      const alreadyIn = data.some(m => m.user_id === me.id)
      if (!alreadyIn) {
        data.unshift({
          user_id:    me.id,
          name:       me.name,
          email:      me.email,
          avatar_url: me.avatar_url || '',
          role:       'Owner'
        })
      }
    }
    
    members.value = data
  } catch (err) {
    console.error('Failed to fetch members', err)
  }
}

async function fetchTasks() {
  try {
    const res = await fetch(`${API}/api/projects/${projectId.value}/tasks`, { headers: getHeaders() })
    tasks.value = await res.json()
  } catch (err) {
    console.error('Failed to fetch tasks', err)
  }
}

async function createTask(taskData) {
  try {
    await fetch(`${API}/api/tasks`, {
      method:  'POST',
      headers: getHeaders(),
      body:    JSON.stringify({
        ...taskData,
        project_id:   Number(projectId.value),
        project_type: 'corporate'
      })
    })
    fetchTasks()
  } catch (err) {
    alert('Failed to create task')
  }
}

async function handleDelete() {
  await fetch(`${API}/api/tasks/${selectedTask.value.id}`, {
    method: 'DELETE', headers: getHeaders()
  })
  await fetchTasks()
  selectedTask.value = null
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

function handleEdit(task) {
  selectedTask.value = task
}

async function handleUpdate(fields) {
  try {
    await fetch(`${API}/api/tasks/${selectedTask.value.id}`, {
      method:  'PATCH',
      headers: getHeaders(),
      body:    JSON.stringify(fields)
    })
    await fetchTasks()
    selectedTask.value = null
  } catch (err) {
    console.error('Failed to update task', err)
  }
}

async function onProjectUpdated() {
  await fetchProject()
  window.dispatchEvent(new Event('projects-updated'))
}

onMounted(async () => {
  await fetchProject()
  await fetchMembers()
  fetchTasks()
})

watch(projectId, async () => {
  await fetchProject()
  fetchMembers()
  fetchTasks()
})
</script>

<style scoped>
/* ── Layout ── */
.project-page {
  padding: 32px 24px;
  width: 100%;
  box-sizing: border-box;
}

@media (max-width: 768px) {
  .project-page {
    padding: 20px 16px;
  }
}

/* ── Header Area ── */
.project-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.head-lef {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1 1 auto;
}

.project-icon {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 40px;
  flex-shrink: 0;
}

.project-info h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 700;
  line-height: 1.2;
}

.project-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 6px;
}

.type-project {
  background-color: #ede9fe;
  color: #7c3aed;
  padding: 2px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
  white-space: nowrap;
}

/* ── Header Right (Team & Tools) ── */
.head-right {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.team-section {
  display: flex;
  align-items: center;
  gap: 8px;
}

.team-label {
  font-size: 13px;
  color: #64748b;
  font-weight: 500;
}

/* ── Avatars ── */
.avatars { 
    display: flex; 
    align-items: center; 
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #e2e8f0;
  border: 2px solid #fff;
  margin-left: -8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #64748b;
  font-size: 11px;
  font-weight: 600;
  overflow: hidden;
}

.avatar:first-child { margin-left: 0; }
.avatar-more { background: #f1f5f9; color: #64748b; }

.avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
}

.add-member {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 2px dashed #cbd5e1;
  background: none;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
  cursor: pointer;
  margin-left: 4px;
}

/* ── Icons/Buttons ── */
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
  flex-shrink: 0;
}

.settings-btn:hover {
  background: #f1f5f9;
  color: #334155;
}

/* ── Summary Cards Container ── */
.card-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}
</style>