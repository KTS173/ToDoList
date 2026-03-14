<template>
  <div class="filter-bar">
    <div class="filter-left">
      <span class="filter-lable">Filters:</span>

      <select class="filter-select">
        <option value="">Priority</option>
        <option value="high">High</option>
        <option value="medium">Medium</option>
        <option value="low">Low</option>
      </select>

      <select class="filter-select">
        <option value="">Tags</option>
        <option value="ux">#ux</option>
        <option value="design">#design</option>
        <option value="dev">#dev</option>
      </select>

      <select class="filter-select">
        <option value="">Due Date</option>
        <option value="today">Today</option>
        <option value="week">This Week</option>
        <option value="month">This Month</option>
      </select>
      <span class="clear-all">Clear all</span>

    </div>

    <div class="filter-right">
      <button class="view-btn" :class="{ active: currentView === 'board' }" @click="setView('board')">Board</button>
      <button class="view-btn" :class="{ active: currentView === 'list' }" @click="setView('list')">List</button>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'

const currentView = ref('board')
const emit = defineEmits(['view-change'])

function setView(view) {
  currentView.value = view
  emit('view-change', view)
}
</script>

<style scoped>
.filter-lable {
  padding: 6px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background-color: #fff;
  color: #334155;
  font-size: 20px;
}

.filter-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  margin-top: 24px;
}

.filter-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.filter-select {
  padding: 6px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  background-color: #fff;
  color: #334155;
  font-size: 15px;
  cursor: pointer;
}

.filter-select:hover {
  background-color: #f1f5f9;
}

.clear-all {
  color: #94a3b8;
  font-size: 13px;
  cursor: pointer;
}

.clear-all:hover {
  color: #334155;
}

.filter-right {
  display: flex;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
}

.view-btn {
  padding: 6px 14px;
  border: none;
  background-color: #fff;
  color: #334155;
  font-size: 13px;
  cursor: pointer;
}

.view-btn:hover {
  background-color: #f1f5f9;
}

.view-btn.active {
  background-color: #1e293b;
  color: #fff;
}
</style>
