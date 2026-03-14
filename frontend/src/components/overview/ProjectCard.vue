<template>
    <div class="project-card" :style="{ background: `linear-gradient(135deg, ${color}20, #fff)` }">
        <div class="card-head">
            <span class="project-icon">
                <template v-if="emoji">{{ emoji }}</template>
                <Book v-else :size="24"/>
            </span>

            <span class="project-setting" @click.stop>
                <Ellipsis :size="24" @click="setting = !setting"/>
                <div v-if="setting" class="setting-dropdown">
                    <button @click.stop="$emit('edit'); setting = false">Edit</button>
                    <button @click.stop="$emit('delete')">Delete</button>
                </div>
            </span>
        </div>
        <div class="card-body">
            <div class="info">
                <p class="project-title"> {{ project_title }}</p>
                <p class="project-details"> {{ details }}</p>
            </div>

            <div class="project-score">
                <div class="score-item">
                    <span class="score-number">{{ done }}</span>
                    <span class="score-label">DONE</span>
                </div>
                <div class="score-item">
                    <span class="score-number">{{ todo }}</span>
                    <span class="score-label">TO DO</span>
                </div>
            </div>

        </div>
        <div class="card-bottom">
            <div class="progress-header">
                <span class="progress-title">Progress</span>
                <span class="progress-percent">{{ percent }}%</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" :style="{ width: percent + '%' }"></div>
            </div>
            <div v-if="showTeam" class="team-row">
                <span class="team-label">TEAM</span>
                <div class="team-avatars">
                  <div
                    class="team-avatar"
                    v-for="m in displayMembers"
                    :key="m.id"
                    :title="m.name"
                  >
                    {{ getInitials(m.name) }}
                  </div>
                  <div v-if="members.length > 3" class="team-avatar avatar-more">
                    +{{ members.length - 3 }}
                  </div>
                </div>
                <a class="add-member" href="#" @click.stop.prevent="$emit('add-member')">+ Add Member</a>
            </div>
        </div>
    </div>
</template>

<script setup>
import {ref, computed} from 'vue'
import { Book, Ellipsis } from 'lucide-vue-next'

const props = defineProps({
    project_title: { type: String, default: 'Project 1' },
    details : {type : String},
    done: { type: Number, default: 0 },
    todo: { type: Number, default: 0 },
    percent: { type: Number, default: 0 },
    showTeam: { type: Boolean, default: false },
    members: { type: Array, default: () => [] },
    color: { type: String, default: '#3b82f6' },
    emoji: { type: String, default: '' }

})

const setting = ref(false)
const emit = defineEmits(['delete', 'add-member', 'edit'])

const displayMembers = computed(() => props.members.slice(0, 3))

function getInitials(name) {
  return name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase()
}

</script>

<style scoped>
.project-card {
    display: flex;
    flex-direction: column;
    width: 240px;
    height: 300px;
    background: #fff;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.card-head {
    display: flex;
    justify-content: space-between;
    margin-bottom: 24px;
}

.project-icon {
    width: 45px;
    height: 45px;
    border-radius: 20%;
    background: #fcfcfc;
    color: #320909;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 40px;
}

.project-setting {
    color: #bbb;
    cursor: pointer;
    position: relative;
}

.setting-dropdown {
    position: absolute;
    top: 24px;
    right: 0;
    background: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    padding: 4px;
    z-index: 10;
}

.setting-dropdown button {
    background: none;
    border: none;
    padding: 8px 16px;
    cursor: pointer;
    color: #ef4444;
    font-size: 14px;
    white-space: nowrap;
    font-style: normal;
    display: block;
    width: 100%;
    text-align: left;
}

.setting-dropdown button:first-child {
    color: #333;           
}

.setting-dropdown button:last-child {
    color: #ef4444;        
}
.setting-dropdown button:hover {
    background: #fee2e2;
    border-radius: 4px;
}


.card-body {
    font-family: inherit;
    flex: 1;
    display: flex;
    flex-direction: column;
}

.info {
    display: 1;
}

.project-title {
    font-size: 16px;
    font-weight: 700;
    color: #1a1a2e;
    margin: 0 0 4px;
}

.project-details {
    font-size: 12px;
    color: #999;
    margin: 0;
}


.project-score {
    display: flex;
    gap: 20px;
    margin-top: auto;
}

.score-item {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.score-item + .score-item {
    border-left: 1px solid #e5e7eb;
    padding-left: 20px;
}

.score-number {
    font-size: 24px;
    font-weight: 700;
    color: #1a1a2e;
    line-height: 1;
}

.score-label {
    font-size: 10px;
    color: #aaa;
    font-weight: 600;
    margin-top: 4px;
}

.card-bottom {
    margin-top: 14px;
}

.progress-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 6px;
}

.progress-title {
    font-size: 12px;
    color: #888;
}

.progress-percent {
    font-size: 12px;
    font-weight: 600;
    color: #1a1a2e;
}

.progress-bar {
    height: 6px;
    background: #e8e5e0;
    border-radius: 3px;
    overflow: hidden;
    margin-bottom: 14px;
}

.progress-fill {
    height: 100%;
    background: #3b82f6;
    border-radius: 3px;
    transition: width 0.3s;
}

.team-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.team-label {
    font-size: 10px;
    font-weight: 600;
    color: #aaa;
}

.team-avatars {
    display: flex;
    align-items: center;
}

.team-avatar {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: #e2e8f0;
    border: 2px solid #fff;
    margin-left: -6px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #64748b;
    font-size: 9px;
    font-weight: 600;
}

.team-avatar:first-child { margin-left: 0; }
.avatar-more { background: #f1f5f9; color: #64748b; }

.add-member {
    font-size: 12px;
    color: #3b82f6;
    text-decoration: none;
    font-weight: 500;
}

</style>