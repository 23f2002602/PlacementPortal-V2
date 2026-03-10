<template>

<div class="container">

<h2>Create Drive</h2>

<input v-model="title" placeholder="Job Title" />
<input v-model="location" placeholder="Location" />
<input v-model="salary" placeholder="Salary" />

<button @click="create">Create</button>

</div>

</template>

<script>
import API from "@/utils/api"

export default{

 data(){
 return{
 title:"",
 location:"",
 salary:""
 }
 },

 methods:{

 async create(){

 await API.post("/company/drive/create",{

 job_title:this.title,
 location:this.location,
 salary:this.salary

 })

 alert("Drive created")

 }

 }

}
</script>