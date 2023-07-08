<template>
    <div class="courses">
        <div class="hero is-info">
            <div class="hero-body has-text-centered">
                <h1 class="title"> Courses </h1>
            </div>
        </div>

        <section class="section">
            <div class="container">
                <div class="columns">
                    <div class="column is-2">
                        <aside class="menu">
                            <p class="menu-label"> Categories </p>

                            <ul class="new-list">
                                <li><a> All courses </a></li>
                                <li><a> Something </a></li>
                                <li><a> Something </a></li>
                            </ul>
                        </aside>
                    </div>

                    <div class="column is-10"
                        v-for="course in courses"
                        v-bind:key="course.id"
                    >  
                        <div class="card">
                            <div class="card-image">
                                <figure class="image is-128x128">
                                    <img src="../assets/logo.png">
                                </figure>
                            </div>

                            <div class="card-content">
                                <div class="media">
                                    <div class="media-content">
                                        <p class="is-size-5"> {{course.title}} </p>
                                    </div>
                                </div>
                            </div>

                            <div class="content">
                                <p class="size is-5"> {{course.long_description}} </p>

                                <router-link :to="{'name': 'Course', params: {slug: course.slug}}"> More </router-link>
                            </div>
                        </div>
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
            courses: []
        }
    }, 
    mounted() {
        console.log('mounted')

        axios
            .get(`/api/v1/courses/`)
            .then(response => {
                console.log(response.data)

                this.courses = response.data
            })
    }
}
</script>