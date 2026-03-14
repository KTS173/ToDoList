<template>
  <div class="calendar-page">
    <div class="calendar-header">
      <h1 class="page-title">Calendar</h1>
      <div class="legend">
        <span class="legend-item"><span class="dot personal"></span>Personal</span>
        <span class="legend-item"><span class="dot corporate"></span>Corporate</span>
        <span class="legend-item"><span class="dot no-project"></span>No Project</span>
        <span class="legend-item"><span class="dot done"></span>Done</span>
      </div>
    </div>
    <FullCalendar :options="options" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import interactionPlugin from '@fullcalendar/interaction'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function getHeaders() {
  const token = localStorage.getItem('token')
  return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
}

const options = ref({
  plugins: [dayGridPlugin, interactionPlugin],
  initialView: 'dayGridMonth',
  headerToolbar: {
    left: 'title',
    center: '',
    right: 'prev,today,next'
  },
  height: 'auto',
  fixedWeekCount: false,
  dayMaxEvents: 3,
  eventClick: (info) => {
    info.jsEvent.preventDefault()
  },
  events: []
})

async function fetchAllTasks() {
  try {
    // ดึง projects ทั้งหมดก่อน
    const projRes  = await fetch(`${API}/api/projects`, { headers: getHeaders() })
    const projects = await projRes.json()

    // ดึง personal tasks
    const taskRes    = await fetch(`${API}/api/tasks`, { headers: getHeaders() })
    const allMyTasks = await taskRes.json()

    const events = []

    // tasks ที่ไม่มี project (personal standalone)
    const standaloneTasks = allMyTasks.filter(t => !t.project_id)
    for (const t of standaloneTasks) {
      if (!t.due_date) continue
      events.push({
        id:    `task-${t.id}`,
        title: t.title,
        date:  t.due_date,
        color: t.is_completed ? '#94a3b8' : '#10b981',
        extendedProps: { type: 'personal' }
      })
    }

    // tasks ใน projects แต่ละอัน
    for (const proj of projects) {
      const res   = await fetch(`${API}/api/projects/${proj.id}/tasks`, { headers: getHeaders() })
      const tasks = await res.json()

      const isPersonal  = proj.type?.toLowerCase() === 'personal'
      const isCorporate = proj.type?.toLowerCase() === 'corporate'
      const baseColor   = isCorporate ? '#7c3aed' : '#3b82f6'

      for (const t of tasks) {
        if (!t.due_date) continue
        events.push({
          id:    `proj-${proj.id}-task-${t.id}`,
          title: `${proj.emoji || ''} ${t.title}`,
          date:  t.due_date,
          color: t.is_completed ? '#94a3b8' : baseColor,
          extendedProps: { type: proj.type, projectName: proj.name }
        })
      }
    }

    options.value = { ...options.value, events }
  } catch (err) {
    console.error('Failed to fetch tasks', err)
  }
}

onMounted(fetchAllTasks)
</script>

<style>
/* ── Base Layout ── */
.calendar-page {
  padding: 32px 40px;
  background: #f7f5f2;
  min-height: 100vh;
  font-family: 'DM Sans', 'Segoe UI', sans-serif;
  box-sizing: border-box; /* Ensure padding is included in element's total width and height */
  width: 100%; /* Take full width */
}

@media (max-width: 768px) {
  .calendar-page {
    padding: 20px 16px; /* Reduce padding on mobile */
  }
}

/* ── Header ── */
.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap; /* Allow items to wrap on smaller screens */
  gap: 16px; /* Add gap between items when wrapped */
}

.page-title {
  font-size: 26px;
  font-weight: 700;
  color: #1a1a1a;
  margin: 0;
}

/* ── Legend ── */
.legend {
  display: flex;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap; /* Allow legend items to wrap */
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #555;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.dot.personal    { background: #3b82f6; }
.dot.corporate   { background: #7c3aed; }
.dot.no-project  { background: #10b981; }
.dot.done        { background: #94a3b8; }

/* ── FullCalendar Toolbar ── */
.fc .fc-toolbar { margin-bottom: 20px; align-items: center; }
.fc .fc-toolbar-title { font-size: 22px; font-weight: 700; color: #1a1a1a; }

.fc .fc-button {
  background: transparent !important; border: none !important;
  box-shadow: none !important; color: #555 !important;
  font-size: 14px !important; font-weight: 500 !important;
  padding: 6px 12px !important; border-radius: 8px !important;
  font-family: inherit !important; transition: background 0.15s !important;
}
.fc .fc-button:hover     { background: #e4e0da !important; color: #1a1a1a !important; }
.fc .fc-button:focus     { box-shadow: none !important; outline: none !important; }
.fc .fc-today-button     { font-weight: 600 !important; }
.fc .fc-button-primary:not(:disabled).fc-button-active { background: transparent !important; color: #3b82f6 !important; }

/* ── Grid ── */
.fc .fc-view-harness { background: #fff; border-radius: 16px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
.fc .fc-col-header { background: #fff; }
.fc .fc-col-header-cell { padding: 14px 0; border-color: #ece9e4; }
.fc .fc-col-header-cell-cushion { font-size: 12px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #999; text-decoration: none; }
.fc .fc-daygrid-day { border-color: #ece9e4; }
.fc .fc-daygrid-day-frame { padding: 8px; min-height: 90px; }
.fc .fc-daygrid-day-number { font-size: 14px; font-weight: 500; color: #1a1a1a; text-decoration: none; padding: 2px 4px; border-radius: 50%; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; }
.fc .fc-daygrid-day-number:hover { background: #f0ede8; }
.fc .fc-day-today { background: #f0f4ff !important; }
.fc .fc-day-today .fc-daygrid-day-number { background: #3b82f6; color: #fff; }
.fc .fc-day-past .fc-daygrid-day-number { color: #bbb; }
.fc .fc-scrollgrid { border-color: #ece9e4; border-radius: 16px; }
.fc .fc-scrollgrid td, .fc .fc-scrollgrid th { border-color: #ece9e4; }
.fc .fc-event { border: none; border-radius: 6px; font-size: 12px; padding: 2px 6px; font-family: inherit; }
.fc .fc-event:hover { filter: brightness(0.9); }
</style>