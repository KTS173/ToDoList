<template>
    <div class="modal-content">
        <div class="stepper">
            <div class="step-item done">
                <CheckCircle2 :size="20" />
                <span>Project Type</span>
            </div>
            <div class="step-line active"></div>
            <div class="step-item active">
                <span class="step-number">2</span>
                <span>Project Details</span>
            </div>
        </div>

        <h2 class="modal-title">Configure Corporate Project</h2>
        <p class="modal-subtitle">Set up your collaborative workspace.</p>

        <div class="form-row">
            <div class="form-group flex-1">
                <label class="form-label">Project Name</label>
                <input v-model="name" type="text" class="form-input" placeholder="E.g., Q4 Marketing Campaign" />
            </div>
            <div class="form-group">
                <label class="form-label">Project Color</label>
                <div class="color-dropdown" @click="showDropdown = !showDropdown">
                    <span class="color-dot" :style="{ background: color }"></span>
                    <span>{{ colorName }}</span>
                    <ChevronDown :size="16" />
                </div>
                <div v-if="showDropdown" class="color-dropdown-list">
                    <div
                        v-for="(cName, cValue) in colorMap"
                        :key="cValue"
                        class="color-dropdown-item"
                        @click="color = cValue; showDropdown = false"
                    >
                        <span class="color-dot" :style="{ background: cValue }"></span>
                        <span>{{ cName }}</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="form-group">
            <div class="invite-header">
                <label class="form-label">Invite Team Members</label>
                <span class="member-count">{{ members.length }} members added</span>
            </div>
            <div class="invite-row">
                <input v-model="memberEmail" type="email" class="form-input flex-1" placeholder="Enter email address" @keyup.enter="addMember" />
                <button class="btn-add" @click="addMember">Add</button>
            </div>
            <div v-if="members.length" class="member-list">
                <div v-for="(m, i) in members" :key="i" class="member-item">
                    <div class="member-avatar" :style="{ background: m.color }">{{ m.initials }}</div>
                    <div class="member-info">
                        <p class="member-name">{{ m.name }}</p>
                        <p class="member-email">{{ m.email }}</p>
                    </div>
                    <select v-model="m.role" class="member-role">
                        <option value="Admin">Admin</option>
                        <option value="Member">Member</option>
                    </select>
                    <button class="btn-remove-member" @click="members.splice(i, 1)">
                        <X :size="16" />
                    </button>
                </div>
            </div>
        </div>

        <div class="form-actions">
            <button class="btn-back" @click="$emit('back')">
                <ArrowLeft :size="16" /> Back
            </button>
            <button class="btn-create" :disabled="!name" @click="$emit('create', { name, color, members })">
                Create Project <Check :size="18" />
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { CheckCircle2, ChevronDown, X, ArrowLeft, Check } from 'lucide-vue-next'

defineEmits(['back', 'create'])

const colorMap = {
    '#3b82f6': 'Blue',
    '#ef4444': 'Red',
    '#10b981': 'Green',
    '#a855f7': 'Purple',
    '#f97316': 'Orange',
    '#14b8a6': 'Teal',
    '#ec4899': 'Pink',
    '#8b5cf6': 'Violet',
    '#6b7280': 'Gray'
}

const name = ref('')
const color = ref('#3b82f6')
const showDropdown = ref(false)
const memberEmail = ref('')
const members = ref([])

const colorName = computed(() => colorMap[color.value] || 'Blue')

const avatarColors = ['#3b82f6', '#a855f7', '#f97316', '#10b981', '#ef4444']

function addMember() {
    const email = memberEmail.value.trim()
    if (!email) return
    const mName = email.split('@')[0].replace(/[._]/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
    const initials = mName.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase()
    members.value.push({
        email,
        name: mName,
        initials,
        role: 'Member',
        color: avatarColors[members.value.length % avatarColors.length]
    })
    memberEmail.value = ''
}
</script>

<style scoped>
.modal-content {
    background: #fff;
    border-radius: 20px;
    padding: 36px 40px;
    width: 600px;
    max-width: 90vw;
    text-align: center;
}

.modal-title {
    font-size: 22px;
    font-weight: 700;
    color: #1a1a2e;
    margin: 0 0 6px;
}
.modal-subtitle {
    font-size: 14px;
    color: #999;
    margin: 0 0 24px;
}

/* Stepper */
.stepper {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    margin-bottom: 24px;
}
.step-item {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 13px;
    color: #aaa;
    font-weight: 500;
}
.step-item.done { color: #3b82f6; }
.step-item.active { color: #3b82f6; }
.step-number {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: #3b82f6;
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 700;
}
.step-line {
    width: 40px;
    height: 2px;
    background: #e5e7eb;
    border-radius: 1px;
}
.step-line.active { background: #22c55e; }

/* Form */
.form-group { margin-bottom: 20px; text-align: left; }
.form-label {
    display: block;
    font-size: 13px;
    font-weight: 600;
    color: #1a1a2e;
    margin-bottom: 8px;
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
.form-input::placeholder { color: #bbb; }

.form-row {
    display: flex;
    gap: 16px;
    align-items: flex-start;
    text-align: left;
}
.flex-1 { flex: 1; }

/* Color dropdown */
.color-dropdown {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 14px;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    cursor: pointer;
    font-size: 14px;
    color: #333;
    min-width: 130px;
    position: relative;
}
.color-dot {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    flex-shrink: 0;
}
.color-dropdown-list {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    margin-top: 4px;
    z-index: 10;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    max-height: 200px;
    overflow-y: auto;
}
.color-dropdown-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 14px;
    cursor: pointer;
    font-size: 13px;
}
.color-dropdown-item:hover { background: #f5f5f5; }

/* Invite members */
.invite-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}
.invite-header .form-label { margin-bottom: 0; }
.member-count { font-size: 12px; color: #3b82f6; }

.invite-row {
    display: flex;
    gap: 10px;
    margin-bottom: 12px;
}
.btn-add {
    padding: 10px 20px;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    background: #fff;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    font-family: inherit;
    color: #333;
}
.btn-add:hover { background: #f5f5f5; }

.member-list {
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    overflow: hidden;
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
    color: #fff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 700;
    flex-shrink: 0;
}
.member-info { flex: 1; text-align: left; }
.member-name {
    font-size: 13px;
    font-weight: 600;
    color: #1a1a2e;
    margin: 0;
}
.member-email {
    font-size: 11px;
    color: #999;
    margin: 0;
}
.member-role {
    padding: 4px 10px;
    border: 1px solid #e5e7eb;
    border-radius: 6px;
    font-size: 12px;
    font-family: inherit;
    color: #333;
    background: #fff;
    cursor: pointer;
}
.btn-remove-member {
    background: none;
    border: none;
    color: #bbb;
    cursor: pointer;
    padding: 4px;
}
.btn-remove-member:hover { color: #ef4444; }

/* Actions */
.form-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.btn-back {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 10px 20px;
    border: 1px solid #e5e7eb;
    border-radius: 10px;
    background: #fff;
    font-size: 14px;
    cursor: pointer;
    font-family: inherit;
    color: #333;
}
.btn-back:hover { background: #f5f5f5; }
.btn-create {
    display: flex;
    align-items: center;
    gap: 6px;
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
.btn-create:hover:not(:disabled) { background: #2563eb; }
.btn-create:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
