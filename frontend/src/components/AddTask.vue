<template>
  <!-- Trigger -->
  <div v-if="!isOpen" class="trigger" @click="open">
    <CirclePlus :size="20" class="trigger-icon" />
    <span>Add a task...</span>
  </div>

  <!-- Popup card 2-->
  <Transition name="pop">
    <div v-if="isOpen" class="card">

      <div class="card-header">
        <Sparkles :size="15" class="spark" />
        <span class="card-title">NEW TASK</span>
      </div>

      <input ref="nameRef" v-model="form.name" class="name-input"
        placeholder="What needs to be done?"
        @keyup.enter="submit" @keyup.esc="close" />

      <div class="sep" />

      <!-- Meta buttons row -->
      <div class="meta-row">

        <!-- Priority -->
        <div class="pill-wrap">
          <button class="meta-btn" :class="{ on: form.priority }" @click.stop="toggle('priority')">
            <Flag :size="13" :style="form.priority ? { color: priorityColor } : {}" />
            <span>{{ form.priority || 'Priority' }}</span>
          </button>
          <Transition name="drop">
            <div v-if="show === 'priority'" class="pop-list" @click.stop>
              <button v-for="p in PRIORITIES" :key="p.v" class="pop-item"
                :class="{ selected: form.priority === p.v }"
                @click="form.priority = p.v; show = null">
                <Flag :size="12" :style="{ color: p.color }" /> {{ p.label }}
              </button>
              <button v-if="form.priority" class="pop-item pop-clear"
                @click="form.priority = ''; show = null">Clear</button>
            </div>
          </Transition>
        </div>

        <!-- Due date -->
        <div class="pill-wrap">
          <button class="meta-btn" :class="{ on: form.dueDate }" @click.stop="toggle('date')">
            <CalendarDays :size="13" />
            <span>{{ form.dueDate ? fmtDate(form.dueDate) : 'Due date' }}</span>
          </button>
          <Transition name="drop">
            <div v-if="show === 'date'" class="pop-calendar" @click.stop>
              <div class="cal-nav-row">
                <button class="cal-nav" @click="prevMonth">‹</button>
                <span class="cal-title">{{ calTitle }}</span>
                <button class="cal-nav" @click="nextMonth">›</button>
              </div>
              <div class="cal-grid">
                <div v-for="d in DOW" :key="d" class="cal-dow">{{ d }}</div>
                <div v-for="(day, i) in calDays" :key="i" class="cal-day"
                  :class="{
                    empty: !day,
                    today: day && isToday(day),
                    selected: day && isSelected(day),
                    past: day && isPast(day),
                  }"
                  @click="day && !isPast(day) && selectDay(day)">
                  {{ day ? day.getDate() : '' }}
                </div>
              </div>
              <div class="cal-foot">
                <button v-if="form.dueDate" class="cal-clear" @click="form.dueDate=''; show=null">Clear</button>
                <button class="cal-today" @click="selectToday">Today</button>
              </div>
            </div>
          </Transition>
        </div>

        <!-- Time -->
        <div class="pill-wrap">
          <button class="meta-btn" :class="{ on: form.time }" @click.stop="toggle('time')">
            <Clock :size="13" />
            <span>{{ form.time || 'Time' }}</span>
          </button>
          <Transition name="drop">
            <div v-if="show === 'time'" class="pop-time" @click.stop>
              <div class="time-label">SET TIME</div>
              <input type="time" v-model="form.time" class="time-input" @change="show = null" />
              <button v-if="form.time" class="cal-clear" @click="form.time=''; show=null">Clear</button>
            </div>
          </Transition>
        </div>

        <!-- Project Type -->
        <div class="pill-wrap">
          <button class="meta-btn" :class="{ on: form.projectType }" @click.stop="toggle('projectType')">
            <Briefcase :size="13" />
            <span>{{ form.projectType || 'Project Type' }}</span>
          </button>
          <Transition name="drop">
            <div v-if="show === 'projectType'" class="pop-list" @click.stop>
              <button v-for="pt in PROJECT_TYPES" :key="pt" class="pop-item"
                :class="{ selected: form.projectType === pt }"
                @click="form.projectType = pt; form.projectId = null; form.projectName = ''; show = null">
                <span class="dot" :class="{ on: form.projectType === pt }" />
                {{ pt }}
                <Check v-if="form.projectType === pt" :size="11" class="ml-auto check-ico" />
              </button>
              <button v-if="form.projectType" class="pop-item pop-clear"
                @click="form.projectType = ''; form.projectId = null; form.projectName = ''; show = null">Clear</button>
            </div>
          </Transition>
        </div>

        <!-- Project Name -->
        <div class="pill-wrap">
          <button class="meta-btn" :class="{ on: form.projectId }" @click.stop="toggle('project')"
            :disabled="!form.projectType">
            <FolderOpen :size="13" />
            <span>{{ form.projectName || 'Project' }}</span>
          </button>
          <Transition name="drop">
            <div v-if="show === 'project'" class="pop-list" @click.stop>
              <button v-if="filteredProjects.length === 0" class="pop-item" disabled>
                No projects found
              </button>
              <button v-for="proj in filteredProjects" :key="proj.id" class="pop-item"
                :class="{ selected: form.projectId === proj.id }"
                @click="form.projectId = proj.id; form.projectName = proj.emoji + ' ' + proj.name; show = null">
                <span>{{ proj.emoji }} {{ proj.name }}</span>
                <Check v-if="form.projectId === proj.id" :size="11" class="ml-auto check-ico" />
              </button>
              <button v-if="form.projectId" class="pop-item pop-clear"
                @click="form.projectId = null; form.projectName = ''; show = null">Clear</button>
            </div>
          </Transition>
        </div>

      </div>

      <div class="sep" />

      <div class="actions">
        <button class="btn-cancel" @click="close">Cancel</button>
        <button class="btn-add" :disabled="!form.name.trim()" @click="submit">Add Task</button>
      </div>

    </div>
  </Transition>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, onUnmounted } from 'vue'
