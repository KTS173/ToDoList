<template>
    <div
        class="kanban-column"
        @dragover.prevent
        @drop="onDrop"
        :class="{ 'drag-over': isDragOver }"
        @dragenter="isDragOver = true"
        @dragleave="isDragOver = false"
    >
        <div class="column-header">
            <Circle :size="10" :fill="color" :color="color" />
            <span class="column-title">{{ title }}</span>
            <span class="count">{{ tasks.length }}</span>
        </div>

    <TaskCard
        v-for="task in tasks"
        :key="task.id"
        :name="task.title"
        :description="task.description"
        :priority="task.priority"
        :due-date="task.due_date"
        :done="task.done"
        :assignees="getAssignees(task)"
        draggable="true"
        @edit="emit('edit', task)"
        @dragstart="onDragStart(task)"
        @dragend="isDragOver = false"
    />

        <div v-if="tasks.length === 0" class="empty-state">
            <span>{{ emptyMessage }}</span>
        </div>

        <AddTask v-if="showAddTask" @add="data => emit('add', data)" />
    </div>
</template>

<script setup>
import { ref } from 'vue'
import TaskCard from './TaskCard.vue'
import AddTask from '@/components/AddTask.vue'
import { Circle } from 'lucide-vue-next'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const props = defineProps({
    title:        { type: String,  default: 'TO DO' },
    color:        { type: String,  default: '#f59e0b' },
    tasks:        { type: Array,   default: () => [] },
    emptyMessage: { type: String,  default: 'No tasks' },
    showAddTask:  { type: Boolean, default: false },
    status:       { type: String,  default: 'Not started' },
    members:      { type: Array,   default: () => [] }
})

const emit = defineEmits(['add', 'drop', 'edit'])
const isDragOver = ref(false)

function getAssignees(task) {
    let assigneeIds = task.assignee_ids
    
    // ถ้าไม่มี assignee_ids ให้ใช้ user_id แทน
    if (!assigneeIds?.length && task.user_id) {
        assigneeIds = [task.user_id]
    }
    
    if (!assigneeIds?.length) return []
    
    return assigneeIds.map(uid => {
        const m = props.members.find(m => m.user_id === uid)
        return {
            name:   m?.name || m?.email || '',
            avatar: m?.avatar_url ? `${API}${m.avatar_url}` : ''
        }
    }).filter(a => a.name)
}

function onDragStart(task) {
    window.__draggedTaskId = task.id
}

function onDrop() {
    isDragOver.value = false
    const taskId = window.__draggedTaskId
    if (taskId !== undefined) {
        emit('drop', { taskId, newStatus: props.status })
        window.__draggedTaskId = undefined
    }
}
</script>

<style scoped>
.kanban-column { flex: 1; min-width: 0; border-radius: 12px; padding: 4px; transition: background 0.15s; }
.kanban-column.drag-over { background: #f0f7ff; outline: 2px dashed #3b82f6; }
.column-header { display: flex; align-items: center; gap: 8px; margin-bottom: 16px; }
.column-title { font-size: 13px; font-weight: 700; text-transform: uppercase; }
.count { background: #f1f5f9; color: #64748b; font-size: 12px; padding: 2px 8px; border-radius: 10px; }
.empty-state { display: flex; align-items: center; justify-content: center; padding: 40px 16px; color: #94a3b8; font-size: 13px; }
</style>