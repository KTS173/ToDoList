<template>
    <div class="overview">
        <div class="overview-head">
            <div class="head-left">
                <h1 class="head-greeting">{{ greeting }}, {{ me?.name || username }}!</h1>
                <p class="head-sub">Here's what's happening with your projects today.</p>
            </div>
            <div class="head-right">
                <div class="head-search">
                    <Search :size="16" class="head-search-icon" />
                    <input type="text" placeholder="Search projects, tasks, tags..." />
                </div>
                <button class="head-notif">
                    <Bell :size="20" />
                </button>
                <div class="head-avatar">
                    <img 
                        v-if="me?.avatar_url" 
                        :src="`${API}${me.avatar_url}`" 
                        style="width:100%;height:100%;object-fit:cover;border-radius:50%;"
                    />
                    <User v-else :size="20" />
                </div>
            </div>
        </div>

        <div class="overview-body">
            <div class="overview-tab">
                <button 
                    :class="{active: activeTab === 'personal'}" 
                    @click="activeTab = 'personal'"
                >
                    Personal
                </button>
                <button 
                    :class="{active: activeTab === 'corporate'}"
                    @click="activeTab = 'corporate'"
                >
                    Corporate
                </button>
            </div>

            <div class="overview-card">
                <NewProjectCard @click="showCreateModal = true" />
                <ProjectCard
                    v-for="p in filteredProjects"
                    :key="p.id"
                    :project_title="p.name"
                    :done="getProjectStats(p.id).done"
                    :todo="getProjectStats(p.id).todo"
                    :percent="getProjectStats(p.id).percent"
                    :showTeam="activeTab === 'corporate'"
                    :members="projectMembers[p.id] || []"
                    :details="p.description"
                    :color="p.color"
                    :emoji="p.emoji"

                    @click="$router.push(activeTab === 'corporate' ? `/corporate/${p.id}` : `/project/${p.id}`)"
                    @delete="deleteProject(p.id)"
                    @add-member="openAddMember(p.id)"
                    @edit="openEdit(p)"

                />
            </div>

            <div class="overview-event">
                <div class="active-chart"></div>
                <div class="upcomming"></div>

            </div>

        </div>

        <ProjectModal v-model="showCreateModal" @created="onProjectCreated" />
        <AddMemberModal
            v-model="showAddMemberModal"
            :project-id="selectedProjectId"
            :members="projectMembers[selectedProjectId] || []"
            @members-changed="refreshMembers"
        />

        <EditProjectModal
            v-model="showEditModal"
            :project="editingProject"
            @updated="onProjectUpdated"
        />

    </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { Search, Bell, User } from 'lucide-vue-next'
import ProjectCard from '@/components/overview/ProjectCard.vue'
import NewProjectCard from '@/components/overview/NewProjectCard.vue'
import ProjectModal from '@/components/overview/modal/ProjectModal.vue'
import AddMemberModal from '@/components/overview/modal/AddMemberModal.vue'
import EditProjectModal from '@/components/overview/modal/EditProjectModal.vue'

const showCreateModal = ref(false)
const showAddMemberModal = ref(false)
const selectedProjectId = ref(null)

const activeTab = ref('personal')
const projects = ref([])
const projectTasks = ref({})
const projectMembers = ref({})

const showEditModal = ref(false)
const editingProject = ref(null)
const me = ref(null)


const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function getHeaders() {
  const token = localStorage.getItem('token')
  return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
}

async function onProjectCreated() {
  await fetchProjects()
  window.dispatchEvent(new Event('projects-updated'))
}

async function onProjectUpdated() {
  await fetchProjects()
  window.dispatchEvent(new Event('projects-updated'))
}

function openEdit(project) {
  editingProject.value = project
  showEditModal.value = true
}

async function fetchProjects() {
    const res = await fetch(`${API}/api/projects/overview`, { headers: getHeaders() })
    const data = await res.json()
    projects.value = data.map(d => d.project)
    for (const d of data) {
        projectTasks.value[d.project.id] = d.tasks
        projectMembers.value[d.project.id] = d.members
    }
}


function openAddMember(projectId) {
    selectedProjectId.value = projectId
    showAddMemberModal.value = true
}

