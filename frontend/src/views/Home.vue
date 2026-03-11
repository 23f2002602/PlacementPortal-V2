<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100">
    <div class="spinner-border text-primary" role="status">
      <span class="visually-hidden">Loading...</span>
    </div>
  </div>
</template>

<script>
export default {
  mounted() {
    const role = localStorage.getItem('ppa_role');
    if (!role) {
      this.$router.push('/login');
    } else if (role === 'admin') {
      this.$router.push('/admin');
    } else if (role === 'student') {
      this.$router.push('/student');
    } else if (role === 'company') {
      this.$router.push('/company');
    } else {
      this.$router.push('/login');
    }
  }
};
</script>
