<template>
<div class="register-company-page">
  <PublicNavbar />
  <div class="page-content">
    <div class="card">
      <h2>Company Registration</h2>
      <div class="form-grid">
        <input v-model="form.name" placeholder="HR Contact Name" required />
        <input v-model="form.email" type="email" placeholder="HR Email" required />
        <input v-model="form.password" type="password" placeholder="Password" required />
        <input v-model="form.company_name" placeholder="Company Name" required />
        <input v-model="form.industry" placeholder="Industry" />
        <input v-model="form.location" placeholder="Location" />
        <input v-model="form.website" placeholder="Website URL" />
        <textarea v-model="form.description" placeholder="Company Description" rows="3"></textarea>
      </div>

      <button @click="register">Register Company</button>
      <router-link to="/login" class="login-link">Already have an account? Login</router-link>
    </div>
  </div>
</div>
</template>

<script>
import API from "../../utils/api.js"
import PublicNavbar from '@/components/PublicNavbar.vue'

export default {
  components: {
    PublicNavbar
  },
  data() {
    return {
      form: {
        name: "",
        email: "",
        password: "",
        company_name: "",
        industry: "",
        location: "",
        website: "",
        description: "",
        role: "company"
      }
    }
  },
  methods: {
    async register() {
      try {
        await API.register(this.form);
        alert("Registration successful! Please wait for admin approval.");
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
}
.page-content {
  min-height: calc(100vh - 72px);
  padding: 40px 20px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Inter', sans-serif;
}

.card {
  background: #0f172a;
  padding: 40px;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  width: 100%;
  max-width: 520px;
  color: white;
  border: 1px solid #1e293b;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

h2 {
  text-align: center;
  margin-bottom: 10px;
  font-weight: 800;
  letter-spacing: -0.03em;
  background: linear-gradient(to right, #6366f1, #a855f7);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.form-grid {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

input, textarea {
  padding: 14px;
  border-radius: 10px;
  border: 1px solid #334155;
  background: #020617;
  color: white;
  transition: all 0.2s;
}

input:focus, textarea:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
}

button {
  padding: 16px;
  background: linear-gradient(135deg, #6366f1, #7c3aed);
  border: none;
  border-radius: 12px;
  color: white;
  font-weight: 700;
  cursor: pointer;
  margin-top: 10px;
  transition: transform 0.2s, opacity 0.2s;
}

button:hover {
  transform: translateY(-2px);
  opacity: 0.95;
}

.login-link {
  color: #94a3b8;
  text-align: center;
  font-size: 0.9em;
  text-decoration: none;
  transition: color 0.2s;
}

.login-link:hover {
  color: #6366f1;
}
</style>