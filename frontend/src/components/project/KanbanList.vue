<template>
    <div class="kanban-list">

        <div v-for="(section, index) in sections" :key="section.title" class="list-section">

            <!-- SECTION HEADER -->
            <div class="section-header" @click="toggleSection(index)">
                <ChevronDown v-if="!collapsed[index]" :size="16" />
                <ChevronRight v-else :size="16" />

                <Circle :size="10" :fill="section.color" :color="section.color" />

                <span class="section-title">{{ section.title }}</span>

                <span class="count">{{ section.tasks.length }}</span>

                <button class="add-btn" @click.stop>
                    <Plus :size="16" />
                </button>
            </div>

            <!-- SECTION BODY -->
            <div v-show="!collapsed[index]" class="section-body">

                <div v-for="task in section.tasks" :key="task.id" class="task-row">

                    <!-- CHECKBOX -->
                    <input type="checkbox" class="task-checkbox" />

                    <!-- TASK INFO -->
                    <div class="task-info">
                        <span class="task-name">{{ task.title || task.name }}</span>
                        <span class="task-desc">{{ task.description || task.desc }}</span>
                    </div>

                    <!-- ASSIGNEE -->
                    <div class="assignee">
                        <div class="avatar-img">
                            <img 
                                v-if="me?.avatar_url"
                                :src="`${API}${me.avatar_url}`"
                                style="width:100%;height:100%;object-fit:cover;border-radius:50%;"
                            />
                            <User v-else :size="16" />
                        </div>
                        <div class="assignee-info">
                            <span class="assignee-name">{{ me?.name || 'Me' }}</span>
                        </div>
                    </div>

                    <!-- STATUS -->
                    <span class="status-badge" :class="task.status?.toLowerCase().replace(' ', '-')">
                        {{ task.status || "To Do" }}
                    </span>

                    <!-- DUE DATE -->
                    <span class="due-date">
                        <Calendar :size="14" />
                        {{ task.due_date || task.dueDate || "-" }}
                    </span>

                    <!-- PRIORITY -->
                    <Flag :size="16" class="flag-icon" :class="task.priority" />
                </div>

                <!-- ADD TASK -->
                <button class="add-task-btn">
                    + Add Task
                </button>

            </div>

        </div>

    </div>
</template>

<script setup>
import { ref, computed } from "vue"

import {ChevronDown,ChevronRight,Circle,Plus,Calendar,Flag,User} from "lucide-vue-next"

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const props = defineProps({
    todoTasks: { type: Array, default: () => [] },
    inProgressTasks: { type: Array, default: () => [] },
    me:              { type: Object, default: null },
    doneTasks: { type: Array, default: () => [] }
    
})

const collapsed = ref({
    0: false,
    1: false,
    2: false
})

const sections = computed(() => [
    {
        title: "TO DO",
        color: "#f59e0b",
        tasks: props.todoTasks
    },
    {
        title: "IN PROGRESS",
        color: "#3b82f6",
        tasks: props.inProgressTasks
    },
    {
        title: "DONE",
        color: "#22c55e",
        tasks: props.doneTasks
    }
])

function toggleSection(index) {
    collapsed.value[index] = !collapsed.value[index]
}
</script>

<style scoped>
.kanban-list {

    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    width: 100%;
    box-sizing: border-box;
    overflow-x: hidden;
}

.section-header {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 16px;
    cursor: pointer;
    user-select: none;
}

.section-title {
    font-size: 13px;
    font-weight: 700;
    text-transform: uppercase;
}

.count {
    background: #f1f5f9;
    color: #64748b;
    font-size: 12px;
    padding: 2px 8px;
    border-radius: 10px;
}

.add-btn {
    margin-left: auto;
    border: none;
    background: none;
    color: #94a3b8;
    cursor: pointer;
}

.section-body {
    border-top: 1px solid #e2e8f0;
}

/* TASK ROW */

.task-row {
  display: grid;
  grid-template-columns: 24px 300px 300px 110px 300px 50px;
  align-items: center;
  gap: 24px;
  padding: 12px 16px;
  border-bottom: 1px solid #f1f5f9;
  background: #fff;
}

.task-row:hover {
    background: #f1f5f9;
}

/* CHECKBOX */

.task-checkbox {
    width: 16px;
    height: 16px;
    cursor: pointer;
}

/* TASK INFO */

.task-info {
    display: flex;
    flex-direction: column;
    min-width: 0;
}

.task-name {
    font-size: 14px;
    font-weight: 500;
    color: #1e293b;

    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.task-desc {
    font-size: 12px;
    color: #94a3b8;
    margin-top: 2px;

    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* ASSIGNEE */

.assignee {
    display: flex;
    align-items: center;
    gap: 8px;
    min-width: 0;
}

.avatar-img {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: #e2e8f0;

    display: flex;
    align-items: center;
    justify-content: center;

    color: #64748b;
    flex-shrink: 0;
}

.assignee-info {
    display: flex;
    flex-direction: column;
    min-width: 0;
}

.assignee-name {
    font-size: 13px;
    font-weight: 500;
    color: #1e293b;
}

.assignee-role {
    font-size: 11px;
    color: #94a3b8;
}

/* STATUS BADGE */

.status-badge {
    text-align: center;
    font-size: 12px;
    padding: 4px 12px;
    border-radius: 20px;
    font-weight: 500;
    white-space: nowrap;
}

.status-badge.to-do {
    background: #f1f5f9;
    color: #64748b;
}

.status-badge.in-progress {
    background: #dbeafe;
    color: #3b82f6;
}

.status-badge.done {
    background: #dcfce7;
    color: #16a34a;
}

/* DUE DATE */

.due-date {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #64748b;
  margin-left: 120px;
  
}

/* PRIORITY */

.flag-icon {
  justify-self: end;  
}
.flag-icon.high {
    color: #ef4444;
}

.flag-icon.medium {
    color: #f59e0b;
}

.flag-icon.low {
    color: #94a3b8;
}

/* ADD TASK */

.add-task-btn {
    width: 100%;
    padding: 12px 16px;
    border: none;
    background: #fff;
    color: #94a3b8;
    font-size: 13px;
    cursor: pointer;
    text-align: left;
}

.add-task-btn:hover {
    color: #64748b;
    background: #f1f5f9;
}

.avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
}
</style>