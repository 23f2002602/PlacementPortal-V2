<template>

<div class="container">

<h2>My Applications</h2>

<table>
<tr>
<th>Company</th>
<th>Drive</th>
<th>Status</th>
</tr>

<tr v-for="a in apps" :key="a.id">
<td>{{a.company}}</td>
<td>{{a.drive}}</td>
<td>{{a.status}}</td>
</tr>

</table>

</div>

</template>

<script>
import API from "@/utils/api"

export default{

 data(){
 return{apps:[]}
 },

 async mounted(){

 const res = await API.get("/student/applications")

 this.apps = res.data

 }

}
</script>