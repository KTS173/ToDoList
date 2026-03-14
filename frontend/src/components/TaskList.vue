<template>
  <div class="task-list">
    <h2 class="title">{{ title }}</h2>
    <p class="subtitle">{{ subtitle }}</p>
    <span class="task-count">{{ tasks.length }} tasks</span>
    <div class="items">
    <TaskItem
      v-for="task in tasks"
      :key="task.id"
      :name="task.name"
      :tag="task.tag"
      :due_date="task.due_date"
      :due_time="task.due_time"
      :done="task.done"
      @toggle="emit('toggle', task)"
      @select="emit('select', task)"
      @delete="emit('delete', task)"
      @edit="emit('edit', task)" 
    />
    </div>
  </div>
</template>

<script setup>
import TaskItem from './TaskItem.vue'

defineProps({
  title: { type: String, default: 'Inbox' },
  subtitle: { type: String, default: 'All your pending tasks' },
  tasks: { type: Array, default: () => [] }
})

const emit = defineEmits(['toggle', 'select', 'delete', 'edit'])
</script>

<style scoped>
.task-list {
  margin-top: 24px;
}

.title {
  font-size: 24px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0;
}

.subtitle {
  font-size: 14px;
  color: #7f8c9b;
  margin: 4px 0 0 0;
}

.task-count {
  font-size: 13px;
  color: #b0b8c1;
  display: block;
  margin-top: 16px;
}

.items {
  margin-top: 8px;
}
</style>
