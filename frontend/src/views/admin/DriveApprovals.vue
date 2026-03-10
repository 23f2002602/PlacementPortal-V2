<template>
<div class="container">

<h2>Drive Approvals</h2>

<table>
<thead>
<tr>
<th>Company</th>
<th>Role</th>
<th>Action</th>
</tr>
</thead>

<tbody>
<tr v-for="d in drives" :key="d.id">
<td>{{d.company}}</td>
<td>{{d.title}}</td>
<td>
<button @click="approve(d.id)">Approve</button>
<button @click="reject(d.id)">Reject</button>
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

 const res = await API.get("/admin/drives/pending")

 this.drives = res.data

 },

 methods:{

 async approve(id){

 await API.put(`/admin/drive/${id}/approve`)

 alert("Drive Approved")

 location.reload()

 },

 async reject(id){

 await API.put(`/admin/drive/${id}/reject`)

 alert("Drive Rejected")

 location.reload()

 }

 }

}
</script>