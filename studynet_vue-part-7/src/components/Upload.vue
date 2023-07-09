<template>
  <div>
    <input type="file" @change="handleFileUpload" accept=".csv" />
    <button @click="uploadFile">Upload</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      file: null,
    };
  },
  methods: {
    handleFileUpload(event) {
      this.file = event.target.files[0];
    },
    uploadFile() {
      const formData = new FormData();
      formData.append('file', this.file);
    },
  },
};
</script>