import { CirclePlus, Sparkles, Flag, CalendarDays, Clock, Briefcase, FolderOpen, Check } from 'lucide-vue-next'
import axios from 'axios'

const emit = defineEmits(['add'])

const isOpen  = ref(false)
const nameRef = ref(null)
const show    = ref(null)   // 'priority'|'date'|'time'|'projectType'|null
const form    = ref({ name: '', priority: '', dueDate: '', time: '', projectType: '', projectId: null, projectName: '' })

// Projects
const allProjects = ref([])
async function loadProjects() {
  const res = await axios.get('/api/projects')
  allProjects.value = res.data
}
const filteredProjects = computed(() =>
  allProjects.value.filter(p => p.type?.toLowerCase() === form.value.projectType?.toLowerCase())
)

const PRIORITIES = [
  { label: 'High',   v: 'High',   color: '#ef4444' },
  { label: 'Medium', v: 'Medium', color: '#f59e0b' },
  { label: 'Low',    v: 'Low',    color: '#6b7280' },
]
const PROJECT_TYPES = ['Personal', 'Corporate']
const DOW  = ['Su','Mo','Tu','We','Th','Fr','Sa']

// Close popover on outside click
function handleOutside(e) {
  if (!e.target.closest('.pill-wrap')) show.value = null
}
onMounted(() => document.addEventListener('mousedown', handleOutside))
onUnmounted(() => document.removeEventListener('mousedown', handleOutside))

// Calendar
const calView = ref(new Date())
const calTitle = computed(() =>
  calView.value.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
)
const calDays = computed(() => {
  const y = calView.value.getFullYear(), m = calView.value.getMonth()
  const first = new Date(y, m, 1).getDay()
  const last  = new Date(y, m+1, 0).getDate()
  const days = []
  for (let i = 0; i < first; i++) days.push(null)
  for (let d = 1; d <= last; d++) days.push(new Date(y, m, d))
  return days
})
const tod = new Date(); tod.setHours(0,0,0,0)
const isToday = d => d.toDateString() === tod.toDateString()
const isPast  = d => d < tod
const isSelected = d => form.value.dueDate &&
  d.toDateString() === new Date(form.value.dueDate + 'T00:00').toDateString()
