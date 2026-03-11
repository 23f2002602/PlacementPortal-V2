<template>
<div class="login-page">
  <PublicNavbar />
  <div class="page-content">
    <div class="card">
      <h2>Access Portal</h2>
      <p class="text-center text-muted small mb-4">Select your role and enter credentials</p>
      
      <div class="role-selector d-flex gap-2 mb-4">
        <button 
          v-for="r in ['student', 'company', 'admin']" 
          :key="r"
          @click="role = r"
          class="role-btn flex-grow-1 text-capitalize"
          :class="{ active: role === r }"
        >
          {{ r }}
        </button>
      </div>

      <div class="form-grid">
        <div class="input-group-custom">
           <i class="bi bi-envelope"></i>
           <input v-model="email" type="email" placeholder="Email Address" required />
        </div>
        <div class="input-group-custom">
           <i class="bi bi-lock"></i>
           <input v-model="password" type="password" placeholder="Password" required />
        </div>
      </div>

      <button @click="login" class="login-submit-btn">Continue to Dashboard</button>
      
      <div class="auth-footer text-center mt-3">
        <span class="text-muted small">New here?</span>
        <div class="d-flex justify-content-center gap-3 mt-2">
          <router-link to="/register/student" class="auth-link">Student Hub</router-link>
          <div class="vr"></div>
          <router-link to="/register/company" class="auth-link">Company Partner</router-link>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import API from "../../utils/api.js"
import PublicNavbar from '@/components/PublicNavbar.vue'

export default {
  components: { PublicNavbar },
  data() {
    return {
      email: "",
      password: "",
      role: "student"
    }
  },
  methods: {
    async login() {
      try {
        const res = await API.login({ email: this.email, password: this.password, role: this.role });
        localStorage.setItem("ppa_token", res.data.token);
        localStorage.setItem("ppa_role", res.data.role);
        localStorage.setItem("ppa_name", res.data.name);
        localStorage.setItem("ppa_user_id", res.data.user_id);
        
        if (res.data.role === "admin") this.$router.push("/admin");
        else if (res.data.role === "company") this.$router.push("/company");
        else this.$router.push("/student");
      } catch (err) {
        alert(err.response?.data?.error || "Login failed");
      }
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: #020617;
}
.page-content {
  min-height: calc(100vh - 72px);
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Inter', sans-serif;
}
.login-card {
  width: 380px;
  padding: 40px;
  border-radius: 16px;
  background: #020617;
  border: 1px solid #1e293b;
  display: flex;
  flex-direction: column;
  gap: 18px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}
.title {
  text-align: center;
  font-size: 26px;
  font-weight: 700;
  margin-bottom: 10px;
  color: white;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
label {
  font-size: 14px;
  color: #94a3b8;
}
input {
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #334155;
  background: #0f172a;
  color: white;
  font-size: 14px;
}
input:focus {
  outline: none;
  border-color: #6366f1;
}
.login-btn {
  margin-top: 10px;
  padding: 12px;
  border: none;
  border-radius: 8px;
  background: linear-gradient(135deg, #6366f1, #7c3aed);
  color: white;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}
.login-btn:hover {
  opacity: 0.9;
}
</style>