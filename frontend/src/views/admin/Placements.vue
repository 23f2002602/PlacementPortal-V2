<template>
<div class="container">

<h2>Placements</h2>

<table>
<thead>
<tr>
<th>Student</th>
<th>Company</th>
<th>Position</th>
</tr>
</thead>

<tbody>
<tr v-for="p in placements" :key="p.id">
<td>{{p.student}}</td>
<td>{{p.company}}</td>
<td>{{p.position}}</td>
</tr>
</tbody>
</table>

</div>
</template>

<script>
import API from "@/utils/api"

export default{

 data(){
 return{placements:[]}
 },

 async mounted(){

 const res = await API.get("/admin/placements")

 this.placements = res.data

 }

}
</script>