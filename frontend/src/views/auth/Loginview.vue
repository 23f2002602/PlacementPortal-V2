<template>

<div class="login-container">

  <div class="login-card">

    <h1 class="title">Placement Portal</h1>

    <div class="form-group">
      <label>Email</label>
      <input
        v-model="email"
        type="email"
        placeholder="Enter your email"
      />
    </div>

    <div class="form-group">
      <label>Password</label>
      <input
        v-model="password"
        type="password"
        placeholder="Enter your password"
      />
    </div>

    <button class="login-btn" @click="login">
      Login
    </button>

  </div>

</div>

</template>

<script>
import API from "@/utils/api"

export default {

  data() {
    return {
      email: "",
      password: ""
    }
  },

  methods: {

    async login() {

      try {

        const res = await API.login({
          email: this.email,
          password: this.password
        })

        const data = res.data

        localStorage.setItem("ppa_token", data.token)
        localStorage.setItem("role", data.role)

        this.$router.push("/admin")

      } catch (err) {

        console.error(err)
        alert("Login failed")

      }

    }

  }

}
</script>

<style scoped>

/* -------- PAGE -------- */

.login-container{
  height:100vh;
  display:flex;
  justify-content:center;
  align-items:center;
  background:radial-gradient(circle at top,#1e293b,#020617);
  font-family:'Inter',sans-serif;
}

/* -------- CARD -------- */

.login-card{
  width:380px;
  padding:40px;
  border-radius:16px;

  background:#020617;

  border:1px solid #1e293b;

  display:flex;
  flex-direction:column;
  gap:18px;

  box-shadow:0 20px 40px rgba(0,0,0,0.4);
}

/* -------- TITLE -------- */

.title{
  text-align:center;
  font-size:26px;
  font-weight:700;
  margin-bottom:10px;
  color:white;
}

/* -------- FORM -------- */

.form-group{
  display:flex;
  flex-direction:column;
  gap:6px;
}

label{
  font-size:14px;
  color:#94a3b8;
}

/* -------- INPUT -------- */

input{
  padding:12px;
  border-radius:8px;

  border:1px solid #334155;

  background:#0f172a;

  color:white;

  font-size:14px;
}

input:focus{
  outline:none;
  border-color:#6366f1;
}

/* -------- BUTTON -------- */

.login-btn{
  margin-top:10px;

  padding:12px;

  border:none;

  border-radius:8px;

  background:linear-gradient(135deg,#6366f1,#7c3aed);

  color:white;

  font-weight:600;

  cursor:pointer;

  transition:0.2s;
}

.login-btn:hover{
  opacity:0.9;
}

</style>