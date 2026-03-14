import { createRouter, createWebHistory } from 'vue-router'
import Inbox from '../views/inbox.vue'
import Today from '../views/today.vue'
import Upcoming from '../views/upcoming.vue'
import Calendar from '../views/calendar.vue'
import plan from '../views/plan.vue'
import Completed from '../views/completed.vue'
import Project from '../views/project.vue'
import Login from "../views/login.vue"
import Signup from "../views/register.vue"
import overview from '../views/overview.vue'
import Corporate from '@/views/corporate.vue'
import Settings from '@/views/settings.vue'

const routes = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'Inbox',
            component: Inbox
        },
        {
            path: '/today',
            name: 'Today',
            component: Today
        },
        {
            path: '/upcoming',
            name: 'Upcoming',
            component: Upcoming
        },
        {
            path: '/calendar',
            name: 'Calendar',
            component: Calendar
        },
        {
            path: '/plan',
            name: 'Plan',
            component: plan
        },
        {
            path: '/completed',
            name: 'Completed',
            component: Completed
        },
        {
            path: '/project/:id',
            name: 'Project',
            component: Project
        },
        {
            path: "/login",
            component: Login
        },
        {
            path: "/signup",
            component: Signup
        },
        {
            path: '/overview',
            name: 'Overview',
            component: overview
        },

        {   path: '/corporate/:id',
            name: 'Corporate',
            component: Corporate },
        {
            path: '/settings',
            name: 'Settings',
            component: Settings
        }
    ]
})

// none token → redirect go to /login

// [Checklist: มีการให้ login และ protect routing อย่างเหมาะสม (Y)]
// ส่วนนี้คือ Router Guard (beforeEach) ก่อนจะเรนเดอร์เนื้อหาใดๆ
// การทำงาน: จะตรวจสอบทุกครั้งว่ามีเซสชั่น/Token ในระบบหรือไม่
// ถ้าไม่มีค่า Token ใน localStorage และหน้าที่พยายามจะไปดันไม่ใช่หน้า Login หรือ Signup
// ตัวแอปจะ Reject และดีดกลับมาหน้า Login ทันที เพื่อป้องกันการเข้าถึงจากผู้ที่ไม่ได้รับอนุญาต
routes.beforeEach((to, from, next) => {
    // Google OAuth callback:
    const urlToken = to.query.token
    if (urlToken) {
        // [Checklist: ในการเก็บ token/session เลือกใช้ cookie/local storage -> เลือกใช้ Local Storage]
        // ทำการเก็บ Web Token ไว้ใน Local Storage ของเบราว์เซอร์ เพื่อใช้อ้างอิงการยืนยันตัวตนใน Session การใช้งาน
        localStorage.setItem('token', urlToken)
        return next({ path: '/', replace: true })
    }

    const token = localStorage.getItem('token')
    const publicRoutes = ['/login', '/signup']

    if (!publicRoutes.includes(to.path) && !token) {
        next('/login')
    } else {
        next()
    }
})


export default routes   