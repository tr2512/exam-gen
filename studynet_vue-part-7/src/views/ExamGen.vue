<template>
    <div class="hero is-info">
            <div class="hero-body has-text-centered">
                <h1 class="title"> Title </h1>
            </div>
        </div>
    <div class="generate-exam-container">
    <div class="generate-exam-container03">
       <div class="column is-3">
        <ul> 
            <li><router-link v-bind:to="'/courses/' +  this.slug + '/question-database'"> Questions database </router-link></li>
            <li><router-link v-bind:to="'/courses/' + this.slug + '/exam-gen'"> Exam generation </router-link></li>
        </ul>
        </div>
      <div class="generate-exam-container06">
        <div class="generate-exam-container07">
          <span class="generate-exam-text17">
            <span>Type and number of questions</span>
          </span>
          <div class="generate-exam-container09">
            <input
              type="text"
              id="multiple_input"
              placeholder="Number of multiple choices"
              class="generate-exam-textinput1 input"
              v-model="input.qtype.multichoices"
            />
            <input
              type="text"
              id="multiple_input"
              placeholder="Number of T/F choices"
              class="generate-exam-textinput1 input"
              v-model="input.qtype.tf"
            />
            <input
              type="text"
              id="coding_input"
              placeholder="Number of paragraph questions"
              class="generate-exam-textinput2 input"
              v-model="input.qtype.paragraph"
            />
          </div>
          <span class="generate-exam-text24">Chapter spans</span>
          <div v-for="(header, index) in chapters" v-bind:key="index">
            <input
              type="checkbox"
              id="chapter1_checkbox"
              class="generate-exam-checkbox04"
              value="true"
              v-model="input.chapters[header.id]"
            />
            <label class="generate-exam-text25"> {{header.title}} </label>
          </div>
          <div class="generate-exam-container11">
            <span class="generate-exam-text35">
              Duration of the exam in minutes:
            </span>
            <label class="generate-exam-text36">Minimum</label>
            <input
              type="text"
              id="minimum_input"
              placeholder="Minimum time"
              class="generate-exam-textinput3 input"
              v-model="input.min_duration"
            />
            <label class="generate-exam-text37">Maximum</label>
            <input
              type="text"
              id="maximum_time"
              placeholder="Maximum time"
              class="generate-exam-textinput4 input"
              v-model="input.max_duration"
            />
          </div>
          <div class="generate-exam-container12">
            <span class="generate-exam-text38">Average difficulties:</span>
            <input
              type="text"
              placeholder="Ranking from 1 to 5. Decimal is accepted"
              class="generate-exam-textinput5 input"
              v-model="input.avg_diff"
            />
          </div>
            <br/>
          <div class="generate-exam-container17">
            <span class="generate-exam-text45">Output format:</span>
            <input
              type="checkbox"
              id="pdf_checkbox"
              class="generate-exam-checkbox10"
            />
            <label>PDF</label>
            <input
              type="checkbox"
              id="html_checkbox"
              class="generate-exam-checkbox11"
            />
            <label>HTML</label>
          </div>
          <div class="generate-exam-container18">
            <button type="button" class="generate-exam-button button" @click="generateExam()">
              Generate exam
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
    data() {
        return {
            slug: null,
            chapters: [],
            input: {
                "qtype": {
                    "multichoices": null,
                    "tf": null,
                    "paragraph": null,
                },
                "chapters": {},
                "min_duration": 0,
                "max_duration": 0,
                "avg_diff": 0
            },
        }
    }, 
    mounted() {
        console.log('mounted')

        const slug = this.$route.params.slug
        this.slug = slug
        axios
            .get(`/api/v1/courses/${slug}/get-chapter`)
            .then(response => {
                this.chapters = response.data
                console.log(this.chapters)
                for (let i = 0; i < response.data.length; i++) {
                    this.input.chapters[response.data[i].id] = null 
                console.log(this.input)
                }
            })
        
    }, methods: {
        generateExam() {
            const params = {"content": this.input};
            axios
                .get(`/api/v1/courses/${this.slug}/gen-exam`, {
                    responseType: 'blob',
                    params
                })
                .then(response => {
                    const blob = new Blob([response.data], { type: response.headers['content-type'] });

          // Create a temporary URL for the Blob
          const url = URL.createObjectURL(blob);

          // Create a link element and simulate a click to trigger the download
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', 'file.pdf');
          link.style.display = 'none';
          document.body.appendChild(link);
          link.click();
          document.body.removeChild(link);
                })
        }
    },
}

