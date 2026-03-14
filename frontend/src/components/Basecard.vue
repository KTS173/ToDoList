<template>
  <div class="card">
    <div class="icon-wrapper" :style="{ backgroundColor: iconBg }">
      <span class="icon">{{ icon }}</span>
    </div>
    <h2 class="total">{{ total }}</h2>
    <p class="msg">{{ msg }}</p>
  </div>
</template>

<script setup>
defineProps({
  msg: String,
  total: [String, Number],
  icon: { type: String, default: '' },
  iconBg: { type: String, default: '#f0f0f0' }
})
</script>

<style scoped>
.card {
  display: flex;
  flex: 1;
  flex-direction: column;
  align-items: center;
  justify-content: left;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 24px 20px;
  min-width: 120px;
}

.icon-wrapper {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
  font-size: 18px;
}

.total {
  font-size: 32px;
  font-weight: 700;
  color: #2c3e50;
  margin: 0 0 4px 0;
}

.msg {
  font-size: 14px;
  color: #7f8c9b;
  margin: 0;
}
</style>