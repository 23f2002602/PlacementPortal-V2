<template>
<div class="layout">
  <div class="content">
    <router-view/>
  </div>

  <div class="sidebar">
    <h2>Company Portal</h2>
    <nav>
      <router-link to="/company">Our Drives</router-link>
      <router-link to="/company/drives/create">Create Drive</router-link>
      <button @click="logout" class="logout-btn">Logout</button>
    </nav>
  </div>
</div>
</template>

<script>
export default {
  methods: {
    logout() {
      localStorage.removeItem('ppa_token');
      localStorage.removeItem('ppa_role');
      localStorage.removeItem('ppa_name');
      localStorage.removeItem('ppa_user_id');
      this.$router.push('/');
    }
  }
}
</script>

<style>
.layout{
  display:flex;
  min-height:100vh;
  background: #f8fafc;
}

.content{
  flex:1;
  padding:40px;
}

.sidebar{
  width:260px;
  background:#020617;
  padding:30px;
  border-left:1px solid #1e293b;
  color: white;
}

.sidebar h2{
  margin-bottom:30px;
  font-size: 1.5rem;
  font-weight: 700;
}

.sidebar nav{
  display:flex;
  flex-direction:column;
  gap:12px;
}

.sidebar a{
  text-decoration:none;
  color:#94a3b8;
  padding:10px 12px;
  border-radius:8px;
  transition: all 0.2s;
}

.sidebar a:hover {
  background: #1e293b;
  color: white;
}

.sidebar a.router-link-active{
  background:#6366f1;
  color:white;
}

.logout-btn {
  margin-top: 20px;
  background: #ef4444;
  color: white;
  border: none;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  text-align: left;
  transition: background 0.2s;
}

.logout-btn:hover {
  background: #dc2626;
}
</style>
