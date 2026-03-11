<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="text-primary fw-bold">Applicants Management</h2>
      <button @click="$router.push('/company')" class="btn btn-outline-secondary btn-sm">Back to Dashboard</button>
    </div>

    <div class="card border-0 shadow-sm">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0 text-center">
          <thead class="table-dark">
            <tr>
              <th>Student Name</th>
              <th>Email</th>
              <th>CGPA</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in applicants" :key="a.id">
              <td class="fw-bold text-start ps-4">{{ a.student }}</td>
              <td class="text-muted">{{ a.email }}</td>
              <td><span class="badge bg-light text-dark border">{{ a.cgpa || 'N/A' }}</span></td>
              <td>
                <span :class="getStatusClass(a.status)" class="badge">
                  {{ a.status.toUpperCase() }}
                </span>
              </td>
              <td class="text-nowrap">
                <template v-if="a.status === 'applied'">
                  <button @click="accept(a.id)" class="btn btn-sm btn-success me-1">Shortlist/Select</button>
                  <button @click="reject(a.id)" class="btn btn-sm btn-outline-danger">Reject</button>
                </template>
                <span v-else class="text-muted small">Status Updated</span>
              </td>
            </tr>
            <tr v-if="applicants.length === 0">
              <td colspan="5" class="text-center py-5 text-muted">No applications received yet.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import API from "../../utils/api.js"

export default {
  data() {
    return {
      applicants: []
    }
  },
  async mounted() {
    this.fetchApplicants();
  },
  methods: {
    async fetchApplicants() {
      const id = this.$route.params.id;
      const res = await API.get(`/company/drive/${id}/applications`);
      this.applicants = res.data;
    },
    async accept(id) {
      if (confirm("Confirm selection of this student? This will create a placement record.")) {
        await API.put(`/company/application/${id}/accept`);
        this.fetchApplicants();
      }
    },
    async reject(id) {
      if (confirm("Are you sure you want to reject this applicant?")) {
        await API.put(`/company/application/${id}/reject`);
        this.fetchApplicants();
      }
    },
    getStatusClass(status) {
      const map = { 'applied': 'bg-primary', 'selected': 'bg-success', 'rejected': 'bg-danger' };
      return map[status] || 'bg-secondary';
    }
  }
}
</script>