<template>
    <div class="courses">
        <div class="hero is-info has-background-link">
            <div class="hero-body has-text-centered">
                <h1 class="title"> Courses </h1>
            </div>
        </div>
         <router-link to="/courses/create-course" v-if="this.userGroup === 'Admin'"><button> Create course</button> </router-link> 

        <section class="section">
            <div class="container">
                <div class="columns is-multiline">

                    <div class="column is-4"
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
                                <div class="has-text-danger-dark">
                                <div class="is-clickable" @click="deleteCourse(course)" v-if="this.userGroup === 'Admin'"> Delete course </div>
                                <router-link :to="{'name': 'EditCourse', params: {slug: course.slug}}"> Edit course </router-link>
                                </div>
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
            courses: [],
            userGroup: null
        }
    }, 
    mounted() {
        console.log('mounted')

        axios
            .get(`/api/v1/courses/course/`)
            .then(response => {
                console.log(response.data)

                this.courses = response.data
        })

        axios
            .get('/api/v1/courses/verify/')
            .then(response => {
                console.log(response.data.user_group)
                this.userGroup = response.data.user_group
            })
    }, methods: {
        deleteCourse(course) {
            confirm("Are you sure about deleting " + course.title +  " course?")
            axios
                .post("/api/v1/courses/delete-course/", course)
                .then(response => {
                    alert("The course " + course.title + " has been deleted")
                    this.$router.go()
                }) 
                .catch(error => {
                    alert("The delete operation faled, please try again.")
                })
        } 
    },
}
</script>