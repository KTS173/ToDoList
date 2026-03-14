<template>
  <div class="task-item" @click="emit('select')">
    <component
      :is="done ? CheckCircle : Circle"
      :size="20"
      class="checkbox"
      @click.stop="emit('toggle')"
    />

    <div class="task-content">
      <span class="task-name">{{ name }}</span>
      <div class="task-meta">
        <span v-if="tag" class="tag"># {{ tag }}</span>
        <span v-if="due_date || due_time" class="due-chip">
          {{ fmtDateTime(due_date, due_time) }}
        </span>
      </div>
    </div>

    <div class="btn-group">
      <button class="delete-btn" @click.stop="emit('edit')">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
          fill="currentColor" viewBox="0 0 24 24">
          <path d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04a1 1 0 0 0 0-1.41l-2.34-2.34a1 1 0 0 0-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z"/>
        </svg>
      </button>
      <button class="delete-btn" @click.stop="emit('delete')">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
          fill="currentColor" viewBox="0 0 24 24">
          <path d="M17 6V4c0-1.1-.9-2-2-2H9c-1.1 0-2 .9-2 2v2H2v2h2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8h2V6zM9 4h6v2H9zM6 20V8h12v12z"/>
        </svg>
      </button>
    </div>

  </div>
</template>

<script setup>
import { Circle, CheckCircle } from 'lucide-vue-next'

defineProps({
  name:     { type: String,  required: true },
  tag:      { type: String,  default: '' },
  done:     { type: Boolean, default: false },
  due_date: { type: String,  default: '' },
  due_time: { type: String,  default: '' },
})

const emit = defineEmits(['toggle', 'select', 'delete', 'edit'])

function fmtDateTime(date, time) {
  let result = ''
  if (date) {
    result = new Date(date + 'T00:00').toLocaleDateString('en-US', {
      month: 'long', day: 'numeric', year: 'numeric'
    })
  }
  if (time) {
    const [h, m] = time.split(':')
    const d = new Date()
    d.setHours(+h, +m)
    result += ', ' + d.toLocaleTimeString('en-US', {
      hour: 'numeric', minute: '2-digit', hour12: false
    })
  }
  return result
}
</script>

<style scoped>
/* ── Container ── */
.task-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 16px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  margin-bottom: 10px;
  background: #fff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  cursor: pointer;
  transition: box-shadow 0.2s;
  width: 100%;
  box-sizing: border-box;
}

.task-item:hover { box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12); }

@media (max-width: 480px) {
  .task-item {
    padding: 12px 14px; /* Slightly tighter padding on mobile */
    gap: 8px;
  }
}

/* ── Checkbox ── */
.checkbox { 
    cursor: pointer; 
    color: #c0c6ce; 
    flex-shrink: 0; 
}

/* ── Content & Text ── */
.task-content { 
    display: flex; 
    flex-direction: column; 
    gap: 4px; 
    flex: 1; 
    min-width: 0; /* Prevent text from pushing container */
}

.task-name { 
    font-size: 15px; 
    color: #2c3e50; 
    /* Truncate long names */
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* ── Metadata & Tags ── */
.task-meta { 
    display: flex; 
    gap: 6px; 
    flex-wrap: wrap; 
    margin-top: 2px; 
}

.tag {
  font-size: 12px; color: #27ae60;
  background: #e8f8ef; padding: 2px 8px;
  border-radius: 4px;
}

.due-chip {
  font-size: 11px; color: #7b8090;
  background: #f4f2ee; padding: 2px 8px;
  border-radius: 4px;
}

/* ── Action Buttons ── */
.btn-group { 
    display: flex; 
    align-items: center; 
    gap: 4px; 
    margin-left: auto; 
    flex-shrink: 0; /* Don't squash buttons */
}

.delete-btn {
  background: transparent; border: none;
  cursor: pointer; opacity: 0.6;
  transition: opacity 0.2s; padding: 4px;
}
.delete-btn:hover { opacity: 1; }
</style>