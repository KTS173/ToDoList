<template>
  <div class="settings-page">
    <h1 class="settings-title">Settings</h1>
    <p class="settings-sub">Manage your account information</p>

    <div class="settings-card">
      <div class="avatar-section">
        <div class="avatar-wrapper" @click="triggerUpload">
          <img v-if="avatarUrl" :src="avatarUrl" class="avatar-img" />
          <div v-else class="avatar">{{ initials }}</div>
          <div class="avatar-overlay">
            <Camera :size="16" />
          </div>
        </div>
        <input ref="fileInput" type="file" accept="image/*" class="hidden-input" @change="uploadAvatar" />
        <div class="avatar-info">
          <p class="avatar-name">{{ form.name || 'No name' }}</p>
          <p class="avatar-email">{{ form.email }}</p>
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">Name</label>
        <input v-model="form.name" type="text" class="form-input" placeholder="Your name" />
      </div>

      <div class="form-group">
        <label class="form-label">Email</label>
        <input v-model="form.email" type="email" class="form-input" placeholder="Your email" />
      </div>

      <div class="form-divider"></div>

      <h3 class="section-title">Change Password</h3>

      <div class="form-group">
        <label class="form-label">New Password</label>
        <input v-model="form.password" type="password" class="form-input" placeholder="Leave blank to keep current" />
      </div>

      <div class="form-group">
        <label class="form-label">Confirm Password</label>
        <input v-model="confirmPassword" type="password" class="form-input" placeholder="Confirm new password" />
      </div>

      <p v-if="message" :class="['message', messageType]">{{ message }}</p>

      <div class="form-actions">
        <button class="btn-save" :disabled="saving" @click="save">
          {{ saving ? 'Saving...' : 'Save Changes' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Camera } from 'lucide-vue-next'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const form            = ref({ name: '', email: '', password: '' })
const confirmPassword = ref('')
const saving          = ref(false)
const message         = ref('')
const messageType     = ref('success')
const avatarUrl       = ref('')
const fileInput       = ref(null)

function getHeaders() {
  const token = localStorage.getItem('token')
  return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
}

function getAuthHeader() {
  const token = localStorage.getItem('token')
  return { 'Authorization': `Bearer ${token}` }
}

const initials = computed(() => {
  const name = form.value.name
  if (!name) return '?'
  return name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase()
})

async function fetchUser() {
  const res  = await fetch(`${API}/api/me`, { headers: getHeaders() })
  const data = await res.json()
  form.value.name  = data.name  || ''
  form.value.email = data.email || ''
  avatarUrl.value  = data.avatar_url ? `${API}${data.avatar_url}` : ''
}

function triggerUpload() {
  fileInput.value.click()
}

async function uploadAvatar(e) {
  const file = e.target.files[0]
  if (!file) return

  const formData = new FormData()
  formData.append('file', file)

  try {
    const res = await fetch(`${API}/api/me/avatar`, {
      method:  'POST',
      headers: getAuthHeader(),
      body:    formData
    })
    if (!res.ok) throw new Error('Upload failed')
    const data  = await res.json()
    avatarUrl.value = `${API}${data.avatar_url}?t=${Date.now()}`
    message.value   = 'Avatar updated'
    messageType.value = 'success'
  } catch (err) {
    message.value   = 'Failed to upload avatar'
    messageType.value = 'error'
  }
}

async function save() {
  message.value = ''

  if (form.value.password && form.value.password !== confirmPassword.value) {
    message.value     = 'Passwords do not match'
    messageType.value = 'error'
    return
  }

  saving.value = true
  try {
    const body = { name: form.value.name, email: form.value.email }
    if (form.value.password) body.password = form.value.password

    const res = await fetch(`${API}/api/me`, {
      method:  'PATCH',
      headers: getHeaders(),
      body:    JSON.stringify(body)
    })

    if (!res.ok) {
      const err = await res.json()
      throw new Error(err.detail || 'Failed to update')
    }

    const data = await res.json()
    localStorage.setItem('token', data.token)
    localStorage.setItem('email', data.email)
    localStorage.setItem('name',  data.name || '')

    form.value.password = ''
    confirmPassword.value = ''
    message.value     = 'Settings saved successfully'
    messageType.value = 'success'
  } catch (err) {
    message.value     = err.message
    messageType.value = 'error'
  } finally {
    saving.value = false
  }
}

onMounted(fetchUser)
</script>

<style scoped>
.settings-page {
  padding: 32px 24px;
  max-width: 600px;
}

.settings-title {
  font-size: 24px;
  font-weight: 700;
  color: #1a1a2e;
  margin: 0;
}

.settings-sub {
  color: #94a3b8;
  font-size: 14px;
  margin: 4px 0 24px;
}

.settings-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 28px;
}

.avatar-section {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.avatar-wrapper {
  position: relative;
  width: 56px;
  height: 56px;
  cursor: pointer;
  border-radius: 50%;
  flex-shrink: 0;
}

.avatar-img {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  object-fit: cover;
}

.avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #3b82f6;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
}

.avatar-overlay {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: rgba(0,0,0,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  opacity: 0;
  transition: opacity 0.2s;
}

.avatar-wrapper:hover .avatar-overlay {
  opacity: 1;
}

.hidden-input { display: none; }

.avatar-name {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a2e;
  margin: 0;
}

.avatar-email {
  font-size: 13px;
  color: #94a3b8;
  margin: 2px 0 0;
}

.form-group { margin-bottom: 16px; }

.form-label {
  display: block;
  font-size: 13px;
  font-weight: 600;
  color: #1a1a2e;
  margin-bottom: 6px;
}

.form-input {
  width: 100%;
  padding: 10px 14px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  font-size: 14px;
  font-family: inherit;
  color: #333;
  outline: none;
  box-sizing: border-box;
  transition: border-color 0.2s;
}

.form-input:focus { border-color: #3b82f6; }

.form-divider {
  height: 1px;
  background: #e5e7eb;
  margin: 24px 0;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #1a1a2e;
  margin: 0 0 16px;
}

.form-actions { margin-top: 24px; }

.btn-save {
  padding: 12px 28px;
  border: none;
  border-radius: 10px;
  background: #3b82f6;
  color: #fff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  font-family: inherit;
  transition: background 0.2s;
}

.btn-save:hover:not(:disabled) { background: #2563eb; }
.btn-save:disabled { opacity: 0.5; cursor: not-allowed; }

.message {
  font-size: 13px;
  margin: 12px 0 0;
  padding: 8px 12px;
  border-radius: 8px;
}

.message.success { background: #f0fdf4; color: #16a34a; }
.message.error   { background: #fef2f2; color: #dc2626; }
</style>