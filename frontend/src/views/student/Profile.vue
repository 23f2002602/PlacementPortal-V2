<template>
  <div class="container py-4">
    <div class="row g-4">
      <div class="col-lg-8">
        <div class="card shadow-sm border-0">
          <div class="card-header bg-primary text-white py-3">
            <h4 class="mb-0 fw-bold">Personal Profile</h4>
          </div>
          <div class="card-body p-4">
            <form v-if="profile" @submit.prevent="updateProfile">
              <div class="row g-3">
                <div class="col-md-6">
                  <label class="form-label fw-bold small text-muted text-uppercase">Full Name</label>
                  <input type="text" class="form-control" v-model="profile.name" disabled>
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold small text-muted text-uppercase">Email</label>
                  <input type="email" class="form-control" v-model="profile.email" disabled>
                </div>
                <div class="col-md-4">
                  <label class="form-label fw-bold small text-muted text-uppercase">Roll Number</label>
                  <input type="text" class="form-control" v-model="profile.roll_number">
                </div>
                <div class="col-md-4">
                  <label class="form-label fw-bold small text-muted text-uppercase">Branch</label>
                  <input type="text" class="form-control" v-model="profile.branch">
                </div>
                <div class="col-md-4">
                   <label class="form-label fw-bold small text-muted text-uppercase">Year</label>
                   <input type="number" class="form-control" v-model="profile.year">
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold small text-muted text-uppercase">CGPA</label>
                  <input type="number" step="0.01" class="form-control" v-model="profile.cgpa">
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold small text-muted text-uppercase">Phone</label>
                  <input type="text" class="form-control" v-model="profile.phone">
                </div>
                <div class="col-12">
                  <label class="form-label fw-bold small text-muted text-uppercase">Skills</label>
                  <textarea class="form-control" v-model="profile.skills" rows="2" placeholder="e.g. Python, VueJS, SQL"></textarea>
                </div>
                <div class="col-12">
                  <label class="form-label fw-bold small text-muted text-uppercase">Experience</label>
                  <textarea class="form-control" v-model="profile.experience" rows="3" placeholder="Past internships or projects"></textarea>
                </div>
                <div class="col-12">
                  <label class="form-label fw-bold small text-muted text-uppercase">Resume (PDF)</label>
                  <div class="input-group">
                    <input type="file" class="form-control" @change="onFileChange" accept=".pdf">
                  </div>
                  <div v-if="profile.resume" class="mt-2 small text-muted">
                     Current: <a :href="`/uploads/${profile.resume}`" target="_blank">{{ profile.resume }}</a>
                  </div>
                </div>
              </div>
              <div class="mt-4 text-end">
                <button type="submit" class="btn btn-primary px-5 fw-bold" :disabled="loading">
                   {{ loading ? 'Saving...' : 'Update Details' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
      
      <!-- Placement History Sidebar -->
      <div class="col-lg-4">
        <div class="card shadow-sm border-0 h-100">
           <div class="card-header bg-success text-white py-3">
              <h4 class="mb-0 fw-bold">Placement History</h4>
           </div>
           <div class="card-body p-4">
              <div v-if="history.length > 0">
                 <div v-for="p in history" :key="p.id" class="p-3 mb-3 border rounded-3 bg-light">
                    <h6 class="fw-bold mb-1">{{ p.company }}</h6>
                    <p class="small text-muted mb-2">{{ p.position }}</p>
                    <div class="d-flex justify-content-between align-items-center">
                       <span class="badge bg-success">₹{{ p.salary }} LPA</span>
                       <small class="text-muted">{{ p.placed_on }}</small>
                    </div>
                 </div>
              </div>
              <div v-else class="text-center py-5 text-muted">
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
