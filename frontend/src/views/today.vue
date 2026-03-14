<template>
  <div class="inbox-page">

    <TaskStatus :tasks="tasks" />

    <AddTask msg="Add New Task" @add="handleAdd" />

    <TaskList
      title="Today"
      :subtitle="formattedToday"
      :tasks="todayTasks"
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
import AddTask   from '../components/AddTask.vue'
import TaskList  from '../components/TaskList.vue'
import TaskModal from '../components/TaskModal.vue'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const tasks        = ref([])
const selectedTask = ref(null)
const props        = defineProps({ search: String })
const today        = new Date().toLocaleDateString('sv-SE')

function getHeaders() {
    const token = localStorage.getItem('token')
    return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
}

async function loadTasks() {
    // [Checklist: เพจและ content ที่ควร dynamic ไม่ควรทำเป็น static page (Y)]
    // [Checklist: ตัวอย่างการใช้ Fetch API สำหรับดึงข้อมูล (GET Request)]
    // ส่วนนี้คือการยิง Fetch API 
    // การทำงาน: หน้าจอเราไม่ต้อง Hardcode เป็น HTML แบบ static คงที่ 
    // แต่โค้ดนี้จะไปดึงตัวงาน (Tasks) ของจริงในแต่ละวัน มาอัปเดตตัวแปร list (tasks.value)
    // เพื่อให้ Vue นำไปปั้นหน้าจอให้เป็น Dynamic มีความพลวัตตอบสนองตามข้อมูล 
    
    // 1. ส่ง Request พร้อมแบก Token แนบไปกับ Header
    const res = await fetch(`${API}/api/tasks`, { headers: getHeaders() })
    // 2. แปลงผลลัพธ์ที่ได้กลับมาจาก JSON string เป็น Object/Array ของ Javascript
    const data = await res.json()
    // 3. แมปค่ากลับเข้าไปยัง Reactive State ให้ Vue รู้วาต้องวาดหน้าจอใหม่
    tasks.value = data.map(t => ({
        id: t.id, name: t.title, tag: t.tag || '', done: t.is_completed,
        due_date: t.due_date, status: t.status, due_time: t.due_time,
        description: t.description, project_type: t.project_type, project_id: t.project_id
    }))
}

const todayTasks = computed(() => {
    let data = tasks.value.filter(t => !t.done && t.due_date === today)
    if (props.search) {
        const q = props.search.toLowerCase()
        data = data.filter(t => t.name.toLowerCase().includes(q))
    }
    return data
})

async function handleAdd(data) {
    await fetch(`${API}/api/tasks`, { method: 'POST', headers: getHeaders(), body: JSON.stringify({ title: data.title, due_date: data.due_date || today, due_time: data.due_time || null }) })
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

const formattedToday = computed(() => new Date().toLocaleDateString('en-US', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }))

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

/* ── Component Container ── */
.card-container {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap; /* Ensure wrapping on smaller devices */
}
</style>