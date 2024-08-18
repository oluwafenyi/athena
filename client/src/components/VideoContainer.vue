<script>
import UploadIcon from './icons/IconUpload.vue'

export default {
  name: 'VideoContainer',
  props: {
    forUpload: {
      type: Boolean,
      default: false
    },
    videoDataUrl: {
      type: String
    },
    videoFileName: {
      type: String,
      default: 'translated-video.mp4'
    }
  },
  components: {
    UploadIcon
  },
  methods: {
    handleUploadButtonClick() {
      this.$refs.videoUploadField.click()
    },
    handleLanguageSelection(event, sourceOrTarget) {
      const languageCode = event.target.value
      this.$emit('languageSelectionUpdate', languageCode, sourceOrTarget)
    },
    handleUploadFileChange(event) {
      const file = event.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
          this.$emit('inputVideoUpdate', e.target.result, file.name)
        }
        reader.readAsDataURL(file)
      } else {
        this.$emit('inputVideoUpdate', null, null)
      }
    },
    handleVideoDownload() {
      const link = document.createElement('a')
      link.href = this.videoDataUrl
      link.setAttribute('download', this.videoFileName)
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  },
  data() {
    return {
      supportedLanguages: [
        { id: 1, name: 'English', code: 'en' },
        { id: 2, name: 'French', code: 'fr' },
        { id: 3, name: 'Spanish', code: 'es' }
      ],
      sourceLanguageCode: null
    }
  }
}
</script>

<template>
  <div class="wrapper">
    <h1 v-if="forUpload">Athena: Video-to-Video Translation</h1>
    <h1 v-else>Translated Video</h1>

    <div class="centered-box">
      <UploadIcon v-if="forUpload && videoDataUrl === null" @click="handleUploadButtonClick" />
      <form v-if="forUpload">
        <input
          @change="handleUploadFileChange"
          type="file"
          ref="videoUploadField"
          id="video-upload"
          name="video"
          accept="video/*"
          style="display: none"
          required
        />
      </form>
      <video v-if="videoDataUrl !== null" controls>
        <source :src="videoDataUrl" />
      </video>
    </div>
    <div class="form-container" v-if="forUpload">
      <div class="fields-container">
        <div class="fields-container--selection">
          <label>Source Language</label>
          <select
            name="source-language"
            id="sourceLanguage"
            @change="handleLanguageSelection($event, 'source')"
          >
            <option disabled selected value style="display: none">-- select an option --</option>
            <option v-for="lang in supportedLanguages" :value="lang.code" :key="lang.id">
              {{ lang.name }}
            </option>
          </select>
        </div>

        <div class="fields-container--selection">
          <label>Target Language</label>
          <select
            name="target-language"
            id="targetLanguage"
            @change="handleLanguageSelection($event, 'target')"
          >
            <option disabled selected value style="display: none">-- select an option --</option>
            <option v-for="lang in supportedLanguages" :value="lang.code" :key="lang.id">
              {{ lang.name }}
            </option>
          </select>
        </div>
      </div>
      <div class="buttons-container">
        <button @click="handleUploadButtonClick">Select Video File</button>
        <button @click="$emit('translateVideo')">Translate</button>
      </div>
    </div>
    <div class="form-container" v-else>
      <div class="fields-container"></div>
      <div class="buttons-container">
        <button @click="handleVideoDownload">Download</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
h1 {
    color: rgb(124, 145, 151);
}

.wrapper {
  display: flex;
  justify-content: center; /* Center horizontally */
  align-items: center; /* Center vertically */
  flex-direction: column; /* Stack box and buttons vertically */
  min-height: 100vh; /* Full viewport height */
}

.centered-box {
  width: 1600px; /* Set the width of the box */
  height: 700px; /* Set the height of the box */
  background-color: #ffffff; /* Background color of the box */
  border-radius: 8px; /* Optional: Rounded corners */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Optional: Box shadow */
  display: flex;
  align-items: center; /* Center content vertically */
  justify-content: center; /* Center content horizontally */
  text-align: center; /* Center text inside the box */
  margin-bottom: 20px; /* Space between the box and buttons */
  border-width: thick;
  border-color: lightblue;
  border-style: solid;
}

.form-container {
  text-align: center; /* Center the buttons horizontally */
  max-width: 1600px;
  width: 100%; /* Make the container responsive to smaller screens */
  display: flex;
  margin: 0 auto; /* Center the button container horizontally */
}

.fields-container {
  text-align: center; /* Center the buttons horizontally */
  max-width: 800px;
  width: 100%; /* Make the container responsive to smaller screens */
  display: flex;
  justify-content: flex-start; /* Align buttons to the right */
  margin: 0 auto; /* Center the button container horizontally */
}

.fields-container--selection {
  display: inline-block;
  margin-right: 20px;
}

.fields-container--selection label {
  display: block;
  text-transform: uppercase;
  font-size: 0.75rem;
  font-weight: bold;
  text-align: left;
  color: rgb(124, 145, 151);
}

.fields-container--selection select {
  width: 200px;
  height: 30px;
  outline: none;
  cursor: pointer;
  color: white;
  background-color: lightblue;
  border: 1px solid lightblue;
  border-radius: 5px;
  font-weight: bold;
  text-align: center;
}

.buttons-container {
  text-align: center; /* Center the buttons horizontally */
  max-width: 800px;
  width: 100%; /* Make the container responsive to smaller screens */
  display: flex;
  justify-content: flex-end; /* Align buttons to the right */
  margin: 0 auto; /* Center the button container horizontally */
}

.buttons-container button {
  padding: 10px 20px; /* Padding inside the buttons */
  margin-left: 20px;
  background-color: lightblue; /* Button background color */
  color: white; /* Button text color */
  border: none; /* Remove button borders */
  border-radius: 5px; /* Rounded corners for buttons */
  cursor: pointer; /* Change cursor to pointer on hover */
  transition: background-color 0.3s; /* Smooth transition for hover effect */
}

.buttons-container button:hover {
  background-color: blue; /* Darker background color on hover */
}

video {
  width: 1600px; /* Set width */
  height: 700px; /* Set height */
}
</style>
