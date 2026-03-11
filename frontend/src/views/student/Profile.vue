<template>
  <div class="container py-4">
    <div class="row g-4">
      <div class="col-lg-8">
        <div class="card shadow-lg border-theme bg-card-dark">
          <div class="card-header bg-royal-grad text-white py-3">
            <h4 class="mb-0 fw-bold">Personal Profile</h4>
          </div>
          <div class="card-body p-4">
            <form v-if="profile" @submit.prevent="updateProfile">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label text-muted-light small text-uppercase fw-bold">Full Name</label>
                  <input type="text" class="form-control bg-dark-input text-white border-theme" v-model="profile.name" disabled>
                </div>
                <div class="col-md-6">
                  <label class="form-label text-muted-light small text-uppercase fw-bold">Email</label>
                  <input type="email" class="form-control bg-dark-input text-white border-theme" v-model="profile.email" disabled>
                </div>
                <div class="col-md-4">
                  <label class="form-label text-muted-light small text-uppercase fw-bold">Roll Number</label>
                  <input type="text" class="form-control bg-dark-input text-white border-theme" v-model="profile.roll_number">
                </div>
                <div class="col-md-4">
                  <label class="form-label text-muted-light small text-uppercase fw-bold">Branch</label>
                  <input type="text" class="form-control bg-dark-input text-white border-theme" v-model="profile.branch">
                </div>
                <div class="col-md-4">
                   <label class="form-label text-muted-light small text-uppercase fw-bold">Year</label>
                   <input type="number" class="form-control bg-dark-input text-white border-theme" v-model="profile.year">
                </div>
                <div class="col-md-6">
                  <label class="form-label text-muted-light small text-uppercase fw-bold">CGPA</label>
                  <input type="number" step="0.01" class="form-control bg-dark-input text-white border-theme" v-model="profile.cgpa">
                </div>
                <div class="col-md-6">
                  <label class="form-label text-muted-light small text-uppercase fw-bold">Phone</label>
                  <input type="text" class="form-control bg-dark-input text-white border-theme" v-model="profile.phone">
                </div>
                <div class="col-12">
                  <label class="form-label text-muted-light small text-uppercase fw-bold">Skills</label>
                  <textarea class="form-control bg-dark-input text-white border-theme" v-model="profile.skills" rows="2" placeholder="e.g. Python, VueJS, SQL"></textarea>
                </div>
                <div class="col-12">
                  <label class="form-label text-muted-light small text-uppercase fw-bold">Experience</label>
                  <textarea class="form-control bg-dark-input text-white border-theme" v-model="profile.experience" rows="3" placeholder="Past internships or projects"></textarea>
                </div>
                <div class="col-12">
                  <label class="form-label text-muted-light small text-uppercase fw-bold">Resume (PDF)</label>
                  <input type="file" class="form-control bg-dark-input text-white border-theme" @change="onFileChange" accept=".pdf">
                  <div v-if="profile.resume" class="mt-2 small text-muted-light">
                     Current: <a :href="`/uploads/${profile.resume}`" target="_blank" class="text-royal">{{ profile.resume }}</a>
                  </div>
                </div>
              </div>
              <div class="mt-4 text-end">
                <button type="submit" class="btn btn-royal px-5 fw-bold" :disabled="loading">
                   {{ loading ? 'Saving...' : 'Update Details' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
      
      <div class="col-lg-4">
        <div class="card shadow-lg border-theme bg-card-dark h-100">
           <div class="card-header bg-success text-white py-3">
              <h4 class="mb-0 fw-bold">Placement History</h4>
           </div>
           <div class="card-body p-4">
              <div v-if="history.length > 0">
                 <div v-for="p in history" :key="p.id" class="p-3 mb-3 border-theme rounded-3 bg-dark-input">
                    <h6 class="fw-bold mb-1 text-white">{{ p.company }}</h6>
                    <p class="small text-muted-light mb-2">{{ p.position }}</p>
                    <div class="d-flex justify-content-between align-items-center">
                       <span class="badge bg-success">₹{{ p.salary }} LPA</span>
                       <small class="text-muted-light">{{ p.placed_on }}</small>
                    </div>
                 </div>
              </div>
              <div v-else class="text-center py-5 text-muted-light">
                 <i class="bi bi-person-check fs-1"></i>
                 <p class="mt-2">No placement records found yet.</p>
              </div>
           </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import API from "../../utils/api.js"

export default {
  data() {
    return {
      profile: null,
      history: [],
      resumeFile: null,
      loading: false
    };
  },
  async mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      const [prof, hist] = await Promise.all([
        API.get('/student/profile'),
        API.get('/student/history')
      ]);
      this.profile = prof.data;
      this.history = hist.data;
    },
    onFileChange(e) {
      this.resumeFile = e.target.files[0];
    },
    async updateProfile() {
      this.loading = true;
      const formData = new FormData();
      Object.keys(this.profile).forEach(key => {
        if (this.profile[key] !== null && key !== 'resume') {
           formData.append(key, this.profile[key]);
        }
      });
      if (this.resumeFile) formData.append('resume', this.resumeFile);

      try {
        await API.put('/student/profile/update', formData);
        alert('Profile updated successfully!');
        this.fetchData();
      } catch (err) {
        alert('Error updating profile');
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>

<style scoped>
/* Admin-style Theme Colors */
.bg-card-dark { background-color: #1e1e1e !important; }
.bg-dark-input { background-color: #121212 !important; }
.border-theme { border: 1px solid #2c2c2c !important; }
.text-royal { color: #7c4dff !important; }
.text-muted-light { color: #a0a0a0 !important; }
.bg-royal-grad { background: linear-gradient(135deg, #7c4dff, #6200ea) !important; }
.btn-royal { background: var(--bg-royal-grad); color: white; border: none; }

/* Admin-style Table Styling */
.table-dark-custom { color: #f1f5f9; background-color: #1e1e1e; }
.table-dark-custom thead th { 
  background-color: #252525; 
  color: #7c4dff; 
  text-transform: uppercase; 
  font-size: 0.75rem; 
  border-bottom: 2px solid #2c2c2c;
  padding: 12px 16px;
}
.table-dark-custom td { 
  padding: 12px 16px; 
  border-bottom: 1px solid #2c2c2c; 
  background-color: #1e1e1e;
}
</style>