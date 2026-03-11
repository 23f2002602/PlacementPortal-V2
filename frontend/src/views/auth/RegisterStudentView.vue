<template>
<div class="register-student-page">
  <PublicNavbar />
  <div class="page-content">
    <div class="card">
      <h2>Student Registration</h2>
      <input v-model="form.name" placeholder="Name" required />
      <input v-model="form.email" type="email" placeholder="Email" required />
      <input v-model="form.password" type="password" placeholder="Password" required />
      <input v-model="form.roll_number" placeholder="Roll Number" required />
      <input v-model="form.branch" placeholder="Branch" required />
      <input v-model="form.cgpa" type="number" step="0.01" placeholder="CGPA" required />
      <input v-model="form.year" type="number" placeholder="Year" required />
      
      <div class="file-group">
        <label>Resume (PDF)</label>
        <input type="file" @change="handleFile" accept=".pdf" required />
      </div>

      <button @click="register">Register</button>
      <router-link to="/login" class="login-link">Already have an account? Login</router-link>
    </div>
  </div>
</div>
</template>

<script>
import API from "@/utils/api"
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
        roll_number: "",
        branch: "",
        cgpa: "",
        year: "",
        role: "student"
      },
      resume: null
    }
  },
  methods: {
    handleFile(e) {
      this.resume = e.target.files[0]
    },
    async register() {
      if (!this.resume) return alert("Resume is required")
      
      const formData = new FormData()
      for (const key in this.form) {
        formData.append(key, this.form[key])
      }
      formData.append("resume", this.resume)

      try {
        await API.register(formData, true)
        alert("Registered Successfully! You can now login.")
        this.$router.push("/login")
      } catch (err) {
        alert(err.response?.data?.error || "Registration failed")
      }
    }
  }
}
</script>

<style scoped>
.register-student-page {
  min-height: 100vh;
  background: #020617;
}
.page-content {
  height: calc(100vh - 72px);
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Inter', sans-serif;
}

.card {
  background: #0f172a;
  padding: 40px;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 480px;
  color: white;
  border: 1px solid #1e293b;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  font-weight: 700;
  letter-spacing: -0.025em;
}

input {
  padding: 12px;
  border-radius: 8px;
  border: 1px solid #334155;
  background: #020617;
  color: white;
}

.file-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-size: 0.9em;
  color: #94a3b8;
}

button {
  padding: 12px;
  background: linear-gradient(135deg, #6366f1, #7c3aed);
  border: none;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  cursor: pointer;
  margin-top: 10px;
}

.login-link {
  color: #94a3b8;
  text-align: center;
  font-size: 0.85em;
  text-decoration: none;
}
</style>