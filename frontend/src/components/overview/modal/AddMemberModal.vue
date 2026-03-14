<template>
  <Teleport to="body">
    <div v-if="modelValue" class="modal-overlay" @click.self="$emit('update:modelValue', false)">
      <div class="add-member-modal">
        <h2>Manage Members</h2>

        <div class="invite-row">
          <div class="input-wrapper">
            <input
              v-model="newEmail"
              type="email"
              class="form-input"
              placeholder="Enter email address"
              @input="searchUsers"
              @keyup.enter="addMember"
              @keyup.esc="suggestions = []"
            />
            <div v-if="suggestions.length" class="suggestions">
              <div
                v-for="user in suggestions"
                :key="user.id"
                class="suggestion-item"
                @click="selectUser(user)"
              >
                <div class="suggestion-avatar">{{ getInitials(user.name || user.email) }}</div>
                <div>
                  <p class="suggestion-name">{{ user.name || '-' }}</p>
                  <p class="suggestion-email">{{ user.email }}</p>
                </div>
              </div>
            </div>
          </div>
          <select v-model="newRole" class="role-select">
            <option value="Member">Member</option>
            <option value="Admin">Admin</option>
          </select>
          <button class="btn-add" @click="addMember" :disabled="loading">
            {{ loading ? '...' : 'Add' }}
          </button>
        </div>

        <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>

        <div v-if="members.length" class="member-list">
          <div v-for="member in members" :key="member.user_id" class="member-item">
            <div class="member-avatar">{{ getInitials(member.name || member.email) }}</div>
            <div class="member-info">
              <p class="member-name">{{ member.name || '-' }}</p>
              <p class="member-email">{{ member.email }}</p>
            </div>
            <span class="member-role-badge">{{ member.role }}</span>
            <button class="btn-remove" @click="removeMember(member.user_id)">
              <X :size="16" />
            </button>
          </div>
        </div>
        <p v-else class="no-members">No members yet.</p>

        <button class="btn-close" @click="$emit('update:modelValue', false)">Close</button>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'
import { X } from 'lucide-vue-next'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  projectId:  { type: [Number, String], default: null },
  members:    { type: Array, default: () => [] }
})

const emit = defineEmits(['update:modelValue', 'members-changed'])

const newEmail    = ref('')
const newRole     = ref('Member')
const loading     = ref(false)
const errorMsg    = ref('')
const suggestions = ref([])

function getHeaders() {
  const token = localStorage.getItem('token')
  return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
}

function getInitials(name) {
  if (!name) return '?'
  return name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase()
}

async function searchUsers() {
  const q = newEmail.value.trim()
  if (q.length < 2) { suggestions.value = []; return }
  const res = await fetch(`${API}/api/users/search?q=${encodeURIComponent(q)}`, { headers: getHeaders() })
  suggestions.value = await res.json()
}

function selectUser(user) {
  newEmail.value    = user.email
  suggestions.value = []
}

async function addMember() {
  const email = newEmail.value.trim()
  if (!email) return
  errorMsg.value = ''
  loading.value  = true

  try {
    const res = await fetch(`${API}/api/projects/${props.projectId}/members`, {
      method:  'POST',
      headers: getHeaders(),
      body:    JSON.stringify({ email, role: newRole.value })
    })

    if (!res.ok) {
      const err = await res.json()
      errorMsg.value = err.detail || 'Failed to add member'
      return
    }

    newEmail.value    = ''
    newRole.value     = 'Member'
    suggestions.value = []
    emit('members-changed')
  } catch (err) {
    errorMsg.value = 'Failed to add member'
  } finally {
    loading.value = false
  }
}

async function removeMember(userId) {
  try {
    const res = await fetch(`${API}/api/projects/${props.projectId}/members/${userId}`, {
      method:  'DELETE',
      headers: getHeaders()
    })
    if (!res.ok) { errorMsg.value = 'Failed to remove member'; return }
    emit('members-changed')
  } catch (err) {
    errorMsg.value = 'Failed to remove member'
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.add-member-modal {
  background: #fff;
  border-radius: 20px;
  padding: 32px;
  width: 500px;
  max-width: 90vw;
}

.add-member-modal h2 {
  margin: 0 0 20px;
  font-size: 20px;
  font-weight: 700;
}

.invite-row {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.input-wrapper {
  flex: 1;
  position: relative;
}

.form-input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  outline: none;
  box-sizing: border-box;
}

.form-input:focus { border-color: #3b82f6; }

.suggestions {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  z-index: 100;
  overflow: hidden;
}

.suggestion-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  cursor: pointer;
}

.suggestion-item:hover { background: #f5f5f5; }

.suggestion-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #3b82f6;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 700;
  flex-shrink: 0;
}

.suggestion-name { font-size: 13px; font-weight: 600; color: #1a1a2e; margin: 0; }
.suggestion-email { font-size: 11px; color: #999; margin: 0; }

.role-select {
  padding: 10px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  font-size: 13px;
  background: #fff;
  cursor: pointer;
}

.btn-add {
  padding: 10px 20px;
  border: none;
  border-radius: 10px;
  background: #3b82f6;
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
}

.btn-add:hover { background: #2563eb; }
.btn-add:disabled { opacity: 0.6; cursor: not-allowed; }

.error-msg { color: #ef4444; font-size: 13px; margin: -8px 0 12px; }

.member-list {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 16px;
}

.member-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
}

.member-item + .member-item { border-top: 1px solid #f0f0f0; }

.member-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #3b82f6;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  flex-shrink: 0;
}

.member-info { flex: 1; }
.member-name { font-size: 13px; font-weight: 600; color: #1a1a2e; margin: 0; }
.member-email { font-size: 11px; color: #999; margin: 0; }

.member-role-badge {
  padding: 4px 10px;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 12px;
  color: #333;
}

.btn-remove { background: none; border: none; color: #bbb; cursor: pointer; padding: 4px; }
.btn-remove:hover { color: #ef4444; }

.no-members { text-align: center; color: #999; font-size: 14px; margin: 16px 0; }

.btn-close {
  width: 100%;
  padding: 12px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  background: #fff;
  font-size: 14px;
  cursor: pointer;
}

.btn-close:hover { background: #f5f5f5; }
</style>