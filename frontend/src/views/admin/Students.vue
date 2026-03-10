<template>

<div>

<h2>Students</h2>

<table>

<thead>
<tr>
<th>Name</th>
<th>Email</th>
<th>Roll</th>
<th>Branch</th>
<th>CGPA</th>
</tr>
</thead>

<tbody>

<tr v-for="s in students" :key="s.id">
<td>{{ s.name }}</td>
<td>{{ s.email }}</td>
<td>{{ s.roll_number }}</td>
<td>{{ s.branch }}</td>
<td>{{ s.cgpa }}</td>
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
students:[]
}
},

async mounted(){

const res = await API.get("/admin/students")

this.students = res.data

}

}

</script>