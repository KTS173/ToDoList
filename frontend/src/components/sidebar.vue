<template>
  <aside id="sidebar" :class="{ 'collapsed': isCollapsed, 'mobile-open': isMobileOpen }">

    <!-- ── Logo Section ── -->
    <div class="sb-logo">
      <button class="sb-toggle" @click="toggleSidebar">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10" />
          <polyline points="9 12 11 14 15 10" />
        </svg>
      </button>
      <RouterLink to="/" class="sb-logo-text" @click="emit('close-mobile')">CMU TO DO LIST</RouterLink>
    </div>

    <!-- ── Search Area ── -->
    <div class="sb-search">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
        stroke-linecap="round" stroke-linejoin="round">
        <circle cx="11" cy="11" r="8" />
        <line x1="21" y1="21" x2="16.65" y2="16.65" />
      </svg>
      <input v-model="searchQuery" type="text" placeholder="Search tasks..." />
    </div>

    <!-- ── Main Navigation ── -->
    <!-- 
      [Checklist: มี navigation menu (Y)]
      ส่วนนี้คือโครงสร้าง Sidebar ที่มีรายการเมนู (Link) 
      การทำงาน: มันทำหน้าที่เป็น Navigation Menu ให้คนดูรู้ว่ามีหน้าไหนบ้าง 
      Component นี้ถูกดึงไปใช้ครอบทุกๆ หน้าที่ล็อคอินแล้ว เพื่อให้คลิกสลับเปลี่ยนหน้าได้ง่ายๆ
    -->
    <ul class="sb-nav">
      <li class="sb-item">
        <RouterLink to="/overview" class="sb-link" active-class="sb-active" @click="emit('close-mobile')">
          <svg class="sb-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="7" height="7" />
            <rect x="14" y="3" width="7" height="7" />
            <rect x="14" y="14" width="7" height="7" />
            <rect x="3" y="14" width="7" height="7" />
          </svg>
          <span class="sb-label">Overview</span>
        </RouterLink>
      </li>

      <li class="sb-item">
        <RouterLink to="/" class="sb-link" exact-active-class="sb-active" @click="emit('close-mobile')">
          <svg class="sb-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round">
            <polyline points="22 12 16 12 14 15 10 15 8 12 2 12" />
            <path
              d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z" />
          </svg>
          <span class="sb-label">Inbox</span>
          <span v-if="stats.inbox > 0" class="sb-badge">{{ stats.inbox }}</span>
        </RouterLink>
      </li>

      <li class="sb-item">
        <RouterLink to="/today" class="sb-link" active-class="sb-active" @click="emit('close-mobile')">
          <svg class="sb-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="4" width="18" height="18" rx="2" />
            <line x1="16" y1="2" x2="16" y2="6" />
            <line x1="8" y1="2" x2="8" y2="6" />
            <line x1="3" y1="10" x2="21" y2="10" />
          </svg>
          <span class="sb-label">Today</span>
          <span v-if="stats.today > 0" class="sb-badge">{{ stats.today }}</span>
        </RouterLink>
      </li>

      <li class="sb-item">
        <RouterLink to="/upcoming" class="sb-link" active-class="sb-active" @click="emit('close-mobile')">
          <svg class="sb-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10" />
            <polyline points="12 6 12 12 16 14" />
          </svg>
          <span class="sb-label">Next 7 days</span>
          <span v-if="stats.upcoming > 0" class="sb-badge">{{ stats.upcoming }}</span>
        </RouterLink>
      </li>

      <li class="sb-item">
        <RouterLink to="/calendar" class="sb-link" active-class="sb-active" @click="emit('close-mobile')">
          <svg class="sb-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="4" width="18" height="18" rx="2" />
            <line x1="16" y1="2" x2="16" y2="6" />
            <line x1="8" y1="2" x2="8" y2="6" />
            <line x1="3" y1="10" x2="21" y2="10" />
          </svg>
          <span class="sb-label">Calendar</span>
        </RouterLink>
      </li>

      <li class="sb-item">
        <RouterLink to="/plan" class="sb-link" active-class="sb-active" @click="emit('close-mobile')">
          <svg class="sb-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="7" height="7" />
            <rect x="14" y="3" width="7" height="7" />
            <rect x="14" y="14" width="7" height="7" />
            <rect x="3" y="14" width="7" height="7" />
          </svg>
          <span class="sb-label">Year Plan</span>
        </RouterLink>
      </li>

      <li class="sb-item">
        <RouterLink to="/completed" class="sb-link" active-class="sb-active" @click="emit('close-mobile')">
          <svg class="sb-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
            stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="10" />
            <polyline points="9 12 11 14 15 10" />
          </svg>
          <span class="sb-label">Completed</span>
          <span class="sb-badge" v-if="stats.completed">{{ stats.completed }}</span>
        </RouterLink>
      </li>

    </ul>

    <div class="sb-divider"></div>

    <!-- ── Personal Projects Section ── -->
    <div class="sb-section">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
        stroke-linecap="round" stroke-linejoin="round">
        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
        <circle cx="12" cy="7" r="4" />
      </svg>
      <span>PERSONAL</span>
      <button class="sb-add-btn" @click="startAdding('personal')">+</button>
    </div>

    <ul class="sb-nav">
      <li v-for="p in personalProjects" :key="p.id" class="sb-item">
        <RouterLink :to="`/project/${p.id}`" class="sb-link" active-class="sb-active" @click="emit('close-mobile')">
          <span class="sb-emoji">{{ p.emoji }}</span>
          <span class="sb-label">{{ p.name }}</span>
        </RouterLink>
      </li>

      <li v-if="addingSection === 'personal'" class="sb-item">
        <div class="sb-link sb-adding">
          <span class="sb-emoji">💡</span>
          <input ref="addInputRef" v-model="newProjectName" type="text" placeholder="Project name..."
            @keyup.enter="confirmAdd" @keyup.esc="cancelAdd" />
        </div>
      </li>
    </ul>

    <div class="sb-divider"></div>

    <!-- ── Corporate Projects Section ── -->
    <div class="sb-section">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
        stroke-linecap="round" stroke-linejoin="round">
        <rect x="2" y="7" width="20" height="14" rx="2" />
        <path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2" />
      </svg>
      <span>CORPORATE</span>
      <button class="sb-add-btn" @click="startAdding('corporate')">+</button>
    </div>

    <ul class="sb-nav">
      <li v-for="p in corporateProjects" :key="p.id" class="sb-item">
        <RouterLink :to="`/corporate/${p.id}`" class="sb-link" active-class="sb-active" @click="emit('close-mobile')">
          <span class="sb-emoji">{{ p.emoji }}</span>
          <span class="sb-label">{{ p.name }}</span>
          <span v-if="p.active" class="sb-dot"></span>
        </RouterLink>
      </li>

      <li v-if="addingSection === 'corporate'" class="sb-item">
        <div class="sb-link sb-adding">
          <span class="sb-emoji">💼</span>
          <input ref="addInputRef" v-model="newProjectName" type="text" placeholder="Project name..."
            @keyup.enter="confirmAdd" @keyup.esc="cancelAdd" />
        </div>
      </li>
    </ul>



    <!-- ── Settings & Footer Section ── -->
    <div class="sb-footer">
      <RouterLink to="/settings" class="sb-link" active-class="sb-active" @click="emit('close-mobile')">
        <svg class="sb-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="3" />
          <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
        </svg>
        <span class="sb-label">Settings</span>
      </RouterLink>
      <a href="#" class="sb-link" @click.prevent="$emit('sign-out')">
        <svg class="sb-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
          <polyline points="16 17 21 12 16 7" />
          <line x1="21" y1="12" x2="9" y2="12" />
        </svg>
        <span class="sb-label">Sign out</span>
      </a>
    </div>

  </aside>
