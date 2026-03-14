<script setup>
import { ref } from 'vue'
import Sidebar from './components/sidebar.vue'
import { useRoute, useRouter } from 'vue-router'
import { Menu } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const searchQuery = ref('')
const isMobileOpen = ref(false)

function signOut() {
    localStorage.removeItem('token')
    localStorage.removeItem('email')
    localStorage.removeItem('name')
    router.push('/login')
}

function toggleMobileSidebar() {
    isMobileOpen.value = !isMobileOpen.value
}

function closeMobileSidebar() {
    isMobileOpen.value = false
}
</script>

<template>
  <div v-if="route.path === '/login' || route.path === '/signup'">
    <router-view />
  </div>

  <div v-else class="layout">
    <div class="mobile-header">
      <button class="mobile-menu-btn" @click="toggleMobileSidebar">
        <Menu :size="24" />
      </button>
      <span class="mobile-title">CMU TO DO LIST</span>
    </div>
    <div v-if="isMobileOpen" class="mobile-overlay" @click="closeMobileSidebar"></div>
    <Sidebar :is-mobile-open="isMobileOpen" @close-mobile="closeMobileSidebar" @search="searchQuery = $event" @sign-out="signOut" />
    <div class="content">
      <router-view :search="searchQuery"/>
    </div>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  margin: 0;
}

.layout {
  display: flex;
  min-height: 100vh;
  position: relative;
}

.content {
  flex: 1;
  overflow-y:auto;
  min-width: 0; /* Important for flex children to allow shrinking below min-content */
}

.mobile-header {
  display: none;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: #f0ede8;
  border-bottom: 1px solid #e0ddd8;
  position: sticky;
  top: 0;
  z-index: 50;
  width: 100%;
}

.mobile-menu-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #1a1a1a;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mobile-title {
  font-size: 18px;
  font-weight: 700;
  color: #1a1a1a;
  font-family: 'DM Sans', 'Segoe UI', sans-serif;
}

.mobile-overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  z-index: 90;
}

@media (max-width: 768px) {
  .layout {
    flex-direction: column;
  }
  .mobile-header {
    display: flex;
  }
  .content {
    /* Height will be calculated by content */
  }
  .mobile-overlay {
    display: block;
  }
}

</style>