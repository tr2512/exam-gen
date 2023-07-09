<template>
  <div class="about">
    <div class="hero is-info has-background-link">
      <div class="hero-body has-text-centered">
        <h1 class="title">My Account</h1>
      </div>
    </div>

    <section class="section">
      <button @click="logout()" class="button is-danger">Log out</button>
    </section>
  </div>
</template>

<script>
import axios from 'axios'

export default {
    data() {
        return {
        userGroup: null
        }
    },
    async mounted () {
        axios
            .get('/api/v1/courses/verify/')
            .then(response => {
                console.log(response.data.user_group)
                this.userGroup = response.data.user_group
            })
    },
    methods: {
        async logout() {
            console.log('logout')

            await axios
              .post('/api/v1/token/logout/')
              .then(response => {
                console.log('Logged out')
              })
              .catch(error => {
                console.log(error)
              })

            axios.defaults.headers.common['Authorization'] = ""

            localStorage.removeItem('token')

            this.$store.commit('removeToken')

            this.$router.push('/')
        }
    }
}
</script>