const prevMonth = () => { const d = new Date(calView.value); d.setMonth(d.getMonth()-1); calView.value = d }
const nextMonth = () => { const d = new Date(calView.value); d.setMonth(d.getMonth()+1); calView.value = d }
function selectDay(d) {
  const pad = n => String(n).padStart(2,'0')
  form.value.dueDate = `${d.getFullYear()}-${pad(d.getMonth()+1)}-${pad(d.getDate())}`
  show.value = null
}
function selectToday() { selectDay(tod) }

const priorityColor = computed(() => PRIORITIES.find(p => p.v === form.value.priority)?.color || '')
const fmtDate = s => new Date(s+'T00:00').toLocaleDateString('en-GB', { weekday:'short', day:'numeric', month:'short' })
const toggle = p => { show.value = show.value === p ? null : p }

async function open() {
  isOpen.value = true
  loadProjects()
  await nextTick()
  nameRef.value?.focus()
}
function close() {
  isOpen.value = false
  form.value = { name:'', priority:'', dueDate:'', time:'', projectType:'', projectId: null, projectName: '' }
  show.value = null
}
function submit() {
  if (!form.value.name.trim()) return
  emit('add', {
    title:    form.value.name.trim(),
    due_date: form.value.dueDate || null,
    due_time: form.value.time    || null,
    project_type: form.value.projectType || null,
    project_id: form.value.projectId || null,
  })
  close()
}
</script>

