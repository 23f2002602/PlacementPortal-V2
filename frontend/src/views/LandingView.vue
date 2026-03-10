<template>
<div class="landing">

  <div class="hero">

    <h1>Placement Portal</h1>

    <p>Institute Placement Management System</p>

    <div class="actions">

      <router-link to="/login" class="btn">
        Admin Login
      </router-link>

      <router-link to="/login" class="btn">
        Student / Company Login
      </router-link>

      <router-link to="/register-student" class="btn">
        Register as Student
      </router-link>

      <router-link to="/register-company" class="btn">
        Register as Company
      </router-link>

    </div>

  </div>

</div>
</template>

<style>

.landing{
  height:100vh;
  display:flex;
  align-items:center;
  justify-content:center;
  background:linear-gradient(135deg,#020617,#0f172a);
  color:white;
}

.hero{
  text-align:center;
}

.actions{
  margin-top:30px;
  display:flex;
  gap:15px;
  flex-wrap:wrap;
  justify-content:center;
}

.btn{
  padding:12px 20px;
  border-radius:8px;
  background:#2563eb;
  color:white;
  text-decoration:none;
}

</style>