</script>

<style scoped>
.generate-exam-container {
  width: 100%;
  height: auto;
  display: flex;
  min-height: 100vh;
  align-items: center;
  flex-direction: column;
  justify-content: flex-start;
}
.generate-exam-container01 {
  flex: 0 0 auto;
  width: 100%;
  height: 100px;
  display: flex;
  align-items: center;
}
.generate-exam-image {
  width: 201px;
  height: 49px;
}
.generate-exam-navbar-interactive {
  width: 1011px;
  display: flex;
  align-items: center;
  padding-top: 32px;
  padding-left: 48px;
  padding-right: 48px;
  padding-bottom: 32px;
  justify-content: space-between;
}
.generate-exam-desktop-menu {
  flex: 1;
  display: flex;
  justify-content: space-between;
}
.generate-exam-container02 {
  flex: 0 0 auto;
  width: 280px;
  height: 36px;
  display: flex;
  align-items: flex-start;
  border-color: var(--dl-color-gray-black);
  border-width: 2px;
  border-radius: 5px;
}
.generate-exam-image1 {
  width: auto;
  height: 90%;
  margin-top: 2px;
  object-fit: fill;
  margin-left: 3px;
  border-radius: 5px;
}
.generate-exam-textinput {
  width: 100%;
  height: 100%;
  transition: 0.3s;
  border-width: 0px;
  padding-left: var(--dl-space-space-halfunit);
}
.generate-exam-textinput:focus {
  outline: unset;
}
.generate-exam-thq-dropdown {
  cursor: pointer;
  display: inline-block;
  position: relative;
  border-radius: 2px;
}
.generate-exam-dropdown-toggle {
  fill: #595959;
  color: #595959;
  width: 100%;
  display: inline-flex;
  align-items: center;
  padding-top: var(--dl-space-space-halfunit);
  border-color: var(--dl-color-gray-black);
  border-width: 1px;
  padding-left: var(--dl-space-space-unit);
  border-radius: 5px;
  padding-right: var(--dl-space-space-unit);
  padding-bottom: var(--dl-space-space-halfunit);
}
.generate-exam-dropdown-arrow {
  transition: 0.3s;
}
.generate-exam-icon {
  width: 18px;
  height: 18px;
  margin-top: auto;
  transition: 0.3s;
  margin-bottom: auto;
}
.generate-exam-dropdown-list {
  left: 0%;
  width: max-content;
  display: none;
  z-index: 100;
  position: absolute;
  min-width: 100%;
  transition: 0.3s;
  align-items: stretch;
  border-color: #D9D9D9;
  border-width: 1px;
  border-radius: 4px;
  flex-direction: column;
  list-style-type: none;
  background-color: var(--dl-color-gray-white);
  list-style-position: inside;
}
.generate-exam-dropdown {
  cursor: pointer;
  display: inline-block;
  position: relative;
  border-radius: 2px;
}
.generate-exam-dropdown-toggle1 {
  fill: #595959;
  color: #595959;
  width: 100%;
  display: inline-flex;
  transition: 0.3s;
  align-items: center;
  padding-top: var(--dl-space-space-halfunit);
  padding-left: var(--dl-space-space-unit);
  border-radius: 4px;
  padding-right: var(--dl-space-space-unit);
  padding-bottom: var(--dl-space-space-halfunit);
}
.generate-exam-dropdown-toggle1:hover {
  fill: #fff;
  color: #fff;
  background-color: #595959;
}
.generate-exam-text01 {
  width: 100%;
  cursor: pointer;
  display: flex;
}
.generate-exam-dropdown1 {
  cursor: pointer;
  display: inline-block;
  position: relative;
  border-radius: 2px;
}
.generate-exam-dropdown-toggle2 {
  fill: #595959;
  color: #595959;
  width: 100%;
  display: inline-flex;
  transition: 0.3s;
  align-items: center;
  padding-top: var(--dl-space-space-halfunit);
  padding-left: var(--dl-space-space-unit);
  border-radius: 4px;
  padding-right: var(--dl-space-space-unit);
  padding-bottom: var(--dl-space-space-halfunit);
}
.generate-exam-dropdown-toggle2:hover {
  fill: #fff;
  color: #fff;
  background-color: #595959;
}
.generate-exam-text02 {
  width: 100%;
  cursor: pointer;
  display: flex;
}
.generate-exam-dropdown2 {
  cursor: pointer;
  display: inline-block;
  position: relative;
  border-radius: 2px;
}
.generate-exam-dropdown-toggle3 {
  fill: #595959;
  color: #595959;
  width: 100%;
  display: inline-flex;
  transition: 0.3s;
  align-items: center;
  padding-top: var(--dl-space-space-halfunit);
  padding-left: var(--dl-space-space-unit);
  border-radius: 4px;
  padding-right: var(--dl-space-space-unit);
  padding-bottom: var(--dl-space-space-halfunit);
}
.generate-exam-dropdown-toggle3:hover {
  fill: #fff;
  color: #fff;
  background-color: #595959;
}
.generate-exam-text03 {
  width: 100%;
  cursor: pointer;
  display: flex;
}
.generate-exam-dropdown3 {
  cursor: pointer;
  display: inline-block;
  position: relative;
  border-radius: 2px;
}
.generate-exam-dropdown4 {
  cursor: pointer;
  display: inline-block;
  position: relative;
  border-radius: 2px;
}
.generate-exam-burger-menu {
  display: none;
}
.generate-exam-icon02 {
  width: 16px;
  height: 16px;
}
.generate-exam-mobile-menu {
  top: 0px;
  left: 0px;
  width: 100%;
  height: 100vh;
  display: none;
  padding: 32px;
  z-index: 100;
  position: absolute;
  flex-direction: column;
  justify-content: space-between;
  background-color: #fff;
}
.generate-exam-nav {
  display: flex;
  align-items: flex-start;
  flex-direction: column;
}
.generate-exam-top {
  width: 100%;
  display: flex;
  align-items: center;
  margin-bottom: 48px;
  justify-content: space-between;
}
.generate-exam-logo {
  height: 2rem;
}
.generate-exam-close-menu {
  display: flex;
  align-items: center;
  justify-content: center;
}
.generate-exam-icon04 {
  width: 16px;
  height: 16px;
}
.generate-exam-links {
  flex: 0 0 auto;
  display: flex;
  align-self: flex-start;
  align-items: flex-start;
  flex-direction: column;
}
.generate-exam-text04 {
  margin-bottom: var(--dl-space-space-unit);
}
.generate-exam-text05 {
  margin-bottom: var(--dl-space-space-unit);
}
.generate-exam-text06 {
  margin-bottom: var(--dl-space-space-unit);
}
.generate-exam-text07 {
  margin-bottom: var(--dl-space-space-unit);
}
.generate-exam-text08 {
  margin-bottom: var(--dl-space-space-unit);
}
.generate-exam-buttons {
  display: flex;
  margin-top: var(--dl-space-space-unit);
  align-items: center;
  flex-direction: row;
  justify-content: space-between;
}
.generate-exam-login {
  margin-right: 32px;
}
.generate-exam-icon06 {
  width: 16px;
  height: 16px;
  margin-right: 32px;
}
.generate-exam-icon08 {
  width: 16px;
  height: 16px;
  margin-right: 32px;
}
.generate-exam-icon10 {
  width: 16px;
  height: 16px;
}
.generate-exam-container03 {
  width: 100%;
  height: 870px;
  display: flex;
  overflow-y: auto;
  align-items: flex-start;
}
.generate-exam-container04 {
  flex: 0 0 auto;
  width: 309px;
  height: 100%;
  display: flex;
  align-items: center;
  margin-right: 2px;
  flex-direction: column;
  justify-content: flex-start;
}
.generate-exam-container05 {
  width: 100%;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #c20404;
}
.generate-exam-icon12 {
  fill: #D9D9D9;
  width: 24px;
  height: 24px;
  margin-left: var(--dl-space-space-tripleunit);
}
.generate-exam-text09 {
  color: #ffffff;
  width: 199px;
}
.generate-exam-ul {
  gap: var(--dl-space-space-doubleunit);
  width: 100%;
  height: 580px;
  display: flex;
  overflow-y: auto;
  align-items: flex-start;
  flex-direction: column;
  list-style-type: none;
  list-style-position: outside;
}
.generate-exam-li {
  width: 100%;
}
.generate-exam-thq-dropdown1 {
  width: 100%;
  cursor: pointer;
  display: inline-block;
  position: relative;
  visibility: visible;
  border-radius: 2px;
}
.generate-exam-dropdown-toggle4 {
  fill: #595959;
  color: #595959;
  width: 100%;
  display: inline-flex;
  align-items: center;
  padding-top: var(--dl-space-space-halfunit);
  padding-left: var(--dl-space-space-unit);
  border-radius: 2px;
  padding-right: var(--dl-space-space-unit);
  padding-bottom: var(--dl-space-space-halfunit);
}
.generate-exam-text10 {
  text-align: center;
  margin-right: 4px;
  vertical-align: middle;
}
.generate-exam-dropdown-arrow1 {
  transition: 0.3s;
}
.generate-exam-dropdown-list1 {
  left: 0%;
  width: max-content;
  display: none;
  z-index: 100;
  position: absolute;
  min-width: 100%;
  transition: 0.3s;
  align-items: stretch;
  border-color: #D9D9D9;
  border-width: 1px;
  border-radius: 4px;
  flex-direction: column;
  list-style-type: none;
  background-color: var(--dl-color-gray-white);
  list-style-position: inside;
}
.generate-exam-dropdown5 {
  cursor: pointer;
  display: inline-block;
  position: relative;
  border-radius: 2px;
}
.generate-exam-dropdown-toggle5 {
  fill: #595959;
  color: #595959;
  width: 100%;
  display: inline-flex;
  transition: 0.3s;
  align-items: center;
  padding-top: var(--dl-space-space-halfunit);
  padding-left: var(--dl-space-space-unit);
  border-radius: 4px;
  padding-right: var(--dl-space-space-unit);
  padding-bottom: var(--dl-space-space-halfunit);
}
.generate-exam-dropdown-toggle5:hover {
  fill: #fff;
  color: #fff;
  background-color: #595959;
}
.generate-exam-text11 {
  width: 100%;
  cursor: pointer;
  display: flex;
}
.generate-exam-dropdown6 {
  cursor: pointer;
  display: inline-block;
  position: relative;
  border-radius: 2px;
}
.generate-exam-dropdown-toggle6 {
  fill: #595959;
  color: #595959;
  width: 100%;
  display: inline-flex;
  transition: 0.3s;
  align-items: center;
  padding-top: var(--dl-space-space-halfunit);
  padding-left: var(--dl-space-space-unit);
  border-radius: 4px;
  padding-right: var(--dl-space-space-unit);
  padding-bottom: var(--dl-space-space-halfunit);
}
.generate-exam-dropdown-toggle6:hover {
  fill: #fff;
  color: #fff;
  background-color: #595959;
}
.generate-exam-text12 {
  width: 100%;
  cursor: pointer;
  display: flex;
}
.generate-exam-container06 {
  flex: 0 0 auto;
  width: 874px;
  height: 854px;
  display: flex;
  overflow-y: inherit;
  align-items: flex-start;
  padding-top: 10px;
  padding-left: 20px;
  flex-direction: column;
  background-color: rgba(217, 217, 217, 0.32);
}
.generate-exam-container07 {
  width: 789px;
  height: 796px;
  display: flex;
  overflow-y: inherit;
  align-items: flex-start;
  padding-top: var(--dl-space-space-unit);
  border-color: rgba(18, 18, 18, 0.28);
  border-width: 2px;
  padding-left: var(--dl-space-space-unit);
  flex-direction: column;
  background-color: #ffffff;
}
.generate-exam-text14 {
  margin-bottom: var(--dl-space-space-halfunit);
}
.generate-exam-text17 {
  margin-top: 40px;
  font-weight: 700;
}
.generate-exam-text25 {
    margin-top: 0px;
    margin-right: 10px;
    align: center
}
.generate-exam-container08 {
  width: 730px;
  height: 42px;
  display: flex;
  margin-top: var(--dl-space-space-halfunit);
  align-items: center;
  padding-left: var(--dl-space-space-halfunit);
  justify-content: space-between;
}
.generate-exam-checkbox {
  width: 1.5rem;
  height: 1.5rem;
  border-top-left-radius: var(--dl-radius-radius-radius2);
  border-top-right-radius: var(--dl-radius-radius-radius2);
  border-bottom-left-radius: var(--dl-radius-radius-radius2);
  border-bottom-right-radius: var(--dl-radius-radius-radius2);
}
.generate-exam-checkbox01 {
  width: 1.5rem;
  height: 1.5rem;
  padding-left: var(--dl-space-space-halfunit);
  border-top-left-radius: var(--dl-radius-radius-radius2);
  border-top-right-radius: var(--dl-radius-radius-radius2);
  border-bottom-left-radius: var(--dl-radius-radius-radius2);
  border-bottom-right-radius: var(--dl-radius-radius-radius2);
}
.generate-exam-checkbox02 {
  width: 1.5rem;
  height: 1.5rem;
  border-top-left-radius: var(--dl-radius-radius-radius2);
  border-top-right-radius: var(--dl-radius-radius-radius2);
  border-bottom-left-radius: var(--dl-radius-radius-radius2);
  border-bottom-right-radius: var(--dl-radius-radius-radius2);
}
.generate-exam-checkbox03 {
  width: 1.5rem;
  height: 1.5rem;
  border-top-left-radius: var(--dl-radius-radius-radius2);
  border-top-right-radius: var(--dl-radius-radius-radius2);
  border-bottom-left-radius: var(--dl-radius-radius-radius2);
  border-bottom-right-radius: var(--dl-radius-radius-radius2);
}
.generate-exam-container09 {
  width: 730px;
  height: 50px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
}
.generate-exam-textinput1 {
  width: 200px;
  height: 48px;
  margin-left: var(--dl-space-space-halfunit);
  border-color: #000000;
  border-width: 1px;
  padding-left: var(--dl-space-space-halfunit);
  padding-right: var(--dl-space-space-halfunit);
}
.generate-exam-textinput2 {
  width: 200px;
  height: 48px;
  border-color: #000000;
  border-width: 1px;
  margin-right: var(--dl-space-space-doubleunit);
  padding-left: var(--dl-space-space-halfunit);
  padding-right: var(--dl-space-space-halfunit);
}
.generate-exam-text24 {
  margin-top: 40px;
  font-weight: 700;
  margin-bottom: var(--dl-space-space-halfunit);
}
.generate-exam-container10 {
  width: 760px;
  height: 42px;
  display: flex;
  align-items: center;
  padding-left: var(--dl-space-space-halfunit);
  justify-content: space-between;
}
.generate-exam-checkbox04 {
  margin-top: 5px;
  margin-left: 10px;
  margin-right: 5px;
  width: 1.5rem;
  height: 1.5rem;
  border-top-left-radius: var(--dl-radius-radius-radius2);
  border-top-right-radius: var(--dl-radius-radius-radius2);
  border-bottom-left-radius: var(--dl-radius-radius-radius2);
  border-bottom-right-radius: var(--dl-radius-radius-radius2);
}
.generate-exam-checkbox05 {
  margin-left: 10px;
  padding-left: var(--dl-space-space-halfunit);
  border-top-left-radius: var(--dl-radius-radius-radius2);
  border-top-right-radius: var(--dl-radius-radius-radius2);
  border-bottom-left-radius: var(--dl-radius-radius-radius2);
  border-bottom-right-radius: var(--dl-radius-radius-radius2);
}
.generate-exam-checkbox06 {
  width: 1.5rem;
  height: 1.5rem;
  border-top-left-radius: var(--dl-radius-radius-radius2);
  border-top-right-radius: var(--dl-radius-radius-radius2);
  border-bottom-left-radius: var(--dl-radius-radius-radius2);
  border-bottom-right-radius: var(--dl-radius-radius-radius2);
}
.generate-exam-checkbox07 {
  width: 1.5rem;
  height: 1.5rem;
  border-top-left-radius: var(--dl-radius-radius-radius2);
  border-top-right-radius: var(--dl-radius-radius-radius2);
  border-bottom-left-radius: var(--dl-radius-radius-radius2);
  border-bottom-right-radius: var(--dl-radius-radius-radius2);
}
.generate-exam-checkbox08 {
  width: 1.5rem;
  height: 1.5rem;
  border-top-left-radius: var(--dl-radius-radius-radius2);
  border-top-right-radius: var(--dl-radius-radius-radius2);
  border-bottom-left-radius: var(--dl-radius-radius-radius2);
  border-bottom-right-radius: var(--dl-radius-radius-radius2);
}

