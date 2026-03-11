<template>
  <div class="container py-4">
    <div class="d-flex justify-content-between align-items-center mb-4 bg-white p-3 rounded shadow-sm">
      <h2 class="text-primary fw-bold mb-0">Student Management</h2>
      <div class="input-group w-50">
        <input type="text" class="form-control" placeholder="Search by name..." v-model="searchQuery" @keyup.enter="search">
        <button class="btn btn-primary" @click="search">Search</button>
      </div>
    </div>

    <div class="card shadow-sm border-0">
      <div class="table-responsive">
        <table class="table table-hover align-middle mb-0 text-center">
          <thead class="table-dark">
            <tr>
              <th>Name</th>
              <th>Roll No</th>
              <th>Branch</th>
              <th>CGPA</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in students" :key="s.id">
              <td>
                <div class="fw-bold">{{ s.name }}</div>
                <small class="text-muted">{{ s.email }}</small>
              </td>
              <td>{{ s.roll_number }}</td>
              <td>{{ s.branch }}</td>
              <td><span class="badge bg-light text-dark border">{{ s.cgpa }}</span></td>
              <td>
                <span :class="s.is_blacklisted ? 'badge bg-danger' : (s.is_active ? 'badge bg-success' : 'badge bg-secondary')">
                  {{ s.is_blacklisted ? 'Blacklisted' : (s.is_active ? 'Active' : 'Deactivated') }}
                </span>
              </td>
              <td class="text-nowrap">
                <button @click="toggleBlacklist(s)" class="btn btn-sm me-1" :class="s.is_blacklisted ? 'btn-success' : 'btn-danger'">
                  {{ s.is_blacklisted ? 'Unblacklist' : 'Blacklist' }}
                </button>
                <button @click="toggleStatus(s)" class="btn btn-sm btn-outline-warning me-1">
                  {{ s.is_active ? 'Deactivate' : 'Activate' }}
                </button>
                <button @click="editStudent(s)" class="btn btn-sm btn-info me-1">Edit</button>
                <button @click="deleteStudent(s.id)" class="btn btn-sm btn-danger">Delete</button>
              </td>
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
      students: [],
      searchQuery: ""
    }
  },
  async mounted() {
    this.fetchStudents();
  },
  methods: {
    async fetchStudents() {
      const res = await API.get("/admin/students");
      this.students = res.data;
    },
    async search() {
      const res = await API.get(`/admin/search?role=student&q=${this.searchQuery}`);
      this.students = res.data;
    },
    async toggleBlacklist(s) {
      if (confirm(`Are you sure you want to ${s.is_blacklisted ? 'unblacklist' : 'blacklist'} ${s.name}?`)) {
        await API.put(`/admin/user/${s.user_id}/blacklist`);
        this.fetchStudents();
      }
    },
    async toggleStatus(s) {
      const action = s.is_active ? 'deactivate' : 'activate';
      if (confirm(`Are you sure you want to ${action} ${s.name}?`)) {
        await API.put(`/admin/user/${s.user_id}/${action}`);
        this.fetchStudents();
      }
    },
    async editStudent(s) {
      const branch = prompt("Edit Branch:", s.branch);
      const cgpa = prompt("Edit CGPA:", s.cgpa);
      const year = prompt("Edit Year:", s.year);
      if (branch !== null && cgpa !== null && year !== null) {
        await API.put(`/admin/student/${s.id}/update`, { branch, cgpa, year, roll_number: s.roll_number });
        this.fetchStudents();
      }
    },
    async deleteStudent(id) {
      if (confirm("Are you sure? This will delete the student and their login account.")) {
        await API.delete(`/admin/student/${id}/delete`);
        this.fetchStudents();
      }
    }
  }
}
</script>