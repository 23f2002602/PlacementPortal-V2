<template>

<div class="container">

<h2>Available Drives</h2>

<table>
<thead>
<tr>
<th>Company</th>
<th>Role</th>
<th>Location</th>
<th>Status</th>
</tr>
</thead>

<tbody>
<tr v-for="d in drives" :key="d.id">
<td>{{d.company}}</td>
<td>{{d.title}}</td>
<td>{{d.location}}</td>
<td>{{d.status}}</td>
</tr>
</tbody>

</table>

</div>

</template>

<script>
import API from "@/utils/api"

export default{

 data(){

 return{
 drives:[]
 }

 },

 async mounted(){

 const res = await API.get("/student/drives")

 this.drives = res.data

 }

}
</script>

<style>
.container{
padding:40px;
color:white;
background:#020617;
height:100vh;
}

table{
width:100%;
border-collapse:collapse;
}

th,td{
padding:12px;
border-bottom:1px solid #1e293b;
}

</style>