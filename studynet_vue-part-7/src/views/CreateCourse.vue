<template>
    <div class="hero is-info has-background-link">
        <div class="hero-body has-text-centered">
            <h1 class="title"> Create course </h1>
        </div>
    </div>
  <div class="create-course-container">
    <form @submit.prevent="createCourse" class="create-course-form">
      <div class="form-field">
        <label class="label">Title:</label>
        <input type="text" v-model="title" required />
      </div>

      <div class="form-field">
        <label class="label">Acronym:</label>
        <input type="text" v-model="acronym" required />
      </div>

      <div class="form-field">
        <label class="label">Short Description:</label>
        <textarea v-model="shortDescription" required></textarea>
      </div>

      <div class="form-field">
        <label class="label">Long Description:</label>
        <textarea v-model="longDescription" required></textarea>
      </div>

      <div v-for="(chapter, index) in chapters" :key="index" class="chapter-field">
        <p class="is-size-4">Chapter {{ index + 1 }}</p>
        <div class="form-field">
          <label class="label">Title:</label>
          <input type="text" v-model="chapter.title" required />
        </div>

        <div class="form-field">
          <label class="label">Description:</label>
          <textarea v-model="chapter.description" required></textarea>
        </div>
      </div>

      <div class="form-field">
        <button type="button" @click="addChapter">Add Chapter</button>
      </div>

      <div class="form-field">
        <label class="label">Teacher:</label>
        <div v-for="teacher in this.teachers" :key="teacher.id">
          <input
            type="checkbox"
            :id="'teacher_' + teacher.id"
            :value="teacher.id"
            v-model="selectedTeachers[teacher.id]"
          >
          <label>{{ teacher.username }}</label>
        </div>
      </div>

      <button type="submit">Create</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      title: '',
      acronym: '',
      shortDescription: '',
      longDescription: '',
      chapters: [],
      selectedTeachers: {},
      teachers: [],
      courseData: {},
    };
  },
  methods: {
     createCourse() {
      // Prepare the course data
      this.courseData = {
        title: this.title,
        acronym: this.acronym,
        shortDescription: this.shortDescription,
        longDescription: this.longDescription,
        chapters: this.chapters,
        selectedTeachers: this.selectedTeachers,
      };
      console.log(this.courseData)
      // Send the course data to the backend
      axios
        .post('/api/v1/courses/create-course/', this.courseData)
        .then((response) => {
          // Handle the response from the backend
          console.log(response);
          this.$router.go()
        })
        .catch((error) => {
          // Handle any errors
          console.error(error);
        });
    },
    addChapter() {
      this.chapters.push({ title: '', description: '' });
    },
    fetchTeachers() {
      // Fetch the list of available teachers from the backend
      axios
        .get('/api/v1/courses/get-teachers/')
        .then((response) => {
          // Update the teachers array
          this.teachers = response.data;
          console.log(response)
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  mounted() {
    this.fetchTeachers();
    this.addChapter(); // Add an initial chapter
  },
};
</script>

<style scoped>
.create-course-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 50px;
}

.create-course-form {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  width: 100%;
  padding: 40px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
}

.form-field {
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
  width: 100%;
}

.form-field label {
  align-self: flex-start;
}

.chapter-field {
    display: flex;
  flex-direction: column;
  margin-bottom: 20px;
  width: 100%;
}

button {
  padding: 12px 24px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}
</style>