.generate-exam-checkbox09 {
  width: 1.5rem;
  height: 1.5rem;
  border-top-left-radius: var(--dl-radius-radius-radius2);
  border-top-right-radius: var(--dl-radius-radius-radius2);
  border-bottom-left-radius: var(--dl-radius-radius-radius2);
  border-bottom-right-radius: var(--dl-radius-radius-radius2);
}
.generate-exam-container11 {
  width: 744px;
  height: 75px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.generate-exam-text35 {
  margin-top: 40px;
  align-self: center;
  font-weight: 700;
}
.generate-exam-text36 {
    margin-top: 40px;
  font-weight: 600;
}
.generate-exam-textinput3 {
    margin-top: 40px;
  width: 150px;
  border-color: #000000;
  border-width: 1px;
}
.generate-exam-text37 {
    margin-top: 40px;
  font-weight: 600;
}
.generate-exam-textinput4 {
    margin-top: 40px;
  width: 150px;
  border-color: #000000;
  border-width: 1px;
}
.generate-exam-container12 {
  margin-top: 40px;
  width: 521px;
  height: 45px;
  display: flex;
  align-self: flex-start;
  align-items: center;
  justify-content: space-between;
}
.generate-exam-text38 {
  font-weight: 700;
}
.generate-exam-textinput5 {
  width: 350px;
  border-color: #000000;
  border-width: 1px;
}
.generate-exam-text39 {
  margin-top: var(--dl-space-space-unit);
  font-weight: 700;
  margin-bottom: var(--dl-space-space-doubleunit);
}
.generate-exam-container13 {
  width: 745px;
  height: 197px;
  display: flex;
  overflow-y: inherit;
  align-items: flex-start;
  flex-direction: column;
}
.generate-exam-container14 {
  width: 100%;
  height: 49px;
  display: flex;
  position: relative;
  margin-top: var(--dl-space-space-halfunit);
  align-items: center;
  margin-bottom: var(--dl-space-space-halfunit);
  justify-content: space-between;
}
.generate-exam-text42 {
  font-weight: 600;
}
.generate-exam-select {
  width: 425px;
  height: 100%;
  display: flex;
  border-color: #000000;
  border-width: 1px;
}
.generate-exam-select1 {
  width: 195px;
  height: 100%;
  border-color: #000000;
  border-width: 1px;
}
.generate-exam-container15 {
  width: 100%;
  height: 49px;
  display: flex;
  margin-top: var(--dl-space-space-halfunit);
  align-items: center;
  margin-bottom: var(--dl-space-space-halfunit);
  justify-content: space-between;
}
.generate-exam-text43 {
  font-weight: 600;
}
.generate-exam-select2 {
  width: 425px;
  height: 100%;
  border-color: #000000;
  border-width: 1px;
}
.generate-exam-select3 {
  width: 195px;
  height: 100%;
  border-color: #000000;
  border-width: 1px;
}
.generate-exam-container16 {
  width: 100%;
  height: 49px;
  display: flex;
  margin-top: var(--dl-space-space-halfunit);
  align-items: center;
  margin-bottom: var(--dl-space-space-halfunit);
  justify-content: space-between;
}
.generate-exam-text44 {
  font-weight: 600;
}
.generate-exam-select4 {
  width: 425px;
  height: 100%;
  border-color: #000000;
  border-width: 1px;
}
.generate-exam-select5 {
  width: 195px;
  height: 100%;
  border-color: #000000;
  border-width: 1px;
}
.generate-exam-container17 {
  margin-top: 40px;
  width: 316px;
  height: 49px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.generate-exam-text45 {
  font-weight: 700;
}
.generate-exam-checkbox10 {
  width: 1.5rem;
  height: 1.5rem;
  border-top-left-radius: var(--dl-radius-radius-radius2);
  border-top-right-radius: var(--dl-radius-radius-radius2);
  border-bottom-left-radius: var(--dl-radius-radius-radius2);
  border-bottom-right-radius: var(--dl-radius-radius-radius2);
}
.generate-exam-checkbox11 {
  width: 1.5rem;
  height: 1.5rem;
  border-top-left-radius: var(--dl-radius-radius-radius2);
  border-top-right-radius: var(--dl-radius-radius-radius2);
  border-bottom-left-radius: var(--dl-radius-radius-radius2);
  border-bottom-right-radius: var(--dl-radius-radius-radius2);
}
.generate-exam-container18 {
  width: 100%;
  height: 71px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.generate-exam-button {
  color: #ffffff;
  background-color: #d40000;
}
@media(max-width: 767px) {
  .generate-exam-navbar-interactive {
    padding-left: 32px;
    padding-right: 32px;
  }
  .generate-exam-desktop-menu {
    display: none;
  }
  .generate-exam-burger-menu {
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .generate-exam-text04 {
    margin-bottom: var(--dl-space-space-unit);
  }
  .generate-exam-text05 {
    margin-left: 0;
    margin-bottom: var(--dl-space-space-unit);
  }
  .generate-exam-text06 {
    margin-left: 0;
    margin-bottom: var(--dl-space-space-unit);
  }
  .generate-exam-text07 {
    margin-left: 0;
    margin-bottom: var(--dl-space-space-unit);
  }
  .generate-exam-text08 {
    margin-left: 0;
    margin-bottom: var(--dl-space-space-unit);
  }
}
@media(max-width: 479px) {
  .generate-exam-navbar-interactive {
    padding: var(--dl-space-space-unit);
  }
  .generate-exam-mobile-menu {
    padding: 16px;
  }
}
</style>