<template>

<div>

<h2>Placement Drives</h2>

<table>

<thead>
<tr>
<th>Company</th>
<th>Job</th>
<th>Package</th>
<th>Status</th>
<th>Action</th>
</tr>
</thead>

<tbody>

<tr v-for="d in drives" :key="d.id">

<td>{{ d.company }}</td>
<td>{{ d.job_title }}</td>
<td>{{ d.package }}</td>
<td>{{ d.status }}</td>

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

import API from "../../utils/api.js"

export default{

data(){
return{
drives:[]
}
},

async mounted(){

const res = await API.get("/admin/drives")

this.drives = res.data

},

methods:{

async approve(id){

await API.put(`/admin/drive/${id}/approve`)

location.reload()

},

async reject(id){

await API.put(`/admin/drive/${id}/reject`)

location.reload()

}

}

}

</script>