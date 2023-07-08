<template>
    <div class="QuestionDatabase">
        <div class="hero is-info">
            <div class="hero-body has-text-centered">
                <h1 class="title"> {{course.title}} questions database </h1>
            </div>
        </div>

        <section class="section">
            <div class="container">
                <div class="columns content">
                    <div class="column is-2">
                        <h2> Table of contents </h2>

                        <ul> 
                            <li href="#"> Questions database </li>
                            <li href="#"> Generate exam </li>
                        </ul>
                    </div>

                    <div class="column is-10">
                        <!-- Insert button -->
                        <button @click="showInsertForm">Insert</button>

                        <!-- Filter input -->
                        <input type="text" class="input" v-model="filterText" @input="applyFilter" placeholder="Filter">

                        <!-- Table -->
                        <table class="table">
                            <thead>
                                <tr>
                                    <th   
                                        v-for="(item, i) in headlist" v-bind:key="i"
                                    > {{item.row}}
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(quiz, i) in quizzes" v-bind:key="i">
                                    <td v-for="(header, j) in headlist" v-bind:key="j">
                                        {{quiz[header.row]}}
                                    </td>
                                    
                                    <td>

                                    <!-- Edit button -->
                                        <button @click="editItem(item)">Edit</button>

                                        <!-- Delete button -->
                                        <button @click="deleteItem(item)">Delete</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
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
            headlist: [],
            quizzes: [],
            filterText: '', // Filter input value
        }
    }, 
    mounted() {
        console.log('mounted')

        const slug = this.$route.params.slug

        axios
            .get(`/api/v1/courses/${slug}/get-quizzes`)
            .then(response => {
                console.log(response.data)
                this.headlist = response.data.headlist
                this.course = response.data.course
                this.quizzes = response.data.quizzes
                console.log(this.quizzes)
            })
    }, computed: {
    filteredItems() {
      // Apply filter on items based on filterText
      return this.quizzes.filter(item =>
        item.name.toLowerCase().includes(this.filterText.toLowerCase()) ||
        item.email.toLowerCase().includes(this.filterText.toLowerCase())
      );
    },
  },
  methods: {
    showInsertForm() {
      // Logic to show insert form or navigate to insert view
    },
    applyFilter() {
      // Logic to apply filter
    },
    editItem(item) {
      // Logic to edit the item
    },
    deleteItem(item) {
      // Logic to delete the item
    },
  },
}
</script>