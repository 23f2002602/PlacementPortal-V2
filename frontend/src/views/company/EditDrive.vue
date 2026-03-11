<template>
  <div class="container py-4">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card border-0 shadow-sm">
          <div class="card-body p-4">
            <h2 class="text-primary fw-bold mb-4">Edit Placement Drive</h2>
            <form v-if="form" @submit.prevent="update">
              <div class="row g-3">
                <div class="col-md-12">
                  <label class="form-label fw-bold small text-muted text-uppercase">Job title</label>
                  <input v-model="form.job_title" class="form-control" required />
                </div>
                <div class="col-md-12">
                  <label class="form-label fw-bold small text-muted text-uppercase">Job Description</label>
                  <textarea v-model="form.job_description" class="form-control" rows="3"></textarea>
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold small text-muted text-uppercase">Location</label>
                  <input v-model="form.location" class="form-control" />
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold small text-muted text-uppercase">Package (LPA)</label>
                  <input v-model="form.package" type="number" step="0.1" class="form-control" required />
                </div>
                <div class="col-md-4">
                  <label class="form-label fw-bold small text-muted text-uppercase">Min CGPA</label>
                  <input v-model="form.min_cgpa" type="number" step="0.1" class="form-control" />
                </div>
                <div class="col-md-8">
                  <label class="form-label fw-bold small text-muted text-uppercase">Eligible Branches</label>
                  <input v-model="form.eligible_branches" class="form-control" />
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold small text-muted text-uppercase">Eligible Years</label>
                  <input v-model="form.eligible_years" class="form-control" />
                </div>
                <div class="col-md-6">
                  <label class="form-label fw-bold small text-muted text-uppercase">Application Deadline</label>
                  <input v-model="form.deadline" type="date" class="form-control" required />
                </div>
                <div class="col-md-12 mt-4 text-end">
                  <button type="button" @click="$router.push('/company')" class="btn btn-light me-2">Cancel</button>
                  <button type="submit" class="btn btn-primary px-4">Save Changes</button>
                </div>
              </div>
            </form>
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
      form: null
    }
  },
  async mounted() {
    this.fetchDrive();
  },
  methods: {
    async fetchDrive() {
      const id = this.$route.params.id;
      const res = await API.get(`/company/drive/${id}`);
      this.form = res.data;
    },
    async update() {
      try {
        const id = this.$route.params.id;
        await API.put(`/company/drive/${id}/update`, this.form);
        alert("Drive updated successfully!");
        this.$router.push("/company");
      } catch (err) {
        alert("Failed to update drive");
      }
    }
  }
}
</script>
