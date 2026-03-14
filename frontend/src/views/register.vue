<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"

const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'
const email           = ref("")
const password        = ref("")
const confirmPassword = ref("")
const loading         = ref(false)
const errors          = ref({})
const serverError     = ref("")
const router          = useRouter()

function validate() {
    const e = {}
    if (!email.value)                                          e.email    = "Email is required"
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) e.email    = "Invalid email format"
    if (!password.value)                                       e.password = "Password is required"
    else if (password.value.length < 8)                        e.password = "Password must be at least 8 characters"
    else if (!/[A-Z]/.test(password.value))                    e.password = "Must contain at least one uppercase letter"
    else if (!/[0-9]/.test(password.value))                    e.password = "Must contain at least one number"
    if (!confirmPassword.value)                                e.confirm  = "Please confirm your password"
    else if (password.value !== confirmPassword.value)         e.confirm  = "Passwords do not match"
    errors.value = e
    return Object.keys(e).length === 0
}

async function register() {
    serverError.value = ""
    if (!validate()) return
    loading.value = true
    try {
        const res  = await fetch(`${API}/signup`, {
            method:  "POST",
            headers: { "Content-Type": "application/json" },
            body:    JSON.stringify({ email: email.value, password: password.value })
        })
        const data = await res.json()
        if (res.ok) {
            router.push("/login")
        } else {
            serverError.value = data.detail || "Signup failed"
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

// password strength indicator
function passwordStrength(pw) {
    if (!pw) return 0
    let score = 0
    if (pw.length >= 8)       score++
    if (/[A-Z]/.test(pw))     score++
    if (/[0-9]/.test(pw))     score++
    if (/[^A-Za-z0-9]/.test(pw)) score++
    return score
}
const strength = { 0: '', 1: 'weak', 2: 'fair', 3: 'good', 4: 'strong' }
</script>

<template>
    <div class="register-page">
        <div class="register-card">
            <div class="logo">✔</div>
            <h1>Doify</h1>
            <p class="subtitle">Create your account to get started</p>

            <div v-if="serverError" class="server-error">{{ serverError }}</div>

            <form @submit.prevent="register">
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
                    <div v-if="password" class="strength-bar">
                        <div
                            v-for="i in 4" :key="i"
                            class="strength-seg"
                            :class="{ active: passwordStrength(password) >= i, [strength[passwordStrength(password)]]: true }"
                        ></div>
                    </div>
                    <span v-if="errors.password" class="error-msg">{{ errors.password }}</span>
                    <span v-else-if="password" class="hint">Min 8 chars, 1 uppercase, 1 number</span>
                </div>

                <div class="field">
                    <input
                        v-model="confirmPassword"
                        type="password"
                        placeholder="Confirm password"
                        :class="{ 'input-error': errors.confirm }"
                        @input="delete errors.confirm"
                    />
                    <span v-if="errors.confirm" class="error-msg">{{ errors.confirm }}</span>
                </div>

                <button type="submit" class="register-btn" :disabled="loading">
                    {{ loading ? 'Creating account...' : 'Sign Up →' }}
                </button>
            </form>

            <div class="divider"><span>OR</span></div>

            <button class="google-btn" @click="googleLogin">
                <img src="https://www.gstatic.com/firebasejs/ui/2.0.0/images/auth/google.svg" width="18" />
                Continue with Google
            </button>

            <p class="login-link">Already have an account? <router-link to="/login">Sign in</router-link></p>
        </div>
    </div>
</template>

<style scoped>
/* ── Layout & Background ── */
.register-page { 
    display: flex; 
    justify-content: center; 
    align-items: center; 
    height: 100vh; 
    background: #f5f6f8; 
}

/* ── Register Card Container ── */
.register-card { 
    width: 380px; 
    max-width: 90%; /* Added for mobile responsiveness */
    background: white; 
    padding: 40px; 
    border-radius: 20px; 
    box-shadow: 0 10px 25px rgba(0,0,0,0.08); 
    text-align: center; 
    box-sizing: border-box;
}

@media (max-width: 480px) {
    .register-card {
        padding: 30px 20px; /* Adjust padding for mobile */
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
.hint { font-size: 12px; color: #94a3b8; margin-top: 4px; display: block; }

/* ── Password Strength Bar ── */
.strength-bar { display: flex; gap: 4px; margin-top: 6px; }
.strength-seg { height: 4px; flex: 1; border-radius: 2px; background: #e2e8f0; transition: background 0.2s; }
.strength-seg.active.weak   { background: #ef4444; }
.strength-seg.active.fair   { background: #f97316; }
.strength-seg.active.good   { background: #eab308; }
.strength-seg.active.strong { background: #22c55e; }

/* ── Buttons ── */
.register-btn { 
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
.register-btn:hover:not(:disabled) { background: #3f67b0; }
.register-btn:disabled { opacity: 0.6; cursor: not-allowed; }

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
.login-link { margin-top: 20px; font-size: 14px; }
</style>