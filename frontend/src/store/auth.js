import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {

  state: () => ({

    token: localStorage.getItem('ppa_token') || null,

    user: JSON.parse(localStorage.getItem('ppa_user') || 'null')

  }),

  getters: {

    isLoggedIn: (state) => !!state.token,

    role: (state) => state.user?.role || ''

  },
  actions: {

    setSession(token, userData) {

      this.token = token

      this.user = userData

      localStorage.setItem('ppa_token', token)

      localStorage.setItem('ppa_user', JSON.stringify(userData))

    },

    logout() {

      this.token = null

      this.user = null

      localStorage.removeItem('ppa_token')

      localStorage.removeItem('ppa_user')

    }

  }

})