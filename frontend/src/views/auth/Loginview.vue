<template>
<div class="login-page">
  <PublicNavbar />
  <div class="page-content">
    <div class="login-card shadow-lg">
      <h2 class="title">Access Portal</h2>
      <p class="subtitle">Select your role and enter credentials</p>
      
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

      <div class="form-wrapper">
        <div class="form-group mb-3">
           <label class="form-label">Email Address</label>
           <div class="input-wrapper">
             <i class="bi bi-envelope"></i>
             <input v-model="email" type="email" placeholder="name@example.com" required />
           </div>
        </div>
        
        <div class="form-group mb-4">
           <label class="form-label">Password</label>
           <div class="input-wrapper">
             <i class="bi bi-lock"></i>
             <input v-model="password" type="password" placeholder="Enter password" required />
           </div>
        </div>
      </div>

      <button @click="login" class="login-submit-btn">Continue to Dashboard</button>
      
      <div class="auth-footer text-center mt-4">
        <span class="footer-text">New here?</span>
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
  /* UPDATED: Ensure scrolling is possible */
  overflow-y: auto; 
}

.page-content {
  /* UPDATED: Increased top padding (100px) to clear the navbar and added bottom padding */
  padding: 100px 20px 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.login-card {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  border-radius: 20px;
  background: #0f172a;
  border: 1px solid #1e293b;
  display: flex;
  flex-direction: column;
}

.title {
  text-align: center;
  font-size: 26px;
  font-weight: 700;
  color: white;
  margin-bottom: 5px;
}

.subtitle {
  text-align: center;
  color: #94a3b8;
  font-size: 14px;
  margin-bottom: 30px;
}

.role-btn {
  padding: 10px;
  background: #1e293b;
  border: 1px solid #334155;
  color: #94a3b8;
  border-radius: 10px;
  font-weight: 600;
  transition: 0.2s;
}

.role-btn.active {
  background: #6366f1;
  color: white;
  border-color: #6366f1;
}

.form-label {
  font-size: 13px;
  font-weight: 600;
  color: #cbd5e1;
  margin-bottom: 8px;
  display: block;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper i {
  position: absolute;
  left: 15px;
  color: #64748b;
}

input {
  width: 100%;
  padding: 12px 12px 12px 45px;
  border-radius: 10px;
  border: 1px solid #334155;
  background: #020617;
  color: white;
  transition: 0.2s;
}

.login-submit-btn {
  width: 100%;
  padding: 14px;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #6366f1, #7c3aed);
  color: white;
  font-weight: 700;
  margin-top: 10px;
  cursor: pointer;
  transition: 0.2s;
}

/* UPDATED: Enhanced visibility for "New here?" text */
.footer-text {
  color: #e2e8f0; 
  font-size: 14px;
  font-weight: 500;
}

.auth-link {
  color: #818cf8;
  text-decoration: none;
  font-weight: 600;
}

.vr {
  background-color: #334155;
}
</style>