</template>

<script setup>
import { ref, nextTick, onMounted, watch } from 'vue'
import { RouterLink } from 'vue-router'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const props = defineProps({
  isMobileOpen: { type: Boolean, default: false }
})

const emit           = defineEmits(['sign-out', 'search', 'close-mobile'])
const isCollapsed    = ref(false)
const searchQuery    = ref('')
const addingSection  = ref(null)
const newProjectName = ref('')
const addInputRef    = ref(null)

const personalProjects  = ref([])
const corporateProjects = ref([])
const stats = ref({ inbox: 0, today: 0, upcoming: 0, completed: 0 })

function toggleSidebar() {
  if (window.innerWidth <= 768) {
    emit('close-mobile')
  } else {
    isCollapsed.value = !isCollapsed.value
  }
}

function getHeaders() {
  const token = localStorage.getItem('token')
  return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
}

watch(searchQuery, (q) => emit("search", q))

async function fetchProjects() {
  const res  = await fetch(`${API}/api/projects`, { headers: getHeaders() })  
  const data = await res.json()
  personalProjects.value  = data.filter(p => p.type === 'personal')
  corporateProjects.value = data.filter(p => p.type === 'corporate')
}

async function fetchTaskStats() {
  const res   = await fetch(`${API}/api/tasks`, { headers: getHeaders() })  
  const tasks = await res.json()

  const now   = new Date()
  const today = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`

  stats.value.inbox     = tasks.filter(t => !t.is_completed).length
  stats.value.today     = tasks.filter(t => t.due_date === today && !t.is_completed).length
  stats.value.completed = tasks.filter(t => t.is_completed).length

  const next7 = new Date()
  next7.setDate(next7.getDate() + 7)
  stats.value.upcoming = tasks.filter(t => {
    if (!t.due_date || t.is_completed) return false
    const d = new Date(t.due_date)
    return d <= next7 && d >= new Date()
  }).length
}

onMounted(() => {
  fetchProjects()
  fetchTaskStats()
  window.addEventListener("tasks-updated", fetchTaskStats)
  window.addEventListener("projects-updated", fetchProjects)
})

async function startAdding(section) {
  if (addingSection.value === section) { cancelAdd(); return }
  addingSection.value  = section
  newProjectName.value = ''
  await nextTick()
  addInputRef.value?.focus()
}

async function confirmAdd() {
  const name = newProjectName.value.trim()
  if (!name) { cancelAdd(); return }

  const emoji = addingSection.value === 'personal' ? '💡' : '💼'
  const type  = addingSection.value

  // [Checklist: ตัวอย่างการใช้ Fetch API สำหรับส่ง/สร้างข้อมูล (POST Request)]
  // 1. สร้าง Request กำหนด Method เป็น POST และระบุ Header 
  const res = await fetch(`${API}/api/projects`, {
    method:  'POST',
    headers: getHeaders(),  
    // 2. แปลงข้อมูล Object จากฟอร์มหน้าจอให้กายเป็น JSON String สำหรับส่งผ่าน Network
    body:    JSON.stringify({ name, emoji, type })
  })
  
  // 3. เช็ค Response ว่าสำเร็จหรือไม่ ถ้าได้ 400 (เช่นชื่อซ้ำ) ให้โชว์ Alert จาก Error ของตัว Backend
  if (!res.ok) {
    const errorData = await res.json()
    alert(errorData.detail || "Failed to create project")
    return
  }
  
  // 4. หากผ่าน ดึงก้อนข้อมูลโปรเจกต์ใหม่ยัดเข้า Sidebar ฝั่งหน้าบ้าน (โดยไม่ต้องรอรีเฟรชหน้าต่าง)
  const project = await res.json()

  if (type === 'personal') personalProjects.value.push(project)
  else corporateProjects.value.push(project)

  window.dispatchEvent(new Event('projects-updated'))
  cancelAdd()
}

function cancelAdd() {
  addingSection.value  = null
  newProjectName.value = ''
}
</script>

<style scoped>
/* ── Sidebar ── */
#sidebar {
  width: 260px;
  min-height: 100vh;
  background: #f0ede8;
  display: flex;
  flex-direction: column;
  padding: 20px 12px;
  box-sizing: border-box;
  font-family: 'DM Sans', 'Segoe UI', sans-serif;
  transition: width 0.25s ease, transform 0.3s ease;
  overflow: hidden;
  flex-shrink: 0;
  z-index: 100;
}

#sidebar.collapsed {
  width: 68px;
}

#sidebar.collapsed .sb-logo-text,
#sidebar.collapsed .sb-search,
#sidebar.collapsed .sb-label,
#sidebar.collapsed .sb-badge,
#sidebar.collapsed .sb-section span,
#sidebar.collapsed .sb-add-btn {
  display: none;
}

#sidebar.collapsed .sb-link {
  justify-content: center;
}

/* ── Logo ── */
.sb-logo {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 18px;
  padding: 0 4px;
}

.sb-toggle {
  background: none;
  border: none;
  cursor: pointer;
  color: #3b82f6;
  padding: 4px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  flex-shrink: 0;
  transition: background 0.15s;
}

.sb-toggle:hover {
  background: #e4e0da;
}

.sb-logo-text {
  font-size: 20px;
  font-weight: 700;
  color: #1a1a1a;
  text-decoration: none;
  white-space: nowrap;
}

/* ── Search ── */
.sb-search {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #e8e4df;
  border-radius: 10px;
  padding: 9px 14px;
  margin-bottom: 14px;
}

.sb-search svg {
  color: #aaa;
  flex-shrink: 0;
}

.sb-search input {
  border: none;
  background: transparent;
  font-size: 14px;
  color: #1a1a1a;
  outline: none;
  width: 100%;
  font-family: inherit;
}

.sb-search input::placeholder {
  color: #aaa;
}

/* ── Nav ── */
.sb-nav {
  list-style: none;
  padding: 0;
  margin: 0 0 4px;
}

.sb-item {
  margin-bottom: 2px;
}

/* ── Link ── */
.sb-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 12px;
  border-radius: 10px;
  text-decoration: none;
  color: #1a1a1a;
  font-size: 14.5px;
  font-weight: 500;
  transition: background 0.12s;
  cursor: pointer;
  width: 100%;
  box-sizing: border-box;
}

.sb-link:hover {
  background: #e4e0da;
  color: #1a1a1a;
}

.sb-active {
  background: #e0eaff !important;
  color: #3b82f6 !important;
}

/* ทำให้ icon และ badge เป็นสีฟ้าด้วย */
.sb-active .sb-ic,
.sb-active .sb-badge {
  background: #dbeafe;
  color: #3b82f6;
}

.sb-icon {
  width: 18px;
  height: 18px;
  flex-shrink: 0;
}

.sb-label {
  flex: 1;
}

.sb-emoji {
  width: 20px;
  text-align: center;
  flex-shrink: 0;
  font-size: 16px;
}

/* ── Inline add ── */
.sb-adding {
  background: #e4e0da;
}

.sb-adding input {
  flex: 1;
  min-width: 0;
  border: none;
  background: transparent;
  font-size: 14.5px;
  font-weight: 500;
  color: #1a1a1a;
  outline: none;
  padding: 0;
  font-family: inherit;
}

.sb-adding input::placeholder {
  color: #aaa;
  font-weight: 400;
}

/* ── Badge ── */
.sb-badge {
  font-size: 12px;
  font-weight: 600;
  border-radius: 20px;
  padding: 1px 8px;
  flex-shrink: 0;
}

.sb-badge.blue {
  background: #c7d9ff;
  color: #3b82f6;
}

.sb-badge.muted {
  background: transparent;
  color: #aaa;
}

/* ── Dot ── */
.sb-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #22c55e;
  flex-shrink: 0;
}

/* ── Divider ── */
.sb-divider {
  height: 1px;
  background: #e0ddd8;
  margin: 8px 4px;
}

/* ── Section ── */
.sb-section {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 4px 12px;
  color: #999;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-family: inherit;
}

.sb-section span {
  flex: 1;
}

.sb-add-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #bbb;
  font-size: 18px;
  line-height: 1;
  padding: 0 4px;
  border-radius: 5px;
  transition: color 0.12s, background 0.12s;
}

.sb-add-btn:hover {
  color: #1a1a1a;
  background: #e4e0da;
}

/* ── Footer ── */
.sb-footer {
  margin-top: auto;
  padding-top: 8px;
  border-top: 1px solid #e0ddd8;
}

.sb-footer .sb-link {
  color: #888;
  font-weight: 400;
}

/* ── Mobile Responsive ── */
@media (max-width: 768px) {
  #sidebar {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    transform: translateX(-100%);
    width: 280px; /* Slightly wider on mobile for better touch targets */
  }

  #sidebar.mobile-open {
    transform: translateX(0);
  }

  #sidebar.collapsed {
    width: 280px; /* Disable collapse on mobile */
  }

  #sidebar.collapsed .sb-logo-text,
  #sidebar.collapsed .sb-search,
  #sidebar.collapsed .sb-label,
  #sidebar.collapsed .sb-badge,
  #sidebar.collapsed .sb-section span,
  #sidebar.collapsed .sb-add-btn {
    display: flex; /* Override hide */
  }

  #sidebar.collapsed .sb-link {
    justify-content: flex-start;
  }
}
</style>