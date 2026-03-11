<template>
<div class="register-student-page">
  <PublicNavbar />
  <div class="page-content">
    <div class="register-card shadow-lg">
      <h2 class="title">Student Registration</h2>
      <p class="subtitle">Join our placement community</p>

      <div class="form-wrapper">
        <div class="row g-3">
          <div class="col-md-12">
            <label class="form-label">Full Name</label>
            <input v-model="form.name" placeholder="Enter your name" required />
          </div>
          <div class="col-md-6">
            <label class="form-label">Email Address</label>
            <input v-model="form.email" type="email" placeholder="name@email.com" required />
          </div>
          <div class="col-md-6">
            <label class="form-label">Password</label>
            <input v-model="form.password" type="password" placeholder="Password" required />
          </div>
          <div class="col-md-6">
            <label class="form-label">Roll Number</label>
            <input v-model="form.roll_number" placeholder="Roll Number" required />
          </div>
          <div class="col-md-6">
            <label class="form-label">Branch</label>
            <input v-model="form.branch" placeholder="e.g. CSE" required />
          </div>
          <div class="col-md-6">
            <label class="form-label">CGPA</label>
            <input v-model="form.cgpa" type="number" step="0.01" placeholder="Current CGPA" required />
          </div>
          <div class="col-md-6">
            <label class="form-label">Year of Study</label>
            <input v-model="form.year" type="number" placeholder="e.g. 2024" required />
          </div>
          <div class="col-md-12">
            <label class="form-label">Resume (PDF)</label>
            <input type="file" @change="handleFile" accept=".pdf" class="file-input" required />
          </div>
        </div>
      </div>

      <button @click="register" class="register-submit-btn">Create Student Account</button>
      
      <div class="auth-footer text-center mt-4">
        <span class="footer-text">Already have an account?</span>
        <router-link to="/login" class="auth-link ms-2">Login Now</router-link>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import API from "@/utils/api"
import PublicNavbar from '@/components/PublicNavbar.vue'

export default {
  components: { PublicNavbar },
  data() {
    return {
      form: {
        name: "", email: "", password: "", roll_number: "",
        branch: "", cgpa: "", year: "", role: "student"
      },
      resume: null
    }
  },
  methods: {
    handleFile(e) { this.resume = e.target.files[0] },
    async register() {
      if (!this.resume) return alert("Resume is required");
      const formData = new FormData();
      for (const key in this.form) { formData.append(key, this.form[key]); }
      formData.append("resume", this.resume);
      try {
        await API.register(formData, true);
        alert("Registered Successfully!");
        this.$router.push("/login");
      } catch (err) {
        alert(err.response?.data?.error || "Registration failed");
      }
    }
  }
}
</script>

<style scoped>
.register-student-page {
  min-height: 100vh;
  background: #020617;
  overflow-y: auto;
}

.page-content {
  padding: 110px 20px 60px; /* High top padding to avoid navbar overlap */
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

.register-card {
  width: 100%;
  max-width: 550px;
  padding: 40px;
  border-radius: 20px;
  background: #0f172a;
  border: 1px solid #1e293b;
}

.title { text-align: center; color: white; font-weight: 700; margin-bottom: 5px; }
.subtitle { text-align: center; color: #94a3b8; font-size: 14px; margin-bottom: 30px; }

.form-label { font-size: 13px; font-weight: 600; color: #cbd5e1; margin-bottom: 8px; display: block; }

input {
  width: 100%; padding: 12px; border-radius: 10px; border: 1px solid #334155;
  background: #020617; color: white; margin-bottom: 15px;
}

.file-input { background: #1e293b; border: 1px dashed #6366f1; }

.register-submit-btn {
  width: 100%; padding: 14px; border: none; border-radius: 12px;
  background: linear-gradient(135deg, #6366f1, #7c3aed); color: white;
  font-weight: 700; cursor: pointer; transition: 0.2s;
}

.footer-text { color: #e2e8f0; font-size: 14px; }
.auth-link { color: #818cf8; text-decoration: none; font-weight: 600; }
</style>