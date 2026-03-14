<template>
  <div class="task-page" @click.self="emit('close')">
    <div class="modal">

      <div class="modal-header">
        <h1>{{ name }}</h1>
        <button class="delete-btn" @click="emit('delete')">
          <Trash2 :size="16" />
        </button>
      </div>

      <div class="selected-prob">
        <div class="field">
          <label>Due Date</label>
          <input type="date" class="date-input" :value="date"
            @change="emitUpdate({ due_date: $event.target.value || null })" />
        </div>
        <div class="field">
          <label>Time</label>
          <input type="time" class="date-input" :value="localTime"
            @change="localTime = $event.target.value; emitUpdate({ due_time: $event.target.value || null })" />
        </div>
        <div class="field">
          <label>Status</label>
          <select class="status-select" v-model="localStatus" :class="{
            'status-not-started': localStatus === 'Not started',
            'status-in-progress': localStatus === 'In progress',
            'status-completed':   localStatus === 'Completed'
          }" @change="emitUpdate({ status: localStatus })">
            <option>Not started</option>
            <option>In progress</option>
            <option>Completed</option>
          </select>
        </div>

        <div class="field">
          <label>Assignees</label>
          <div class="assignee-select-wrap">
            <div
              v-for="m in members"
              :key="m.user_id"
              class="assignee-option"
              :class="{ active: localAssigneeIds.includes(m.user_id) }"
              @click="toggleAssignee(m.user_id)"
            >
              <div class="avatar-sm" :style="{ background: getColor(m.name) }">
                <img v-if="m.avatar_url" :src="`${API}${m.avatar_url}`" class="avatar-img" />
                <span v-else>{{ getInitials(m.name || m.email) }}</span>
              </div>
              <span>{{ m.name || m.email }}</span>
              <Check v-if="localAssigneeIds.includes(m.user_id)" :size="12" class="check-icon" />
            </div>
            <div v-if="members.length === 0" class="no-members-msg">No members in this project</div>
          </div>
        </div>

        <div class="field">
          <label>Project Type</label>
          <select class="type-select" v-model="localProjectType"
            @change="localProjectId = null; emitUpdate({ project_type: localProjectType, project_id: null })">
            <option value="">— None —</option>
            <option>Personal</option>
            <option>Corporate</option>
          </select>
        </div>

        <div class="field">
          <label>Project</label>
          <select class="type-select" v-model="localProjectId" :disabled="!localProjectType"
            @change="emitUpdate({ project_id: localProjectId ? Number(localProjectId) : null })">
            <option :value="null">— None —</option>
            <option v-for="proj in filteredProjects" :key="proj.id" :value="proj.id">
              {{ proj.emoji }} {{ proj.name }}
            </option>
          </select>
        </div>
      </div>

      <textarea v-model="localDesc" class="description" placeholder="This task is about"
        @change="emitUpdate({ description: localDesc })">
      </textarea>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Check, Trash2 } from 'lucide-vue-next'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const props = defineProps({
  name:                { type: String,  default: '' },
  date:                { type: String,  default: '' },
  time:                { type: String,  default: '' },
  status:              { type: String,  default: 'Not started' },
  projectType:         { type: String,  default: '' },
  projectId:           { type: Number,  default: null },
  description:         { type: String,  default: '' },
  assigneeIds:         { type: Array,   default: () => [] },
  projectIdForMembers: { type: [Number, String], default: null }
})

const localDesc         = ref(props.description)
const localStatus       = ref(props.status)
const localTime         = ref(props.time)
const localProjectType  = ref(props.projectType)
const localProjectId    = ref(props.projectId)
const localAssigneeIds  = ref([...(props.assigneeIds || [])])

const emit = defineEmits(['close', 'update', 'delete'])

const allProjects = ref([])
const members     = ref([])

function getHeaders() {
  const token = localStorage.getItem('token')
  return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
}

onMounted(async () => {
  const res = await fetch(`${API}/api/projects`, { headers: getHeaders() })
  allProjects.value = await res.json()

  if (props.projectIdForMembers) {
    const [mRes, meRes] = await Promise.all([
      fetch(`${API}/api/projects/${props.projectIdForMembers}/members`, { headers: getHeaders() }),
      fetch(`${API}/api/me`, { headers: getHeaders() })
    ])
    const memberList = await mRes.json()
    const me         = await meRes.json()

    const alreadyIn = memberList.some(m => m.user_id === me.id)
    if (!alreadyIn) {
      memberList.unshift({
        user_id:    me.id,
        name:       me.name,
        email:      me.email,
        avatar_url: me.avatar_url || '',
        role:       'Owner'
      })
    }
    members.value = memberList
  }
})

const filteredProjects = computed(() =>
  allProjects.value.filter(p => p.type?.toLowerCase() === localProjectType.value?.toLowerCase())
)

