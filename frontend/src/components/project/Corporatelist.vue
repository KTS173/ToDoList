<template>
    <div class="kanban-list">

        <!-- COLUMN HEADERS -->
        <div class="list-header">
            <div></div>
            <div class="header-cell">TASK NAME</div>
            <div class="header-cell">ASSIGNEE</div>
            <div class="header-cell">STATUS</div>
            <div class="header-cell">DUE DATE</div>
            <div class="header-cell">PRIORITY</div>
        </div>

        <!-- ALL TASKS FLAT -->
        <div class="section-body">
            <div
                v-for="task in allTasks"
                :key="task.id"
                class="task-row"
                :class="{ done: task.is_completed }"
            >
                <!-- CHECKBOX -->
                <div class="check-col">
                    <span v-if="task.is_completed" class="check-done">✅</span>
                    <input v-else type="checkbox" class="task-checkbox" />
                </div>

                <!-- TASK INFO -->
                <div class="task-info">
                    <span class="task-name" :class="{ strikethrough: task.is_completed }">
                        {{ task.title || task.name }}
                    </span>
                    <span class="task-desc" :class="{ strikethrough: task.is_completed }">
                        {{ task.description || task.desc || '' }}
                    </span>
                </div>

                <!-- ASSIGNEE -->
                <div class="assignees">
                    <div
                        v-for="uid in (task.assignee_ids || [])"
                        :key="uid"
                        class="avatar-img"
                        :style="{ background: getAvatarColor(getMember(uid)?.name) }"
                        :title="getMember(uid)?.name || getMember(uid)?.email"
                    >
                        <img
                            v-if="getMember(uid)?.avatar_url"
                            :src="`${API}${getMember(uid).avatar_url}`"
                            class="avatar-photo"
                        />
                        <span v-else>{{ getInitials(getMember(uid)?.name || getMember(uid)?.email) }}</span>
                    </div>
                    <div v-if="!task.assignee_ids?.length" class="avatar-img gray">
                        <User :size="15" style="color: #94a3b8" />
                    </div>
                </div>

                <!-- STATUS -->
                <span class="status-badge" :class="statusClass(task.status)">
                    {{ statusLabel(task.status) }}
                </span>

                <!-- DUE DATE -->
                <span class="due-date" :class="{ overdue: isOverdue(task.due_date) && !task.is_completed }">
                    <Calendar :size="14" />
                    {{ formatDate(task.due_date) }}
                </span>

                <!-- PRIORITY -->
                <Flag :size="16" class="flag-icon" :class="task.priority || 'low'" />
            </div>

            <button class="add-task-btn">+ Add Task</button>
        </div>

    </div>
</template>

<script setup>
import { computed } from "vue"
import { Calendar, Flag, User } from "lucide-vue-next"
const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function getMember(uid) {
    return props.members.find(m => m.user_id === uid)
}

const props = defineProps({
    todoTasks:       { type: Array, default: () => [] },
    inProgressTasks: { type: Array, default: () => [] },
    doneTasks:       { type: Array, default: () => [] },
    members:         { type: Array, default: () => [] }
})

const allTasks = computed(() => [
    ...props.todoTasks,
    ...props.inProgressTasks,
    ...props.doneTasks
])

function getAssigneeName(task) {
    if (!task.assignee_ids?.length) return null
    const m = props.members.find(m => m.user_id === task.assignee_ids[0])
    return m?.name || m?.email || null
}

// ── Status helpers ──
function statusClass(status) {
    if (!status) return 'not-started'
    const s = status.toLowerCase()
    if (s === 'not started') return 'not-started'
    if (s === 'in progress') return 'in-progress'
    if (s === 'completed')   return 'done'
    if (s === 'review')      return 'review'
    return s.replace(' ', '-')
}

function statusLabel(status) {
    if (!status)                  return 'To Do'
    if (status === 'Not started') return 'To Do'
    if (status === 'In progress') return 'In Progress'
    if (status === 'Completed')   return 'Done'
    return status
}


