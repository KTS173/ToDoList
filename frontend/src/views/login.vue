<script setup>
import { ref, computed } from "vue"
import { useRouter } from "vue-router"

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const email    = ref("")
const password = ref("")
const loading  = ref(false)
const errors   = ref({})
const serverError = ref("")
const router   = useRouter()

function validate() {
    // [Checklist: มีการ validate ข้อมูลทั้งหน้าและหลังบ้าน (Y)]
    // ส่วนนี้ชี้ไปที่การตรวจสอบข้อมูลในส่วนของ Frontend
    // การทำงาน: สำหรับหน้า Login จะมีการใช้ Regex เพื่อเช็คความเป็นไปได้ของ Format อีเมล 
    // รวมทั้งตรวจสอบความยาวพาสเวิร์ดเบื้องต้น หากไม่ผ่าน จะแสดง Error ใต้ช่องกรอกนั้นๆ 
    // โดยยังไม่ส่งข้อมูลใดๆ กลับไปยังเครื่องเซิร์ฟเวอร์ เพื่อช่วยลดภาระโหลดและ Bandwidth ของระบบ
    const e = {}
    if (!email.value)                            e.email = "Email is required"
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) e.email = "Invalid email format"
    if (!password.value)                         e.password = "Password is required"
    else if (password.value.length < 6)          e.password = "Password must be at least 6 characters"
    errors.value = e
    return Object.keys(e).length === 0
}

async function login() {
    serverError.value = ""
    if (!validate()) return
    loading.value = true
    try {
        const res  = await fetch(`${API}/login`, {
            method:  "POST",
            headers: { "Content-Type": "application/json" },
            body:    JSON.stringify({ email: email.value, password: password.value })
        })
        const data = await res.json()
        if (res.ok) {
            localStorage.setItem('token', data.token)
            localStorage.setItem('email', data.email)
            localStorage.setItem('name',  data.name)
            router.push('/')
        } else {
            serverError.value = data.detail || "Login failed"
        }
    } catch {
        serverError.value = "Cannot connect to server"
    } finally {
        loading.value = false
    }
}

function googleLogin() {
    window.location.href = `${API}/login/google`
}
</script>

<template>
    <div class="login-page">
        <div class="login-card">
            <div class="logo">✔</div>
            <h1>Doify</h1>
            <p class="subtitle">Welcome back! Sign in to continue.</p>

            <div v-if="serverError" class="server-error">{{ serverError }}</div>

            <form @submit.prevent="login">
                <div class="field">
                    <input
                        v-model="email"
                        type="text"
                        placeholder="Email address"
                        :class="{ 'input-error': errors.email }"
                        @input="delete errors.email"
                    />
                    <span v-if="errors.email" class="error-msg">{{ errors.email }}</span>
                </div>

                <div class="field">
                    <input
                        v-model="password"
                        type="password"
                        placeholder="Password"
                        :class="{ 'input-error': errors.password }"
                        @input="delete errors.password"
                    />
                    <span v-if="errors.password" class="error-msg">{{ errors.password }}</span>
                </div>

                <button class="login-btn" :disabled="loading">
                    {{ loading ? 'Signing in...' : 'Sign In →' }}
                </button>
            </form>

            <div class="divider"><span>OR</span></div>

            <button class="google-btn" @click="googleLogin">
                <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" width="18" />
                Continue with Google
            </button>

            <p class="signup">Don't have an account? <router-link to="/signup">Sign up</router-link></p>
        </div>
    </div>
</template>

<style scoped>
/* ── Layout & Background ── */
.login-page { 
    display: flex; 
    justify-content: center; 
    align-items: center; 
    height: 100vh; 
    background: #f5f6f8; 
}

/* ── Login Card Container ── */
.login-card { 
    width: 380px; 
    max-width: 90%; /* Added for mobile responsiveness */
    background: white; 
    padding: 40px; 
    border-radius: 20px; 
    box-shadow: 0 10px 25px rgba(0,0,0,0.08); 
    text-align: center; 
    box-sizing: border-box; /* Ensure padding doesn't push width out */
}

/* Responsive adjustments for very small screens */
@media (max-width: 480px) {
    .login-card {
        padding: 30px 20px; /* Reduce padding on mobile */
    }
}

/* ── Logo & Typography ── */
.logo { 
    width: 70px; 
    height: 70px; 
    margin: auto; 
    background: #4a77c9; 
    border-radius: 16px; 
    display: flex; 
    justify-content: center; 
    align-items: center; 
    color: white; 
    font-size: 28px; 
}
h1 { margin-top: 20px; font-size: 28px; }
.subtitle { color: #7b8190; margin-bottom: 25px; }

/* ── Error Messages ── */
.server-error {
    background: #fef2f2; 
    border: 1px solid #fecaca; 
    color: #dc2626;
    border-radius: 10px; 
    padding: 10px 14px; 
    font-size: 13px; 
    margin-bottom: 16px;
}

/* ── Form Fields ── */
.field { margin-bottom: 14px; text-align: left; }
input {
    width: 100%; 
    padding: 14px; 
    border-radius: 12px;
    border: 1px solid #e2e4ea; 
    font-size: 14px; 
    box-sizing: border-box;
    outline: none; 
    transition: border-color 0.2s;
}
input:focus { border-color: #4a77c9; }
input.input-error { border-color: #ef4444; }
.error-msg { font-size: 12px; color: #ef4444; margin-top: 4px; display: block; }

/* ── Buttons ── */
.login-btn { 
    width: 100%; 
    padding: 14px; 
    border: none; 
    border-radius: 12px; 
    background: #4a77c9; 
    color: white; 
    font-weight: 600; 
    font-size: 16px; 
    cursor: pointer; 
    transition: background 0.2s; 
}
.login-btn:hover:not(:disabled) { background: #3f67b0; }
.login-btn:disabled { opacity: 0.6; cursor: not-allowed; }

/* ── Dividers & Footer ── */
.divider { margin: 20px 0; color: #aaa; }
.google-btn { 
    width: 100%; 
    padding: 12px; 
    border-radius: 12px; 
    border: 1px solid #e2e4ea; 
    background: white; 
    cursor: pointer; 
    display: flex; 
    align-items: center; 
    justify-content: center; 
    gap: 10px; 
    font-size: 14px; 
}
.google-btn:hover { background: #f8f9fa; }
.signup { margin-top: 20px; font-size: 14px; }
</style>