<template>
<div class="container">

<h2>Company Approvals</h2>

<table>
<thead>
<tr>
<th>Company</th>
<th>Email</th>
<th>Action</th>
</tr>
</thead>

<tbody>
<tr v-for="c in companies" :key="c.id">
<td>{{c.company_name}}</td>
<td>{{c.email}}</td>
<td>
<button @click="approve(c.id)">Approve</button>
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
 return{companies:[]}
 },

 async mounted(){

 const res = await API.get("/admin/companies/pending")

 this.companies = res.data

 },

 methods:{

 async approve(id){

 await API.put(`/admin/company/${id}/approve`)

 alert("Company Approved")

 location.reload()

 }

 }

}
</script>

<style>
.container{
padding:40px;
color:white;
background:#020617;
min-height:100vh;
}

table{
width:100%;
border-collapse:collapse;
}

th,td{
padding:12px;
border-bottom:1px solid #1e293b;
}

button{
padding:8px 12px;
background:#2563eb;
border:none;
border-radius:6px;
color:white;
}
</style>