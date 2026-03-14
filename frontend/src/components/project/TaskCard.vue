<template>
    <div class="taskcard" @click="emit('edit')">
        <div class="head-card">
            <span v-if="done" class="priority completed">COMPLETED</span>
            <span v-else class="priority" :class="priority">{{ priority }}</span>
            <span v-if="done" class="check-icon">✅</span>
        </div>
        <div class="body-card">
            <h1 class="title" :class="{ strikethrough: done }">{{ name }}</h1>
            <p class="desciption">{{ description }}</p>
        </div>
        <div class="tail-card">
            <span class="due-date">
                <Calendar :size="13" />
                {{ formattedDate }}
            </span>
            <div class="avatars">
                <div
                    v-for="(a, i) in assignees"
                    :key="i"
                    class="avatar"
                    :title="a.name"
                    :style="{ marginLeft: i === 0 ? '0' : '-8px', zIndex: assignees.length - i }"
                >
                    <img v-if="a.avatar" :src="a.avatar" class="avatar-img" />
                    <span v-else>{{ getInitials(a.name) }}</span>
                </div>
                <div v-if="assignees.length === 0" class="avatar gray">
                    <User :size="14" />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue'
import { Calendar, User } from 'lucide-vue-next'

const props = defineProps({
    name:        { type: String,  default: '' },
    description: { type: String,  default: '' },
    dueDate:     { type: String,  default: '' },
    priority:    { type: String,  default: 'low' },
    done:        { type: Boolean, default: false },
    assignees:   { type: Array,   default: () => [] } 
})

const emit = defineEmits(['edit'])

const formattedDate = computed(() => {
  if (!props.dueDate) return ''
  const date     = new Date(props.dueDate)
  const today    = new Date()
  const tomorrow = new Date(today)
  tomorrow.setDate(today.getDate() + 1)
  if (date.toDateString() === today.toDateString())    return 'Today'
  if (date.toDateString() === tomorrow.toDateString()) return 'Tomorrow'
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
})

function getInitials(name) {
  if (!name) return '?'
  return name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase()
}
</script>

<style scoped>
.taskcard {
    background: #fff; border: 1px solid #e2e8f0; border-radius: 12px;
    padding: 16px; margin-bottom: 12px; box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    display: flex; flex-direction: column; gap: 10px; cursor: pointer;
}
.head-card { display: flex; justify-content: space-between; align-items: center; margin: 5px 0; }
.priority { border-radius: 6px; padding: 3px 10px; text-transform: uppercase; font-weight: 700; font-size: 11px; border: none; }
.priority.high      { background: #fee2e2; color: #dc2626; }
.priority.medium    { background: #fef3c7; color: #d97706; }
.priority.low       { background: #dcfce7; color: #16a34a; }
.priority.review    { background: #fef3c7; color: #d97706; }
.priority.completed { background: #f1f5f9; color: #64748b; }
.check-icon { font-size: 16px; }
.title { font-size: 15px; font-weight: 600; color: #1e293b; margin: 0; }
.strikethrough { text-decoration: line-through; color: #94a3b8; }
.desciption { font-size: 13px; color: #64748b; line-height: 1.4; margin: 0; }
.tail-card { display: flex; justify-content: space-between; align-items: center; }
.due-date { display: flex; align-items: center; gap: 4px; font-size: 12px; color: #94a3b8; }
.avatars { display: flex; align-items: center; }
.avatar {
    width: 28px; height: 28px; border-radius: 50%;
    background: #a78bfa; border: 2px solid #fff;
    color: #fff; display: flex; align-items: center; justify-content: center;
    font-size: 10px; font-weight: 700; overflow: hidden; flex-shrink: 0;
}
.avatar.gray { background: #e2e8f0; color: #94a3b8; }
.avatar-img { width: 100%; height: 100%; object-fit: cover; border-radius: 50%; }
</style>