<template>
  <div class="card-container">
    <BaseCard msg="Completed" :total="stats.completed" icon="✅" iconBg="#e8f5e9" />
    <BaseCard msg="Due Today" :total="stats.dueToday"  icon="📅" iconBg="#e3f2fd" />
    <BaseCard msg="Overdue"   :total="stats.overdue"   icon="⏰" iconBg="#fce4ec" />
    <BaseCard msg="Total"     :total="stats.total"     icon="🏁" iconBg="#f3e5f5" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import BaseCard from './Basecard.vue'

const props = defineProps({
  tasks: { type: Array, required: true }
})


const stats = computed(() => {
  const now = new Date()
  const today = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`
  console.log('tasks in TaskStats:', props.tasks)
  return {
    completed: props.tasks.filter(t =>  t.done).length,
    dueToday:  props.tasks.filter(t => !t.done && t.due_date === today).length,
    overdue:   props.tasks.filter(t => !t.done && t.due_date && t.due_date < today).length,
    total:     props.tasks.length
  }
})


</script>

<style scoped>
.card-container {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 8px;
}
</style>