<style scoped>
.trigger {
  display:flex; align-items:center; gap:10px;
  padding:13px 16px; border:1.5px dashed #d4cfc9; border-radius:12px;
  background:#fff; cursor:pointer; font-size:14px; color:#c0bdb8;
  transition:border-color .15s,color .15s; user-select:none; margin-top:8px;
}
.trigger:hover { border-color:#7c9ef8; color:#9ca8cc; }
.trigger-icon { color:#c8c4be; transition:color .15s; }
.trigger:hover .trigger-icon { color:#7c9ef8; }

.card {
  background:#fff; border:1px solid #eae7e1; border-radius:16px;
  padding:20px 20px 18px;
  box-shadow:0 2px 8px rgba(0,0,0,.05),0 12px 40px rgba(0,0,0,.09);
  margin-top:8px;
}

.card-header { display:flex; align-items:center; gap:7px; margin-bottom:14px; }
.spark { color:#7c9ef8; }
.card-title { font-size:11px; font-weight:700; letter-spacing:2px; color:#7c9ef8; }

.name-input {
  width:100%; border:none; outline:none; font-size:16px; color:#1a1a1e;
  font-family:inherit; background:transparent; padding-bottom:16px;
}
.name-input::placeholder { color:#cac7c0; }

.sep { height:1px; background:#f0ede8; margin-bottom:14px; }

.meta-row { display:flex; align-items:center; gap:2px; margin-bottom:14px; flex-wrap:wrap; }

/* pill wrapper keeps popover positioned */
.pill-wrap { position:relative; display:inline-block; }

.meta-btn {
  display:inline-flex; align-items:center; gap:5px;
  padding:6px 10px; border-radius:8px; border:none;
  background:none; font-size:12.5px; color:#7b8090;
  cursor:pointer; font-family:inherit;
  transition:background .12s,color .12s; white-space:nowrap;
}
.meta-btn:hover { background:#f4f2ee; color:#363a45; }
.meta-btn.on    { color:#4a6cf7; background:#eef1fd; }

/* popovers */
.pop-list, .pop-calendar, .pop-time {
  position:absolute; top:calc(100% + 6px); left:0;
  background:#fff; border:1px solid #eae7e1; border-radius:12px;
  box-shadow:0 8px 32px rgba(0,0,0,.12); z-index:200; overflow:hidden;
  min-width:155px;
}

.pop-item {
  display:flex; align-items:center; gap:8px; width:100%;
  padding:9px 14px; border:none; background:none;
  font-size:12.5px; color:#363a45; cursor:pointer;
  font-family:inherit; text-align:left; transition:background .1s;
}
.pop-item:hover { background:#f7f5f1; }
.pop-item.selected { color:#4a6cf7; background:#f0f3fd; }
.pop-clear { color:#aaa; font-size:11.5px; border-top:1px solid #f0ede8; }

.dot { width:7px; height:7px; border-radius:50%; background:#c8c4bd; flex-shrink:0; transition:background .12s; }
.dot.on { background:#4a6cf7; }
.ml-auto { margin-left:auto; }
.check-ico { color:#4a6cf7; }

/* Calendar */
.pop-calendar { padding:14px; min-width:264px; }
.cal-nav-row { display:flex; align-items:center; justify-content:space-between; margin-bottom:10px; }
.cal-nav { border:none; background:none; cursor:pointer; font-size:18px; color:#7b8090; padding:2px 8px; border-radius:6px; transition:background .1s; }
.cal-nav:hover { background:#f4f2ee; }
.cal-title { font-size:13px; font-weight:600; color:#363a45; }
.cal-grid { display:grid; grid-template-columns:repeat(7,1fr); gap:2px; }
.cal-dow { font-size:10px; color:#a0a4b0; text-align:center; padding:4px 0; font-weight:500; }
.cal-day { font-size:12px; text-align:center; padding:6px 2px; border-radius:6px; cursor:pointer; color:#363a45; transition:background .1s; }
.cal-day:not(.empty):not(.past):hover { background:#eef1fd; color:#4a6cf7; }
.cal-day.empty { cursor:default; }
.cal-day.past  { color:#cac7c0; cursor:default; }
.cal-day.today { font-weight:700; color:#4a6cf7; }
.cal-day.selected { background:#4a6cf7!important; color:#fff!important; font-weight:600; border-radius:6px; }
.cal-foot { display:flex; justify-content:flex-end; gap:8px; margin-top:10px; padding-top:10px; border-top:1px solid #f0ede8; }
.cal-clear { border:none; background:none; font-size:12px; color:#a0a4b0; cursor:pointer; font-family:inherit; padding:4px 8px; border-radius:6px; transition:background .1s; }
.cal-clear:hover { background:#f4f2ee; color:#363a45; }
.cal-today { border:none; background:#eef1fd; color:#4a6cf7; font-size:12px; font-weight:500; font-family:inherit; padding:5px 12px; border-radius:7px; cursor:pointer; transition:background .12s; }
.cal-today:hover { background:#dde4fb; }

/* Time */
.pop-time { padding:14px; min-width:180px; }
.time-label { font-size:10px; font-weight:700; letter-spacing:1.5px; color:#a0a4b0; margin-bottom:8px; }
.time-input { width:100%; border:1px solid #eae7e1; border-radius:8px; padding:8px 10px; font-size:14px; font-family:inherit; color:#363a45; outline:none; margin-bottom:8px; }
.time-input:focus { border-color:#7c9ef8; }

/* Actions */
.actions { display:flex; align-items:center; justify-content:flex-end; gap:10px; }
.btn-cancel { border:none; background:none; font-size:13px; color:#a0a4b0; cursor:pointer; font-family:inherit; padding:7px 10px; border-radius:8px; transition:color .12s,background .12s; }
.btn-cancel:hover { color:#363a45; background:#f4f2ee; }
.btn-add { border:none; background:#c8d5fb; color:#3a5cd6; font-size:13px; font-weight:500; font-family:inherit; padding:8px 20px; border-radius:10px; cursor:pointer; transition:background .15s,color .15s; }
.btn-add:not(:disabled):hover { background:#4a6cf7; color:#fff; }
.btn-add:disabled { opacity:.4; cursor:not-allowed; }

/* Transitions */
.pop-enter-active { transition:opacity .18s ease,transform .2s cubic-bezier(.34,1.4,.64,1); }
.pop-leave-active { transition:opacity .13s ease,transform .13s ease; }
.pop-enter-from   { opacity:0; transform:translateY(-6px) scale(.97); }
.pop-leave-to     { opacity:0; transform:translateY(-3px) scale(.99); }
.drop-enter-active { transition:opacity .14s ease,transform .15s cubic-bezier(.34,1.4,.64,1); }
.drop-leave-active { transition:opacity .1s ease; }
.drop-enter-from   { opacity:0; transform:translateY(-4px) scale(.97); }
.drop-leave-to     { opacity:0; }
</style>