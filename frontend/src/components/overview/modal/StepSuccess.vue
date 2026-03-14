<template>
    <div class="modal-content">
        <div class="success-icon">
            <Check :size="32" />
        </div>
        <h2 class="modal-title">Project {{ projectName }} Created!</h2>
        <p class="modal-subtitle">Your new {{ projectType }} project has been set up with the chosen color.</p>

        <button class="btn-dashboard" @click="$emit('dashboard')">Go to Dashboard</button>
        <button class="btn-another" @click="$emit('another')">Create Another</button>
    </div>
</template>

<script setup>
import { Check } from 'lucide-vue-next'

defineProps({
    projectName: { type: String, default: '' },
    projectType: { type: String, default: '' }
})

defineEmits(['dashboard', 'another'])
</script>

<style scoped>
.modal-content {
    background: #fff;
    border-radius: 20px;
    padding: 36px 40px;
    width: 520px;
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

.success-icon {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    background: #eff6ff;
    color: #3b82f6;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 20px;
}

.btn-dashboard {
    width: 100%;
    padding: 14px;
    border: none;
    border-radius: 12px;
    background: #3b82f6;
    color: #fff;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    font-family: inherit;
    margin-bottom: 10px;
    transition: background 0.2s;
}
.btn-dashboard:hover { background: #2563eb; }

.btn-another {
    width: 100%;
    padding: 14px;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    background: #fff;
    color: #333;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    font-family: inherit;
}
.btn-another:hover { background: #f5f5f5; }
</style>
