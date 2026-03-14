<template>
    <Teleport to="body">
        <div v-if="modelValue" class="modal-overlay" @click.self="close">
            <SelectType v-if="step === 1" @next="onTypeSelected" @cancel="close" />
            <StepConfigPersonal v-else-if="step === 2 && selectedType === 'personal'" @back="step = 1" @create="onCreated" />
            <StepConfigCorporate v-else-if="step === 2 && selectedType === 'corporate'" @back="step = 1" @create="onCreated" />
            <StepSuccess v-else-if="step === 3" :projectName="createdProject.name" :projectType="selectedType" @dashboard="close" @another="resetForm" />
        </div>
    </Teleport>
</template>

<script setup>
import { ref } from 'vue'
import SelectType from './SelectType.vue'
import StepConfigPersonal from './StepConfigPersonal.vue'
import StepConfigCorporate from './StepConfigCorporate.vue'
import StepSuccess from './StepSuccess.vue'

defineProps({
    modelValue: { type: Boolean, default: false }
})
const emit = defineEmits(['update:modelValue', 'created'])

const step = ref(1)
const selectedType = ref(null)
const createdProject = ref({})

function onTypeSelected(type) {
    selectedType.value = type
    step.value = 2
}

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function getHeaders() {
    const token = localStorage.getItem('token')
    return { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` }
}

async function onCreated(data) {
    try {
        const res = await fetch(`${API}/api/projects`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify({ name: data.name, color: data.color, type: selectedType.value })
        })
        const project = await res.json()
        createdProject.value = project

        // Add members for corporate project
        if (selectedType.value === 'corporate' && data.members?.length) {
            for (const m of data.members) {
                await fetch(`${API}/api/projects/${project.id}/members`, {
                    method: 'POST',
                    headers: getHeaders(),
                    body: JSON.stringify({ email: m.email, name: m.name, role: m.role })
                })
            }
        }

        emit('created', project)
        step.value = 3
    } catch (err) {
        console.error('Create project error:', err)
        alert('Failed to create project')
    }
}

function resetForm() {
    step.value = 1
    selectedType.value = null
    createdProject.value = {}
}

function close() {
    resetForm()
    emit('update:modelValue', false)
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
</style>