async function refreshMembers() {
    if (!selectedProjectId.value) return
    const res = await fetch(`${API}/api/projects/${selectedProjectId.value}/members`, { headers: getHeaders() })
    projectMembers.value[selectedProjectId.value] = await res.json()
}

const filteredProjects = computed(() =>
    projects.value.filter(p => p.type === activeTab.value)
)

function getProjectStats(projectId) {
    const tasks = projectTasks.value[projectId] || []
    const done = tasks.filter(t => t.status === 'Completed').length
    const todo = tasks.filter(t => t.status === 'Not started').length
    const total = tasks.length
    const percent = total ? Math.round(done / total * 100) : 0
    return { done, todo, percent }
}

const greeting = computed(() => {
    const h = new Date().getHours()
    if (h < 12) return 'Good Morning'
    if (h < 18) return 'Good Afternoon'
    return 'Good Evening'
})

const deleteProject = async (projectId) => {
    await fetch(`${API}/api/projects/${projectId}`, { method: 'DELETE', headers: getHeaders() })
    projects.value = projects.value.filter(p => p.id !== projectId)
    window.dispatchEvent(new Event('projects-updated'))
}

async function fetchMe() {
  const res = await fetch(`${API}/api/me`, { headers: getHeaders() })
  me.value = await res.json()
}

onMounted(() => {
  fetchProjects()
  fetchMe()
  window.addEventListener('projects-updated', fetchProjects)
})

 
</script>

<style scoped>
/* ── Layout & Typography ── */
.overview {
    padding: 32px 40px;
    min-height: 100vh;
    background: #f8f9fb;
    font-family: 'DM Sans', 'Segoe UI', sans-serif;
}

@media (max-width: 480px) {
    .overview {
        padding: 20px 16px; /* Less padding on small screens */
    }
}

/* ── Header Section ── */
.overview-head {
    display: flex;
    justify-content: space-between;
    align-items: flex-start; /* Better alignment when wrapped */
    margin-bottom: 24px;
    flex-wrap: wrap; /* Allow wrapping on small screens */
    gap: 16px;
}

/* ── Greeting ── */
.head-left h1 {
    font-size: 28px;
    font-weight: 700;
    color: #1a1a2e;
    margin: 0;
}
.head-sub {
    color: #888;
    font-size: 14px;
    margin: 4px 0 0;
}

/* ── Header Controls (Search, Notif, Avatar) ── */
.head-right {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap; /* Support narrow screens */
    width: 100%; /* For small screens */
    justify-content: flex-end; /* Align right on desktop */
}

@media (min-width: 768px) {
    .head-right {
        width: auto; /* Revert on larger screens */
    }
}

/* ── Search Bar ── */
.head-search {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 8px 14px;
    min-width: 260px;
    flex: 1; /* Take up available space on mobile */
}
.head-search-icon { color: #aaa; }
.head-search input {
    border: none;
    outline: none;
    font-size: 13px;
    width: 100%;
    font-family: inherit;
    color: #333;
}
.head-search input::placeholder { color: #bbb; }

/* ── Notifications & Avatar ── */
.head-notif {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    padding: 8px;
    cursor: pointer;
    color: #555;
    display: flex;
    align-items: center;
    flex-shrink: 0;
}
.head-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: #1a1a2e;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    overflow: hidden;
}

/* ── Tabs (Personal/Corporate) ── */
.overview-tab {
  display: flex;
  gap: 4px;
  margin-bottom: 24px;
  border-bottom: 1px solid #e5e7eb;
  overflow-x: auto; /* Enable horizontal scroll if needed */
  /* Hide scrollbar for cleaner look */
  -ms-overflow-style: none;  /* IE and Edge */
  scrollbar-width: none;  /* Firefox */
}
.overview-tab::-webkit-scrollbar {
  display: none;
}

.overview-tab button {
  padding: 10px 20px;
  border: none;
  background: none;
  color: #888;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  font-family: inherit;
  transition: all 0.25s;
  white-space: nowrap;
}

.overview-tab button:hover {
  color: #333;
}

.overview-tab button.active {
  color: #3b82f6;
  border-bottom-color: #3b82f6;
}

/* ── Cards Container ── */
.overview-card {
    display: flex;
    gap: 24px;
    flex-wrap: wrap;
}
</style>