<template>

<div>
<h1>Admin Dashboard</h1>

<div class="dashboard-cards">

  <div class="card">
    <h3>Students</h3>
    <p>{{ stats.students }}</p>
  </div>

  <div class="card">
    <h3>Companies</h3>
    <p>{{ stats.companies }}</p>
  </div>

  <div class="card">
    <h3>Drives</h3>
    <p>{{ stats.drives }}</p>
  </div>

  <div class="card">
    <h3>Placements</h3>
    <p>{{ stats.placements }}</p>
  </div>

</div>

</div>

</template>


<script>

import API from "../../utils/api.js"

export default{

data(){
return{
stats:{
students:0,
companies:0,
drives:0,
placements:0
}
}
},

async mounted(){

const res = await API.get("/admin/stats")

this.stats = res.data

}

}

</script>


<style scoped>

.stats{
display:flex;
gap:20px;
}

.card{
padding:20px;
background:#f4f4f4;
border-radius:10px;
width:150px;
text-align:center;
}

.dashboard-cards{
  display:grid;
  grid-template-columns: repeat(4, minmax(220px,1fr));
  gap:30px;
  margin-top:40px;
  max-width:900px;
}

.card{
  background:white;
  padding:30px;
  border-radius:12px;
  text-align:center;
  box-shadow:0 4px 12px rgba(0,0,0,0.1);
}

.card h3{
  font-size:20px;
  margin-bottom:10px;
  white-space:nowrap;
}

.card p{
  font-size:28px;
  font-weight:bold;
}
</style>