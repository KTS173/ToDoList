<script setup>
import { computed } from "vue"

const props = defineProps({
month: Number,
year: Number,
tasks: Array
})

const emit = defineEmits(["select-date"])

function selectDate(day){
if(!day) return

emit("select-date",{
day: day,
month: props.month,
year: props.year
})
}

const startDay = computed(()=>{
return new Date(props.year,props.month,1).getDay()
})

const totalDays = computed(()=>{
return new Date(props.year,props.month+1,0).getDate()
})

const days = computed(()=>{
const arr=[]

for(let i=0;i<startDay.value;i++){
arr.push("")
}

for(let i=1;i<=totalDays.value;i++){
arr.push(i)
}

return arr
})

function isToday(day){

if(!day) return false

const today=new Date()

return (
today.getDate()===day &&
today.getMonth()===props.month &&
today.getFullYear()===props.year
)

}

function countTasks(day){

if(!day) return 0

const tasks = props.tasks?.filter(task => {

const date = new Date(task.due_date)

return (
date.getDate() === day &&
date.getMonth() === props.month &&
date.getFullYear() === props.year
)

})

return tasks?.length || 0

}

function dayClass(day){

if(!day) return ""

const count = countTasks(day)

return {
today: isToday(day),
task1: count === 1,
task2: count === 2,
task3: count >= 3
}

}

</script>


<template>

<div class="calendar">

<div class="weekdays">

<span>S</span>
<span>M</span>
<span>T</span>
<span>W</span>
<span>T</span>
<span>F</span>
<span>S</span>

</div>

<div class="days">

<span
v-for="(day,index) in days"
:key="index"
:class="dayClass(day)"
@click="selectDate(day)"
>

{{ day || "" }}

</span>

</div>

</div>

</template>


<style scoped>

.calendar{
width:100%;
min-height:200px;
}

.weekdays{
display:grid;
grid-template-columns:repeat(7,1fr);
font-size:14px;
font-weight:700;
letter-spacing:0.08em;
text-transform:uppercase;
color:#999;
margin-bottom:8px;
text-align:center;
}

.days{
display:grid;
grid-template-columns:repeat(7,1fr);
grid-template-rows:repeat(6,1fr);
gap:6px;
text-align:center;
}

.days span{
aspect-ratio:1;

width:26px;
height:26px;

display:flex;
align-items:center;
justify-content:center;

font-size:14px;
font-weight:500;

margin:2px auto;

transition:all 0.15s ease;
}

.today{
border:2px solid #111;

background:transparent;

border-radius:50%;

display:flex;
align-items:center;
justify-content:center;

font-size:13px;
font-weight:500;
}

.selected{
background:#3b82f6;
color:white;
border-radius:50%;
}

.days span:hover{
background:#f1efea;
border-radius:50%;

transform:scale(1.5);
}

.task1{
background:#bbf7d0;
border-radius:50%;
}

.task2{
background:#4ade80;
color:white;
border-radius:50%;
}

.task3{
background:#166534;
color:white;
border-radius:50%;
}

</style>