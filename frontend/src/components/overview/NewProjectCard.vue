<template>
    <div class="new-project-card" @click="showModal = true">
        <div class="plus-icon">
            <Plus :size="32" />
        </div>
        <p class="new-project-title">New Project</p>
        <div class="new-project-labels">
            <span>Personal</span>
            <span>Corporate</span>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { Plus, User, Users, ArrowRight } from 'lucide-vue-next'

const showModal = ref(false)
const selectedType = ref(null)

const emit = defineEmits(['next'])

function handleNext() {
    emit('next', selectedType.value)
    showModal.value = false
    selectedType.value = null
}
</script>

<style scoped>
.new-project-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 240px;
    height: 300px;
    border: 2px dashed #d1d5db;
    border-radius: 16px;
    cursor: pointer;
    background: #fff;
    transition: all 0.2s;
}
.new-project-card:hover {
    border-color: #93a3b8;
    background: #f8fafc;
}

.plus-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    background: #f1f5f9;
    color: #94a3b8;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 12px;
}

.new-project-title {
    font-size: 15px;
    font-weight: 600;
    color: #1a1a2e;
    margin: 0 0 8px;
}

.new-project-labels {
    display: flex;
    gap: 12px;
    font-size: 12px;
    color: #999;
}

/* Modal */
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
}

.modal-content {
    background: #fff;
    border-radius: 20px;
    padding: 40px;
    width: 520px;
    max-width: 90vw;
    text-align: center;
}

.modal-title {
    font-size: 24px;
    font-weight: 700;
    color: #1a1a2e;
    margin: 0 0 8px;
}

.modal-subtitle {
    font-size: 14px;
    color: #999;
    margin: 0 0 28px;
}

.modal-options {
    display: flex;
    gap: 16px;
    margin-bottom: 28px;
}

.option-card {
    flex: 1;
    padding: 24px 16px;
    border: 2px solid #f0f0f0;
    border-radius: 14px;
    cursor: pointer;
    transition: all 0.2s;
    background: #fafafa;
}
.option-card:hover {
    border-color: #c5d1e0;
}
.option-card.selected {
    border-color: #3b82f6;
    background: #f0f6ff;
}

.option-icon {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 14px;
}

.personal-icon {
    background: #dbeafe;
    color: #3b82f6;
}

.corporate-icon {
    background: #f3e8ff;
    color: #a855f7;
}

.option-title {
    font-size: 15px;
    font-weight: 600;
    color: #1a1a2e;
    margin: 0 0 6px;
}

.option-desc {
    font-size: 12px;
    color: #999;
    margin: 0;
    line-height: 1.5;
}

.modal-next-btn {
    width: 100%;
    padding: 14px;
    border: none;
    border-radius: 12px;
    background: #93b5f7;
    color: #fff;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    font-family: inherit;
    transition: background 0.2s;
    margin-bottom: 12px;
}
.modal-next-btn:hover:not(:disabled) {
    background: #3b82f6;
}
.modal-next-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}

.modal-cancel-btn {
    background: none;
    border: none;
    color: #999;
    font-size: 14px;
    cursor: pointer;
    font-family: inherit;
}
.modal-cancel-btn:hover {
    color: #666;
}
</style>
