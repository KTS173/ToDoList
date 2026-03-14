<script setup>
import MonthCalendar from "../components/MonthCalendar.vue"
import { ref, onMounted } from "vue"
import axios from "axios"

const year = ref(2026)

const tasks = ref([])

async function loadTasks(){

const token = localStorage.getItem("token")

const res = await axios.get(
  "http://localhost:8000/api/tasks",
  {
    headers:{
      Authorization:`Bearer ${token}`
    }
  }
)

tasks.value = res.data
}

onMounted(loadTasks)

const months = [
"January","February","March",
"April","May","June",
"July","August","September",
"October","November","December"
]

function nextYear(){
year.value++
}

function prevYear(){
year.value--
}

</script>

<template>

<div class="plan-container">

<div class="header">

  <div>
    <h1 class="title">Year Plan</h1>
    <p class="subtitle">{{ year }} overview</p>
  </div>

  <div class="year-switch">
    <button @click="prevYear">‹</button>
    <button class="year-number">{{ year }}</button>
    <button @click="nextYear">›</button>
  </div>

  <div class="legend">

  <div class="legend-item">
    <span class="legend-circle task1"></span>
    <span>1 task</span>
  </div>

  <div class="legend-item">
    <span class="legend-circle task2"></span>
    <span>2 tasks</span>
  </div>

  <div class="legend-item">
    <span class="legend-circle task3"></span>
    <span>3+ tasks</span>
  </div>

  <div class="legend-item">
    <span class="legend-circle today"></span>
    <span>Today</span>
  </div>

</div>

</div>

<div class="calendar-grid">

<div
v-for="(month,index) in months"
:key="month"
class="month-card"
>

<h3>{{ month }}</h3>

<MonthCalendar
:month="index"
:year="year"
:tasks="tasks"
/>

</div>

</div>

</div>

</template>

<style scoped>

.plan-container{
padding:24px 40px;
padding-bottom:40px;

background:#f7f5f2;

height:100vh;

display:flex;
flex-direction:column;

overflow-y:auto;

font-family:'DM Sans','Segoe UI',sans-serif;
}

.title{
font-size:28px;
font-weight:700;
margin-bottom:4px;
}

.subtitle{
color:#777;
margin-bottom:20px;
}

.calendar-grid{
flex:1;

display:grid;
grid-template-columns:repeat(3,1fr);

gap:18px;

padding-bottom:40px;
}

.month-card{
background:#ffffff;

border:1px solid #e5e5e5;

border-radius:16px;

padding:16px;

display:flex;
flex-direction:column;

box-shadow:0 1px 2px rgba(0,0,0,0.04);
}

.month-card:hover{
box-shadow:0 4px 12px rgba(0,0,0,0.06);
}

.month-card h3{
font-size:15px;
font-weight:600;
margin-bottom:8px;
color:#1a1a1a;
}

.subtitle{
font-size:15px;
font-weight:600;
color:#777;
margin-bottom:20px;
}


.header{
display:flex;
justify-content:space-between;
align-items:center;
margin-bottom:20px;
}

.year-switch{
display:flex;
align-items:center;
gap:12px;
font-weight:600;
}

.year-switch button{
background:transparent;
border:none;

font-size:16px;
font-weight:600;

color:#1a1a1a;

cursor:pointer;

padding:6px 10px;
border-radius:6px;

transition:all 0.15s ease;
}

.year-switch button:hover{
background:#e4e0da;
color:#1a1a1a;
}

.year-switch button:focus{
outline:none;
box-shadow:none;
}

.year-number{
background:#f3f4f6;

border:none;
border-radius:6px;

font-size:16px;
font-weight:600;

color:#555;

padding:6px 14px;

cursor:default;
}

.year-number:hover{
background:#e4e0da;
}

.legend{
display:flex;
gap:20px;
align-items:center;

margin-top:6px;
margin-bottom:20px;

font-size:14px;
color:#555;
}

.legend-item{
display:flex;
align-items:center;
gap:6px;
}

.legend-circle{
width:14px;
height:14px;
border-radius:50%;
}

.legend-circle.task1{
background:#bbf7d0;
}

.legend-circle.task2{
background:#4ade80;
}

.legend-circle.task3{
background:#166534;
}

.legend-circle.today{
border:2px solid #111;
background:transparent;
}

</style>