<template>
    <div class="kanban-board">
        <div class="column-wrapper" :class="{ dashed: todoTasks.length === 0 }">
            <KanbanColumn
                title="TO DO"
                color="#94a3b8"
                status="Not started"
                :tasks="todoTasks"
                :show-add-task="true"
                :members="members"
                empty-message=""
                @add="data => emit('add', data)"
                @drop="handleDrop"
                @edit="emit('edit', $event)"
            />
        </div>
        <div class="column-wrapper" :class="{ dashed: inProgressTasks.length === 0 }">
            <KanbanColumn
                title="IN PROGRESS"
                color="#3b82f6"
                status="In progress"
                :tasks="inProgressTasks"
                :members="members"
                empty-message="No tasks in progress"
                @drop="handleDrop"
                @edit="emit('edit', $event)"
            />
        </div>
        <div class="column-wrapper" :class="{ dashed: doneTasks.length === 0 }">
            <KanbanColumn
                title="DONE"
                color="#22c55e"
                status="Completed"
                :tasks="doneTasks"
                :members="members"
                empty-message="No completed tasks"
                @drop="handleDrop"
                @edit="emit('edit', $event)"
            />
        </div>
    </div>
</template>

<script setup>
import KanbanColumn from './KanbanColumn.vue'

const props = defineProps({
    todoTasks:       { type: Array, default: () => [] },
    inProgressTasks: { type: Array, default: () => [] },
    doneTasks:       { type: Array, default: () => [] },
    members:         { type: Array, default: () => [] }
})

const emit = defineEmits(['add', 'move', 'edit'])

function handleDrop({ taskId, newStatus }) {
    emit('move', { taskId, newStatus })
}
</script>

<style scoped>
/* ── Container ── */
.kanban-board { 
    display: flex; 
    gap: 20px; 
    overflow-x: auto; /* Allow horizontal scroll on mobile */
    padding-bottom: 12px; /* Space for scrollbar */
    /* Hide scrollbar for cleaner look if requested, but generally good on desktop */
}

/* ── Columns ── */
.column-wrapper {
    flex: 1;
    min-height: calc(100vh - 300px);
    min-width: 300px; /* Important: prevents columns from crushing on small screens */
    padding: 16px;
    box-sizing: border-box;
}

@media (max-width: 1024px) {
    .column-wrapper {
        min-width: 280px;
    }
}

.column-wrapper.dashed {
    border: 2px dashed #e2e8f0;
    border-radius: 12px;
}

/* Smooth scrolling for the kanban board container */
.kanban-board {
    scroll-snap-type: x mandatory;
    scroll-behavior: smooth;
    -webkit-overflow-scrolling: touch;
}

.column-wrapper {
    scroll-snap-align: start;
}
</style>