// ── Date helpers ──
function formatDate(date) {
    if (!date) return '-'
    const d    = new Date(date)
    const now  = new Date()
    const diff = Math.floor((d - now) / 86400000)
    if (diff === 0)  return 'Today'
    if (diff === -1) return 'Yesterday'
    if (diff === 1)  return 'Tomorrow'
    return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

function isOverdue(date) {
    if (!date) return false
    return new Date(date) < new Date(new Date().toDateString())
}

// ── Avatar helpers ──
const avatarColors = ['#3b82f6', '#a855f7', '#f97316', '#10b981', '#ef4444', '#ec4899', '#14b8a6']

function getAvatarColor(name) {
    if (!name) return '#e2e8f0'
    let hash = 0
    for (let i = 0; i < name.length; i++) hash += name.charCodeAt(i)
    return avatarColors[hash % avatarColors.length]
}

function getInitials(name) {
    if (!name) return ''
    return name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase()
}
</script>

<style scoped>
.kanban-list {
    background: #fff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    width: 100%;
    box-sizing: border-box;
}

/* COLUMN HEADERS */
.list-header {
    display: grid;
    grid-template-columns: 40px 2fr 1.2fr 130px 160px 60px;
    gap: 16px;
    padding: 14px 20px;
    border-bottom: 1px solid #e2e8f0;
    background: #f8fafc;
    border-radius: 12px 12px 0 0;
}

.header-cell {
    font-size: 11px;
    font-weight: 700;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* TASK ROW */
.task-row {
    display: grid;
    grid-template-columns: 40px 2fr 1.2fr 130px 160px 60px;
    align-items: center;
    gap: 16px;
    padding: 16px 20px;
    border-bottom: 1px solid #f1f5f9;
    background: #fff;
}

.task-row:last-of-type { border-bottom: none; }
.task-row:hover { background: #f8fafc; }
.task-row.done  { background: #fafafa; }

/* CHECKBOX */
.check-col {
    display: flex;
    align-items: center;
    justify-content: center;
}

.task-checkbox {
    width: 16px;
    height: 16px;
    cursor: pointer;
    accent-color: #3b82f6;
    border-radius: 50%;
}

.check-done { font-size: 18px; }

/* TASK INFO */
.task-info {
    display: flex;
    flex-direction: column;
    min-width: 0;
}

.task-name {
    font-size: 14px;
    font-weight: 600;
    color: #1e293b;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.task-desc {
    font-size: 12px;
    color: #94a3b8;
    margin-top: 3px;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.strikethrough {
    text-decoration: line-through;
    color: #94a3b8 !important;
}

/* ASSIGNEE */
.assignee {
    display: flex;
    align-items: center;
    gap: 10px;
    min-width: 0;
}

.avatar-img {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: #e2e8f0;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 12px;
    font-weight: 700;
    flex-shrink: 0;
}

.assignee-info { display: flex; flex-direction: column; min-width: 0; }
.assignee-name { font-size: 13px; font-weight: 600; color: #1e293b; }
.assignee-role { font-size: 11px; color: #94a3b8; }

/* STATUS BADGE */
.status-badge {
    display: inline-block;
    font-size: 12px;
    padding: 5px 14px;
    border-radius: 20px;
    font-weight: 500;
    white-space: nowrap;
    width: fit-content;
}

.status-badge.not-started { background: #f1f5f9; color: #64748b; }
.status-badge.in-progress  { background: #dbeafe; color: #3b82f6; }
.status-badge.done         { background: #dcfce7; color: #16a34a; }
.status-badge.review       { background: #fef3c7; color: #d97706; }

/* DUE DATE */
.due-date {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    color: #64748b;
    white-space: nowrap;
}

.due-date.overdue { color: #ef4444; }

/* PRIORITY FLAG */
.flag-icon          { justify-self: center; }
.flag-icon.high     { color: #ef4444; }
.flag-icon.medium   { color: #f59e0b; }
.flag-icon.low      { color: #cbd5e1; }

/* ADD TASK */
.add-task-btn {
    width: 100%;
    padding: 14px 20px;
    border: none;
    background: #fff;
    color: #94a3b8;
    font-size: 13px;
    cursor: pointer;
    text-align: left;
    border-radius: 0 0 12px 12px;
}

.add-task-btn:hover { color: #64748b; background: #f8fafc; }
.assignees { display: flex; align-items: center; gap: -4px; }
.avatar-photo { width: 100%; height: 100%; object-fit: cover; border-radius: 50%; }
.avatar-img.gray { background: #e2e8f0; }
</style>