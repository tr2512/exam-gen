<template>
    <div class="course">
        <div class="hero is-info">
            <div class="hero-body has-text-centered">
                <h1 class="title"> {{course.title}} </h1>
            </div>
        </div>

        <section class="section">
            <div class="container">
                <div class="columns content">
                    <div class="column is-2">
                        <h2> Table of contents </h2>

                        <ul> 
                            <router-link v-bind:to="'/courses/' + course.slug + '/question-database'"> Questions database </router-link>
                            <li href="#"> Generate exam </li>
                        </ul>
                    </div>

                    <div class="column-is-10">
                        <template v-if="$store.state.user.isAuthenticated">
                            {{course.short_description}}
                        </template>

                        <template v-else>
                            <h2> Restricted access </h2>
                            <p> You do not have permission to access the course {{course.title}} </p>
                        </template>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
import axios from 'axios'
   export default {
    data() {
        return {
            course: {},
        }
    }, 
    mounted() {
        console.log('mounted')

        const slug = this.$route.params.slug

        axios
            .get(`/api/v1/courses/${slug}/`)
            .then(response => {
                console.log(response.data)

                this.course = response.data.course
            })
    }
}
</script>