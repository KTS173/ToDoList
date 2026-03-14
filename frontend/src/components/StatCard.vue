<template>
  <div class="stat-card">
    <div class="stat-header">
      <p class="stat-label">{{ label }}</p>
      <div class="stat-icon">
        <component :is="icon" :size="18" />
      </div>
    </div>
    <div class="stat-body">
      <span class="stat-value">{{ percent }}%</span>
      <span class="stat-sub">{{ completed }}/{{ total }} tasks</span>
    </div>
    <div class="progress-bar">
      <div class="progress-fill" :style="{ width: percent + '%' }"></div>
    </div>
  </div>
</template>

<script setup>
import { BarChart3 } from 'lucide-vue-next'

defineProps({
  label:     { type: String, default: 'Completion' },
  percent:   { type: Number, default: 0 },
  completed: { type: Number, default: 0 },
  total:     { type: Number, default: 0 },
  icon:      { type: [Object, Function], default: () => BarChart3 }
})
</script>

<style scoped>
.stat-card {
  flex: 1;
  min-width: 120px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 24px 20px;
}

.stat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.stat-label { font-size: 13px; color: #888; font-weight: 600; margin: 0; }

.stat-icon {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  background: #e0e7ff;
  color: #3b82f6;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-body {
  margin-bottom: 12px;
}

.stat-value { font-size: 32px; font-weight: 700; color: #2c3e50; display: block; }
.stat-sub { font-size: 12px; color: #aaa; }

.progress-bar {
  height: 6px;
  background: #e8e5e0;
  border-radius: 3px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: #3b82f6;
  border-radius: 3px;
  transition: width 0.3s ease;
}
</style>
