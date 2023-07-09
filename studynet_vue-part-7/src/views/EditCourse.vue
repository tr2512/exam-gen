<template>
    <div class="hero is-info has-background-link">
        <div class="hero-body has-text-centered">
            <h1 class="title"> Create course </h1>
        </div>
    </div>
  <div class="create-course-container">

    <form @submit.prevent="editCourse" class="create-course-form">
      <div class="form-field">
        <label class="label">Title:</label>
        <input type="text" v-model="title" required>
      </div>

      <div class="form-field">
        <label class="label">Acronym:</label>
        <input type="text" v-model="acronym" required>
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
          <textarea v-model="chapter.chapter_content" required></textarea>
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
            v-model="selectedTeachers"
          >
          <label>{{teacher.username}}</label>
        </div>
      </div>

      <button type="submit">Save Changes</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      courseId: null,
      title: '',
      acronym: '',
      shortDescription: '',
      longDescription: '',
      chapters: [],
      selectedTeachers: [],
      teachers: [],
      chapters: [],
    };
  },
  methods: {
    fetchCourse() {
      axios
        .get(`/api/v1/courses/course/${this.$route.params.slug}/`)
        .then((response) => {
            console.log(response.data)
          this.courseId = response.data.course.id;
          this.title = response.data.course.title;
          this.acronym = response.data.course.slug;
          this.shortDescription = response.data.course.short_description;
          this.longDescription = response.data.course.long_description;
          this.chapters = response.data.chapters;
          this.teachers = response.data.teachers;
          for (let i = 0; i < this.teachers.length; i++) {
                this.selectedTeachers.push(this.teachers[i].teacher_id)
          }
    
        })
        .catch((error) => {
          console.error(error);
        });
    },
    fetchTeachers() {
      axios
        .get(`/api/v1/courses/${this.$route.params.slug}/teachers/`)
        .then((response) => {
            this.teachers = response.data;

        })
        .catch((error) => {
          console.error(error);
        });
    },
    addChapter() {
      this.chapters.push({
        title: '',
        content: '',
      });
    },
    editCourse() {
      const courseData = {
        title: this.title,
        acronym: this.acronym,
        short_description: this.shortDescription,
        long_description: this.longDescription,
        chapters: this.chapters,
        teachers: this.selectedTeachers,
      };

      axios
        .post(`/api/v1/courses/${this.acronym}/edit-course/`, courseData)
        .then((response) => {
          console.log(response);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  mounted() {
    this.fetchCourse();
    this.fetchTeachers();
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
