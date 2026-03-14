<template>
    <div class="modal-content">
        <h2 class="modal-title">Create New Project</h2>
        <p class="modal-subtitle">Choose the type of project you want to start.</p>

        <div class="modal-options">
            <div
                class="option-card"
                :class="{ selected: selected === 'personal' }"
                @click="selected = 'personal'"
            >
                <div class="option-icon personal-icon">
                    <User :size="28" />
                </div>
                <p class="option-title">Personal Project</p>
                <p class="option-desc">Just for you.</p>
                <p class="option-desc">Private and focused.</p>
            </div>

            <div
                class="option-card"
                :class="{ selected: selected === 'corporate' }"
                @click="selected = 'corporate'"
            >
                <div class="option-icon corporate-icon">
                    <Users :size="28" />
                </div>
                <p class="option-title">Corporate Project</p>
                <p class="option-desc">Collaborate with others.</p>
                <p class="option-desc">Share tasks and progress.</p>
            </div>
        </div>

        <button class="btn-next" :disabled="!selected" @click="$emit('next', selected)">
            Next <ArrowRight :size="18" />
        </button>
        <button class="btn-cancel" @click="$emit('cancel')">Cancel</button>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { User, Users, ArrowRight } from 'lucide-vue-next'

const selected = ref(null)

defineEmits(['next', 'cancel'])
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

.modal-options {
    display: flex;
    gap: 16px;
    margin-bottom: 24px;
}

.option-card {
    flex: 1;
    padding: 24px 16px;
    border: 2px solid #f0f0f0;
    border-radius: 14px;
    cursor: pointer;
    transition: all 0.2s;
    background: #fafafa;
    text-align: center;
}
.option-card:hover { border-color: #c5d1e0; }
.option-card.selected { border-color: #3b82f6; background: #f0f6ff; }

.option-icon {
    width: 52px;
    height: 52px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 14px;
}
.personal-icon { background: #dbeafe; color: #3b82f6; }
.corporate-icon { background: #f3e8ff; color: #a855f7; }

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

.btn-next {
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
.btn-next:hover:not(:disabled) { background: #3b82f6; }
.btn-next:disabled { opacity: 0.6; cursor: not-allowed; }

.btn-cancel {
    display: block;
    margin: 0 auto;
    background: none;
    border: none;
    color: #999;
    font-size: 14px;
    cursor: pointer;
    font-family: inherit;
}
.btn-cancel:hover { color: #666; }
</style>

