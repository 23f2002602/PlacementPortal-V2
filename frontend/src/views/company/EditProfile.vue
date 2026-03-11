<template>
  <div class="container py-4">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card border-0 shadow-sm">
          <div class="card-body p-4">
            <h2 class="text-primary fw-bold mb-4">Edit Company Profile</h2>
            <form v-if="form" @submit.prevent="update">
              <div class="mb-3">
                <label class="form-label small fw-bold text-muted text-uppercase">Company Name</label>
                <input v-model="form.company_name" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label small fw-bold text-muted text-uppercase">Industry</label>
                <input v-model="form.industry" class="form-control" />
              </div>
              <div class="mb-3">
                <label class="form-label small fw-bold text-muted text-uppercase">Location</label>
                <input v-model="form.location" class="form-control" />
              </div>
              <div class="mb-3">
                <label class="form-label small fw-bold text-muted text-uppercase">Website</label>
                <input v-model="form.website" class="form-control" />
              </div>
              <div class="mb-3">
                <label class="form-label small fw-bold text-muted text-uppercase">HR Contact</label>
                <input v-model="form.hr_contact" class="form-control" />
              </div>
              <div class="mb-3">
                <label class="form-label small fw-bold text-muted text-uppercase">Description</label>
                <textarea v-model="form.description" class="form-control" rows="4"></textarea>
              </div>
              <div class="text-end mt-4">
                <button type="button" @click="$router.push('/company')" class="btn btn-light me-2">Cancel</button>
                <button type="submit" class="btn btn-primary px-4">Update Profile</button>
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
    this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      const res = await API.get("/company/profile");
      this.form = res.data;
    },
    async update() {
      try {
        await API.put("/company/profile/update", this.form);
        alert("Profile updated successfully!");
        this.$router.push("/company");
      } catch (err) {
        alert("Failed to update profile");
      }
    }
  }
}
</script>
