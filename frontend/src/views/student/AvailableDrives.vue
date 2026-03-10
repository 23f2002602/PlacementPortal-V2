<template>
<div class="container">
<h2>Available Drives</h2>

<table>
<thead>
<tr>
<th>Company</th>
<th>Role</th>
<th>Status</th>
<th>Action</th>
</tr>
</thead>

<tbody>
<tr v-for="d in drives" :key="d.id">
<td>{{d.company}}</td>
<td>{{d.title}}</td>
<td>{{d.status}}</td>
<td>
<button v-if="d.status==='open'" @click="apply(d.id)">
Apply
</button>
</td>
</tr>
</tbody>
</table>

</div>
</template>

<script>
import API from "@/utils/api"

export default{

 data(){
 return{drives:[]}
 },

 async mounted(){
 const res = await API.get("/student/drives")
 this.drives = res.data
 },

 methods:{

 async apply(id){

 await API.post(`/student/apply/${id}`)

 alert("Applied")

 }

 }

}
</script>