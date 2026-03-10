<template>

<div class="layout">

  <div class="content">
    <router-view/>
  </div>

  <div class="sidebar">

    <h2>Placement Portal</h2>

    <nav>
      <router-link to="/admin">Dashboard</router-link>
      <router-link to="/admin/students">Students</router-link>
      <router-link to="/admin/companies">Companies</router-link>
      <router-link to="/admin/drives">Drives</router-link>
    </nav>

  </div>

</div>

</template>

<style>

.layout{
  display:flex;
  min-height:100vh;
}

.content{
  flex:1;
  padding:50px;
}

.sidebar{
  width:260px;
  background:#020617;
  padding:30px;
  border-left:1px solid #1e293b;
}

.sidebar h2{
  margin-bottom:30px;
}

.sidebar nav{
  display:flex;
  flex-direction:column;
  gap:12px;
}

.sidebar a{
  text-decoration:none;
  color:#94a3b8;
  padding:8px 10px;
  border-radius:6px;
}

.sidebar a.router-link-active{
  background:#6366f1;
  color:white;
}
</style>