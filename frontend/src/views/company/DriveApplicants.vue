<template>

<div class="container">

<h2>Applicants</h2>

<table>
<tr>
<th>Name</th>
<th>Email</th>
<th>Status</th>
<th>Action</th>
</tr>

<tr v-for="a in applicants" :key="a.id">
<td>{{a.student}}</td>
<td>{{a.email}}</td>
<td>{{a.status}}</td>

<td>
<button @click="accept(a.id)">Accept</button>
<button @click="reject(a.id)">Reject</button>
</td>

</tr>

</table>

</div>

</template>

<script>
import API from "@/utils/api"

export default{

 data(){
 return{applicants:[]}
 },

 async mounted(){

 const id = this.$route.params.id

 const res = await API.get(`/company/drive/${id}/applications`)

 this.applicants = res.data

 },

 methods:{

 async accept(id){

 await API.put(`/company/application/${id}/accept`)

 location.reload()

 },

 async reject(id){

 await API.put(`/company/application/${id}/reject`)

 location.reload()

 }

 }

}
</script>