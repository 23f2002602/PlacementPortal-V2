<template>
  <div class="auth-wrap">
    <div class="auth-card">

      <h1 class="mb-4">Placement Portal</h1>

      <form @submit.prevent="login">

        <div class="mb-3">
          <label>Email</label>
          <input
            type="email"
            v-model="email"
            class="form-control"
            required
          />
        </div>

        <div class="mb-4">
          <label>Password</label>
          <input
            type="password"
            v-model="password"
            class="form-control"
            required
          />
        </div>

        <button class="btn-brand w-100">
          Login
        </button>

      </form>

    </div>
  </div>
</template>

<script>
export default {

  data() {
    return {
      email: "",
      password: ""
    }
  },

  methods: {

    login() {

      console.log("Login clicked")

    }

  }

}
</script>