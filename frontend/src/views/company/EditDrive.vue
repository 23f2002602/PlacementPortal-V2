<template>
  <div class="container py-4">
    <div class="card bg-card-dark border-theme shadow-lg">
      <div class="card-body p-4">
        <h2 class="text-royal fw-bold mb-4">Edit Placement Drive</h2>
        <form v-if="form" @submit.prevent="update">
          <div class="row g-3">
            <div class="col-md-12">
              <label class="form-label text-muted-light small fw-bold text-uppercase">Job Title</label>
              <input v-model="form.job_title" class="form-control bg-dark-input text-white border-theme" required />
            </div>
            <div class="col-md-12">
              <label class="form-label text-muted-light small fw-bold text-uppercase">Description</label>
              <textarea v-model="form.job_description" class="form-control bg-dark-input text-white border-theme" rows="4"></textarea>
            </div>
            <div class="col-md-6">
              <label class="form-label text-muted-light small fw-bold text-uppercase">Location</label>
              <input v-model="form.location" class="form-control bg-dark-input text-white border-theme" />
            </div>
            <div class="col-md-6">
              <label class="form-label text-muted-light small fw-bold text-uppercase">Package (LPA)</label>
              <input v-model="form.package" type="number" step="0.1" class="form-control bg-dark-input text-white border-theme" required />
            </div>
            <div class="col-md-4">
              <label class="form-label text-muted-light small fw-bold text-uppercase">Min CGPA</label>
              <input v-model="form.min_cgpa" type="number" step="0.1" class="form-control bg-dark-input text-white border-theme" />
            </div>
            <div class="col-md-8">
              <label class="form-label text-muted-light small fw-bold text-uppercase">Eligible Branches</label>
              <input v-model="form.eligible_branches" class="form-control bg-dark-input text-white border-theme" placeholder="e.g., CSE, IT" />
            </div>
            <div class="col-md-6">
              <label class="form-label text-muted-light small fw-bold text-uppercase">Deadline</label>
              <input v-model="form.deadline" type="date" class="form-control bg-dark-input text-white border-theme" />
            </div>
            <div class="col-md-6">
              <label class="form-label text-muted-light small fw-bold text-uppercase">Status</label>
              <select v-model="form.status" class="form-select bg-dark-input text-white border-theme">
                <option value="open">Open</option>
                <option value="closed">Closed</option>
              </option>
            </div>
            <div class="col-md-12 text-end mt-4">
              <button type="button" @click="$router.back()" class="btn btn-outline-secondary me-2">Cancel</button>
              <button type="submit" class="btn btn-royal px-4">Save Changes</button>
            </div>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import API from "../../utils/api.js"

export default {
  data() {
    return { form: null };
  },
  async mounted() {
    const res = await API.get(`/company/drive/${this.$route.params.id}`);
    this.form = res.data;
    if(this.form.deadline) this.form.deadline = this.form.deadline.split(' ')[0];
  },
  methods: {
    async update() {
      try {
        await API.put(`/company/drive/${this.$route.params.id}/update`, this.form);
        alert("Drive updated successfully!");
        this.$router.push("/company");
      } catch (err) {
        alert("Failed to update drive");
      }
    }
  }
}
</script>

<style scoped>
.bg-card-dark { background-color: #1e1e1e !important; }
.bg-dark-input { background-color: #121212 !important; }
.border-theme { border: 1px solid #2c2c2c !important; }
.text-royal { color: #7c4dff !important; }
.text-muted-light { color: #a0a0a0 !important; }
.btn-royal { background: linear-gradient(135deg, #7c4dff, #6200ea); color: white; border: none; }
</style>