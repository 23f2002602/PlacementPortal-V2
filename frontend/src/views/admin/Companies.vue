<template>

<div>

<h2>Companies</h2>

<table>

<thead>
<tr>
<th>Company</th>
<th>Industry</th>
<th>Status</th>
<th>Actions</th>
</tr>
</thead>

<tbody>

<tr v-for="c in companies" :key="c.id">
<td>{{ c.company_name }}</td>
<td>{{ c.industry }}</td>
<td>{{ c.approval_status }}</td>

<td>
<button @click="approve(c.id)">Approve</button>
<button @click="reject(c.id)">Reject</button>
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
companies:[]
}
},

async mounted(){

const res = await API.get("/admin/companies")

this.companies = res.data

},

methods:{

async approve(id){

await API.put(`/admin/company/${id}/approve`)

location.reload()

},

async reject(id){

await API.put(`/admin/company/${id}/reject`)

location.reload()

}

}

}

</script>