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

// Add helper methods directly to the API instance
API.login = (data) => API.post("/login", data);
API.register = (data, isMultipart = false) => {
  if (isMultipart) {
    return API.post("/register", data, {
      headers: { "Content-Type": "multipart/form-data" }
    });
  }
  const formData = new FormData();
  for (const key in data) {
    formData.append(key, data[key]);
  }
  return API.post("/register", formData);
};
API.getStudents = () => API.get("/admin/students");
API.getCompanies = () => API.get("/admin/companies");
API.getDrives = () => API.get("/admin/drives");

export default API;