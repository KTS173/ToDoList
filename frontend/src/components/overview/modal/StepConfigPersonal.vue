<template>
    <div class="modal-content">
        <div class="stepper">
            <div class="step-item done">
                <CheckCircle2 :size="20" />
                <span>Project Type</span>
            </div>
            <div class="step-line done"></div>
            <div class="step-item active">
                <span class="step-number">2</span>
                <span>Project Details</span>
            </div>
        </div>

        <h2 class="modal-title">Configure Personal Project</h2>
        <p class="modal-subtitle">Set up your workspace exactly how you like it.</p>

        <div class="form-group">
            <label class="form-label">Project Name</label>
            <input v-model="name" type="text" class="form-input" placeholder="e.g., My Portfolio 2024" />
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

        <div class="lock-row">
            <div class="lock-info">
                <Lock :size="18" />
                <div>
                    <p class="lock-title">Lock Project</p>
                    <p class="lock-desc">Password protect this project</p>
                </div>
            </div>
            <label class="toggle">
                <input v-model="locked" type="checkbox" />
                <span class="toggle-slider"></span>
            </label>
        </div>

        <div class="form-actions">
            <button class="btn-back" @click="$emit('back')">
                <ArrowLeft :size="16" /> Back
            </button>
            <button class="btn-create" :disabled="!name" @click="$emit('create', { name, color, locked })">
                Create Project
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { CheckCircle2, Lock, ArrowLeft } from 'lucide-vue-next'

defineEmits(['back', 'create'])

const colors = ['#3b82f6', '#ef4444', '#10b981', '#a855f7', '#f97316', '#14b8a6', '#ec4899', '#8b5cf6', '#6b7280']

const name = ref('')
const color = ref('#3b82f6')
const locked = ref(false)
</script>

<style scoped>
.modal-content {
    background: #fff;
    border-radius: 20px;
    padding: 36px 40px;
    width: 520px;
    max-width: 90vw;
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
.step-line.done { background: #22c55e; }

/* Form */
.form-group { margin-bottom: 20px; }
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

/* Color circles */
.color-circles { display: flex; gap: 10px; }
.color-circle {
    width: 34px;
    height: 34px;
    border-radius: 50%;
    border: 3px solid transparent;
    cursor: pointer;
    transition: all 0.15s;
}
.color-circle.selected {
    border-color: #fff;
    box-shadow: 0 0 0 2px currentColor;
}

/* Lock row */
.lock-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 16px;
    background: #f8f9fb;
    border-radius: 12px;
    margin-bottom: 24px;
}
.lock-info {
    display: flex;
    align-items: center;
    gap: 12px;
    color: #666;
}
.lock-title {
    font-size: 14px;
    font-weight: 600;
    color: #1a1a2e;
    margin: 0;
}
.lock-desc {
    font-size: 12px;
    color: #999;
    margin: 0;
}

/* Toggle */
.toggle { position: relative; width: 42px; height: 24px; }
.toggle input { display: none; }
.toggle-slider {
    position: absolute;
    inset: 0;
    background: #ddd;
    border-radius: 12px;
    cursor: pointer;
    transition: 0.2s;
}
.toggle-slider::before {
    content: '';
    position: absolute;
    width: 18px;
    height: 18px;
    background: #fff;
    border-radius: 50%;
    top: 3px;
    left: 3px;
    transition: 0.2s;
}
.toggle input:checked + .toggle-slider { background: #3b82f6; }
.toggle input:checked + .toggle-slider::before { left: 21px; }

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
