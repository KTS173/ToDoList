<template>
    <Teleport to="body">
        <div v-if="modelValue" class="modal-overlay" @click.self="close">
            <div class="modal-content">
                <h2>Edit Project</h2>

                <div class="form-group">
                    <label class="form-label">Project Name</label>
                    <input v-model="name" type="text" class="form-input"/>
                </div>

                <div class="form-group">
                    <label class="form-label">Description</label>
                    <textarea v-model="description" class="form-input" rows="3" placeholder="Describe your project..."></textarea>
                </div>

                <div class="form-group">
                    <label class="form-label">Icon</label>
                    <div style="position: relative;">
                        <button class="emoji-btn" @click="showEmojiPicker = !showEmojiPicker">
                            {{ emoji }}
                        </button>
                        <EmojiPicker v-if="showEmojiPicker" @select="(e) => { emoji = e.i; showEmojiPicker = false }" />
                    </div>
                </div>

                <div class="form-group">
                    <label class="form-label">Project Color</label>
                    <div class="color-circles">
                        <button
                            v-for="c in colors"
                            :key="c"
                            class="color-circle"
                            :class="{ selected: color === c }"
                            :style="{ background: c }"
                            @click="color = c"
                        ></button>
                    </div>
                </div>

                <!-- Danger Zone -->
                <div class="danger-zone">
                    <span class="danger-label">Danger Zone</span>
                    <button class="btn-delete" @click="confirmDelete = true">
                        <Trash2 :size="14" /> Delete Project
                    </button>
                </div>

                <!-- Confirm -->
                <div v-if="confirmDelete" class="confirm-box">
                    <p>Delete <strong>{{ name }}</strong>? This will remove all tasks permanently.</p>
                    <div class="confirm-actions">
                        <button class="btn-cancel" @click="confirmDelete = false">Cancel</button>
                        <button class="btn-delete-confirm" :disabled="deleting" @click="deleteProject">
                            {{ deleting ? 'Deleting...' : 'Yes, Delete' }}
                        </button>
                    </div>
                </div>

                <div class="form-actions">
                    <button class="btn-cancel" @click="close">Cancel</button>
                    <button class="btn-save" :disabled="!name" @click="save">Save</button>
                </div>
            </div>
        </div>
    </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import EmojiPicker from 'vue3-emoji-picker'
import 'vue3-emoji-picker/css'
import { Trash2 } from 'lucide-vue-next'

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const props = defineProps({
    modelValue: { type: Boolean, default: false },
    project:    { type: Object,  default: null }
})

const emit   = defineEmits(['update:modelValue', 'updated'])
const router = useRouter()

const emoji           = ref('💡')
const showEmojiPicker = ref(false)
const colors          = ['#3b82f6','#ef4444','#10b981','#a855f7','#f97316','#14b8a6','#ec4899','#8b5cf6','#6b7280']
const name            = ref('')
const color           = ref('#3b82f6')
const description     = ref('')
const confirmDelete   = ref(false)
const deleting        = ref(false)

watch(() => props.project, (p) => {
    if (p) {
        name.value        = p.name        || ''
        color.value       = p.color       || '#3b82f6'
        description.value = p.description || ''
        emoji.value       = p.emoji       || '🗂️'
    }
}, { immediate: true })

function close() {
    confirmDelete.value = false
    emit('update:modelValue', false)
}

function getHeaders() {
    const token = localStorage.getItem('token')
    return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
}

async function save() {
    await fetch(`${API}/api/projects/${props.project.id}`, {
        method:  'PATCH',
        headers: getHeaders(),
        body:    JSON.stringify({ name: name.value, color: color.value, description: description.value, emoji: emoji.value })
    })
    emit('updated')
    close()
}

async function deleteProject() {
    deleting.value = true
    try {
        await fetch(`${API}/api/projects/${props.project.id}`, {
            method:  'DELETE',
            headers: getHeaders()
        })
        window.dispatchEvent(new Event('projects-updated'))
        close()
        router.push('/')
    } finally {
        deleting.value = false
    }
}
</script>

<style scoped>
.modal-overlay {
    position: fixed; inset: 0; background: rgba(0,0,0,0.4);
    display: flex; align-items: center; justify-content: center; z-index: 1000;
}
.modal-content {
    background: #fff; border-radius: 20px; padding: 36px 40px;
    width: 520px; max-width: 90vw;
}
.modal-content h2 { margin: 0 0 24px; font-size: 20px; font-weight: 700; }

.form-group { margin-bottom: 20px; }
.form-label { display: block; font-size: 13px; font-weight: 600; color: #1a1a2e; margin-bottom: 8px; }
.form-input {
    width: 100%; padding: 10px 14px; border: 1px solid #e5e7eb;
    border-radius: 10px; font-size: 14px; font-family: inherit;
    color: #333; outline: none; box-sizing: border-box; transition: border-color 0.2s;
}
.form-input:focus { border-color: #3b82f6; }

.color-circles { display: flex; gap: 10px; }
.color-circle {
    width: 34px; height: 34px; border-radius: 50%;
    border: 3px solid transparent; cursor: pointer; transition: all 0.15s;
}
.color-circle.selected { border-color: #fff; box-shadow: 0 0 0 2px currentColor; }

.emoji-btn {
    width: 48px; height: 48px; font-size: 24px; border: 2px solid #e5e7eb;
    border-radius: 12px; background: #f8f9fb; cursor: pointer;
    display: flex; align-items: center; justify-content: center; transition: border-color 0.2s;
}
.emoji-btn:hover { border-color: #3b82f6; }

/* Danger Zone */
.danger-zone {
    display: flex; align-items: center; justify-content: space-between;
    border-top: 1px solid #fee2e2; padding-top: 16px; margin-bottom: 20px;
}
.danger-label { font-size: 13px; font-weight: 600; color: #ef4444; }
.btn-delete {
    display: flex; align-items: center; gap: 6px;
    padding: 7px 14px; border: 1px solid #fecaca;
    border-radius: 8px; background: #fff5f5; color: #ef4444;
    font-size: 13px; font-weight: 500; cursor: pointer; font-family: inherit;
}
.btn-delete:hover { background: #fee2e2; }

.confirm-box {
    background: #fff5f5; border: 1px solid #fecaca;
    border-radius: 10px; padding: 16px; margin-bottom: 16px;
}
.confirm-box p { margin: 0 0 12px; font-size: 13px; color: #7f1d1d; }
.confirm-actions { display: flex; gap: 8px; justify-content: flex-end; }
.btn-delete-confirm {
    padding: 8px 18px; border: none; border-radius: 8px;
    background: #ef4444; color: #fff; font-size: 13px;
    font-weight: 600; cursor: pointer; font-family: inherit;
}
.btn-delete-confirm:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-delete-confirm:hover:not(:disabled) { background: #dc2626; }

.form-actions { display: flex; justify-content: space-between; align-items: center; }
.btn-cancel {
    padding: 10px 20px; border: 1px solid #e5e7eb; border-radius: 10px;
    background: #fff; font-size: 14px; cursor: pointer; font-family: inherit; color: #333;
}
.btn-cancel:hover { background: #f5f5f5; }
.btn-save {
    padding: 12px 28px; border: none; border-radius: 10px;
    background: #3b82f6; color: #fff; font-size: 14px;
    font-weight: 600; cursor: pointer; font-family: inherit; transition: background 0.2s;
}
.btn-save:hover:not(:disabled) { background: #2563eb; }
.btn-save:disabled { opacity: 0.5; cursor: not-allowed; }
</style>