import axios from "axios"

const API = axios.create({
  baseURL: "http://localhost:5000/api"
})

// attach JWT token automatically
API.interceptors.request.use((config) => {

  const token = localStorage.getItem("ppa_token")

  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

export default {

  login(data) {
    return API.post("/login", data)
  },

  register(formData) {
    return API.post("/register", formData, {
      headers: { "Content-Type": "multipart/form-data" }
    })
  },

  getStudents() {
    return API.get("/admin/students")
  },

  getCompanies() {
    return API.get("/admin/companies")
  },

  getDrives() {
    return API.get("/admin/drives")
  }

}