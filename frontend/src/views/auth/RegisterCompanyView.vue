<template>
<div class="register-company-page">
  <PublicNavbar />
  <div class="page-content">
    <div class="register-card shadow-lg">
      <h2 class="title">Company Registration</h2>
      <p class="subtitle">Partner with us for recruitment</p>

      <div class="form-wrapper">
        <div class="form-grid">
          <label class="form-label">HR Contact Name</label>
          <input v-model="form.name" placeholder="Enter name" required />
          
          <label class="form-label">HR Professional Email</label>
          <input v-model="form.email" type="email" placeholder="hr@company.com" required />
          
          <label class="form-label">Password</label>
          <input v-model="form.password" type="password" placeholder="Password" required />
          
          <label class="form-label">Company Name</label>
          <input v-model="form.company_name" placeholder="Legal entity name" required />
          
          <label class="form-label">Company Description</label>
          <textarea v-model="form.description" rows="3" placeholder="Tell us about your organization"></textarea>
        </div>
      </div>

      <button @click="register" class="register-submit-btn">Register Company</button>
      
      <div class="auth-footer text-center mt-4">
        <span class="footer-text">Already a partner?</span>
        <router-link to="/login" class="auth-link ms-2">Login Here</router-link>
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
      form: {
        name: "", email: "", password: "", company_name: "",
        industry: "", location: "", website: "", description: "", role: "company"
      }
    }
  },
  methods: {
    async register() {
      try {
        await API.register(this.form);
        alert("Registration successful! Pending admin approval.");
        this.$router.push("/login");
      } catch (err) {
        alert(err.response?.data?.error || "Registration failed");
      }
    }
  }
}
</script>

<style scoped>
.register-company-page {
  min-height: 100vh;
  background: #020617;
  overflow-y: auto;
}

.page-content {
  padding: 110px 20px 60px; /* Ensures forms are visible below navbar */
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.register-card {
  width: 100%;
  max-width: 500px;
  padding: 40px;
  border-radius: 20px;
  background: #0f172a;
  border: 1px solid #1e293b;
}

.title { text-align: center; color: white; font-weight: 700; margin-bottom: 5px; }
.subtitle { text-align: center; color: #94a3b8; font-size: 14px; margin-bottom: 30px; }

.form-label { font-size: 13px; font-weight: 600; color: #cbd5e1; margin-bottom: 8px; display: block; }

input, textarea {
  width: 100%; padding: 12px; border-radius: 10px; border: 1px solid #334155;
  background: #020617; color: white; margin-bottom: 15px;
}

.register-submit-btn {
  width: 100%; padding: 14px; border: none; border-radius: 12px;
  background: linear-gradient(135deg, #6366f1, #7c3aed); color: white;
  font-weight: 700; cursor: pointer;
}

.footer-text { color: #e2e8f0; font-size: 14px; }
.auth-link { color: #818cf8; text-decoration: none; font-weight: 600; }
</style>