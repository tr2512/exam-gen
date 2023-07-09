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
                            <li><router-link v-bind:to="'/courses/' + course.slug + '/question-database'"> Questions database </router-link></li>
                            <li><router-link v-bind:to="'/courses/' + course.slug + '/exam-gen'"> Exam generation </router-link></li>
                        </ul>
                    </div>

                    <div class="column is-10">
                        <div>
                            <input type="file" ref="fileInput" accept=".csv" />
                            <button @click="uploadFile">Upload CSV file for test time duration</button>
                        </div>
                        <input type="text" class="input" v-model="filterText" @input="applyFilter" placeholder="Filter">

                        <div class="table-container">
                        <!-- Table -->
                            <table class="table">
                                <thead>
                                    <tr>
                                        <th   
                                            v-for="(item, i) in headlist" v-bind:key="i"
                                        > {{item.row}}
                                        </th>
                                        <th>Answer 1</th>
                                        <th>Answer 2</th>
                                        <th>Answer 3</th>
                                        <th>Answer 4</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr v-for="(quiz, i) in quizzes" v-bind:key="i">
                                        <td v-for="(header, j) in headlist" v-bind:key="j">
                                            <span v-if="selected_item === quiz && header.row !== 'qtype'">
                                                <input v-model="quiz[header.row]" type="text">
                                            </span>
                                            <span v-else>
                                                {{quiz[header.row]}}
                                            </span>
                                        </td>
                                            
                                        <td><span v-if="selected_item === quiz && quiz.multichoice.answer1">
                                                <input v-model="quiz.multichoice.answer1" type="text">
                                            </span>
                                            <span v-else>
                                                {{quiz.multichoice.answer1}}
                                            </span></td>
                                        
                                        <td><span v-if="selected_item === quiz && quiz.multichoice.answer2">
                                                <input v-model="quiz.multichoice.answer2" type="text">
                                            </span>
                                            <span v-else>
                                                {{quiz.multichoice.answer2}}
                                            </span></td>
                                        
                                        <td><span v-if="selected_item === quiz && quiz.multichoice.answer3">
                                                <input v-model="quiz.multichoice.answer3" type="text">
                                            </span>
                                            <span v-else>
                                                {{quiz.multichoice.answer3}}
                                            </span></td>
                                        
                                        <td><span v-if="selected_item === quiz && quiz.multichoice.answer4">
                                                <input v-model="quiz.multichoice.answer4" type="text">
                                            </span>
                                            <span v-else>
                                                {{quiz.multichoice.answer4}}
                                            </span></td>
                                        <td>

                                        <!-- Edit button -->
                                            <button @click="editItem(quiz)">Edit</button>

                                            <!-- Delete button -->
                                            <button @click="deleteItem(quiz)">Delete</button>
                                            <button class="button is-small is-success" v-if="selected_item === quiz" @click="updateItem(quiz)">Update</button>

                                        </td>
                                    </tr>
                                </tbody>

                                <tfoot>
                                    <td v-for="(value, name) in this.inserted_item">
                                        <input v-model="this.inserted_item[name]" type="text">
                                    </td>
                                    <td> <button @click="insertItem()">Insert</button> 
                                    </td>
                                </tfoot>
                            </table>  
                        </div>  
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
import Upload from '@/components/Upload'
import axios from 'axios'
   export default {
    data() {
        return {
            course: {},
            selected_item: null,
            inserted_item: {
                "Chapter": null,
                "content": null,
                "level": null,
                "avgtime": null,
                "qtype": null,
                "answer": null,
                "Answer 1": null,
                "Answer 2": null,
                "Answer 3": null,
                "Answer 4": null,
            },
            headlist: [
                {"row": "Chapter"},
                {"row": "content"},
                {"row": "level"},
                {"row": "avgtime"},
                {"row": "qtype"},
                {"row": "answer"},
            ],
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
    uploadFile() {
      const file = this.$refs.fileInput.files[0];
      const formData = new FormData();
      formData.append('file', file);

      axios
        .post(`/api/v1/courses/${this.course.slug}/upload-csv/`, formData)
        .then((response) => {
          alert("Succesful update!")
          this.$router.go()
          console.log(response);
        })
        .catch((error) => {
          // Handle any errors
          console.error(error);
        });
    },
    insertItem() {
    axios
        .post(`/api/v1/courses/${this.course.slug}/insert-quiz/`, this.inserted_item)
        .then(response => {
                    alert("Question has been insrted")
                    this.$router.go()
                })
                .catch(error => {
                    alert(error.response)  
                    console.log(error)
                })
      // Logic to show insert form or navigate to insert view
    },
    applyFilter() {
        const params = {
            "content": this.filterText, 
            };
        axios
            .get(`/api/v1/courses/${this.course.slug}/filter-quiz`, {params})
            .then(response => {
                console.log(response.data)
                this.quizzes = response.data
            })
    },
    editItem(item) {
        this.selected_item = item
    },
    deleteItem(item) {
        if (confirm('Are you sure'))
            axios 
                .delete(`/api/v1/courses/${this.course.slug}/delete-quiz/${item.id}/`)
                .then(response => {
                    alert("Question " + item.id + " has been deleted")
                    this.$router.go()
                })
                .catch(error => {
                    alert(response.data)
                    this.$router.go()
                })
            
    }, 
    updateItem(item) {
        this.selected_item = null
        axios
            .post(`/api/v1/courses/${this.course.slug}/edit-quizzes/`, item)
            .then(response => {
                alert("Question " + item.id + " has been added")
                this.$router.go()
            })
            .catch(error => {
            console.log(error)
            alert(error.response)

            })
    }
  },
}
</script>