function toggleAssignee(userId) {
  const idx = localAssigneeIds.value.indexOf(userId)
  if (idx === -1) {
    localAssigneeIds.value.push(userId)
  } else {
    localAssigneeIds.value.splice(idx, 1)
  }
  emitUpdate({ assignee_ids: [...localAssigneeIds.value] })
}

const avatarColors = ['#3b82f6', '#a855f7', '#f97316', '#10b981', '#ef4444', '#ec4899']
function getColor(name) {
  if (!name) return '#e2e8f0'
  let hash = 0
  for (let i = 0; i < name.length; i++) hash += name.charCodeAt(i)
  return avatarColors[hash % avatarColors.length]
}
function getInitials(name) {
  if (!name) return '?'
  return name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase()
}

function emitUpdate(data) {
  emit('update', data)
}
</script>

<style scoped>
/* ── Modal Overlay ── */
.task-page {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 16px; /* Prevent modal touching edges on small screens */
  box-sizing: border-box;
}

/* ── Modal Container ── */
.modal {
  background: #fff;
  border-radius: 16px;
  width: 500px;
  max-width: 100%; /* Better for mobile */
  padding: 24px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.12);
  max-height: 85vh;
  overflow-y: auto;
  box-sizing: border-box;
}

@media (max-width: 480px) {
  .modal {
    padding: 20px 16px;
  }
}

/* ── Modal Header ── */
.modal-header { 
    display: flex; 
    justify-content: space-between; 
    align-items: flex-start; 
    margin-bottom: 8px; 
    gap: 12px;
}
.modal-header h1 { 
    margin: 0; 
    font-size: 18px; 
    font-weight: 700; 
    color: #1a1a2e; 
    line-height: 1.3;
}

.delete-btn {
  border: none; background: none; color: #ef4444;
  cursor: pointer; padding: 6px; border-radius: 8px; display: flex;
  flex-shrink: 0;
}
.delete-btn:hover { background: #fee2e2; }

/* ── Form Fields ── */
.selected-prob { margin-top: 16px; }

.field { 
    display: flex; 
    align-items: center; 
    padding: 12px 0; 
    border-bottom: 1px solid #f0f0f0; 
    gap: 12px; 
    flex-wrap: wrap; /* Important for small screens */
}
.field label { 
    width: 130px; 
    font-size: 14px; 
    color: #7f8c9b; 
    flex-shrink: 0; 
}

@media (max-width: 480px) {
  .field label {
    width: 100%; /* Stack labels on very small screens */
    padding-bottom: 4px;
  }
}

/* ── Inputs & Selects ── */
.date-input { 
    border: 1px solid #e0e0e0; 
    border-radius: 8px; 
    padding: 6px 10px; 
    font-size: 14px; 
    color: #2c3e50; 
    background: #fff; 
    cursor: pointer; 
    outline: none; 
    flex: 1;
    min-width: 120px;
}
.date-input:focus { border-color: #a0aec0; }

.status-select { 
    color: #fff !important; 
    padding: 4px 12px; 
    border-radius: 12px; 
    font-size: 13px; 
    border: none; 
    cursor: pointer; 
}
.status-not-started { background: #9ca3af; }
.status-in-progress { background: #3b82f6; }
.status-completed   { background: #22c55e; }

.type-select { 
    padding: 6px 12px; 
    border: 1px solid #e0e0e0; 
    border-radius: 8px; 
    font-size: 13px; 
    color: #2c3e50; 
    background: #fff; 
    cursor: pointer; 
    outline: none; 
    flex: 1;
    min-width: 150px;
}

/* ── Assignees List ── */
.assignee-select-wrap { 
    display: flex; 
    flex-wrap: wrap; 
    gap: 6px; 
    flex: 1; 
}
.assignee-option {
  display: flex; align-items: center; gap: 6px;
  padding: 4px 10px 4px 4px;
  border: 1px solid #e2e8f0; border-radius: 20px;
  cursor: pointer; font-size: 12px; color: #334155; transition: all 0.15s;
}
.assignee-option:hover  { border-color: #3b82f6; background: #eff6ff; }
.assignee-option.active { border-color: #3b82f6; background: #eff6ff; color: #3b82f6; font-weight: 600; }
.check-icon { color: #3b82f6; }
.no-members-msg { font-size: 12px; color: #94a3b8; padding-top: 4px;}

.avatar-sm {
  width: 22px; height: 22px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  color: #fff; font-size: 9px; font-weight: 700; overflow: hidden; flex-shrink: 0;
}
.avatar-img { width: 100%; height: 100%; object-fit: cover; border-radius: 50%; }

/* ── Textarea ── */
.description {
  margin-top: 16px; width: 100%; min-height: 120px;
  border: 1px solid #e0e0e0; border-radius: 8px; padding: 12px;
  font-size: 14px; color: #2c3e50; outline: none; resize: vertical;
  font-family: inherit; box-sizing: border-box;
}
.description:focus { border-color: #a0aec0; }
</style>