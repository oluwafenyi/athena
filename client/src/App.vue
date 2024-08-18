<script>
import VideoContainer from './components/VideoContainer.vue'
import axios from 'axios'
import { useToast } from 'vue-toastification'
import Loading from 'vue-loading-overlay'

export default {
  setup() {
    const toast = useToast()
    return { toast }
  },
  methods: {
    receiveInputVideo(data, filename) {
      this.inputVideoDataUrl = data
      this.inputFileName = filename
    },
    receiveLanguageCode(data, sourceOrTarget) {
      if (sourceOrTarget == 'source') {
        this.sourceLanguageCode = data
      }

      if (sourceOrTarget == 'target') {
        this.targetLanguageCode = data
      }
    },
    async translateVideo() {
      if (this.sourceLanguageCode === null || this.targetLanguageCode === null) {
        return this.toast.error('Please select both source and target language.')
      }

      if (this.sourceLanguageCode === this.targetLanguageCode) {
        return this.toast.error('Source and target language cannot be the same value.')
      }

      if (this.inputVideoDataUrl === null) {
        return this.toast.error('Please select an input video.')
      }

      this.isLoading = true
      const videoBlob = this.dataURLToBlob(this.inputVideoDataUrl)

      const formData = new FormData()
      formData.append('video_file', videoBlob, this.inputFileName)
      formData.append('source_language_code', this.sourceLanguageCode)
      formData.append('target_language_code', this.targetLanguageCode)
      try {
        const response = await axios.post('http://localhost:8000/translate/', formData, {
          responseType: 'blob'
        })
        console.log(response)
        this.translatedVideoDataUrl = await this.blobToDataURL(response.data)
        const responseFileName = this.getResponseFileName(response)
        if (responseFileName) {
          this.translatedVideoName
        }

        await this.$nextTick();
        const element = document.getElementById('output');
        if (element) {
          element.scrollIntoView({ behavior: 'smooth' });
        }
      } catch (error) {
        console.log(error)
        this.toast.error('An error occurred with the translation request.')
      }
      this.isLoading = false
    },
    dataURLToBlob(dataURL) {
      const [header, base64] = dataURL.split(',')
      const mime = header.match(/:(.*?);/)[1]
      const binary = atob(base64)
      const arrayBuffer = new ArrayBuffer(binary.length)
      const uint8Array = new Uint8Array(arrayBuffer)

      for (let i = 0; i < binary.length; i++) {
        uint8Array[i] = binary.charCodeAt(i)
      }

      return new Blob([arrayBuffer], { type: mime })
    },
    getResponseFileName(response) {
      const contentDisposition = response.headers['content-disposition']
      let filename = null

      if (contentDisposition) {
        const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/)
        if (filenameMatch && filenameMatch[1]) {
          filename = filenameMatch[1].replace(/['"]/g, '') // Remove quotes around filename
        }
      }
      return filename
    },
    async blobToDataURL(blob) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()

        reader.onloadend = function () {
          resolve(reader.result)
        }

        reader.onerror = function (error) {
          reject(error)
        }

        reader.readAsDataURL(blob)
      })
    }
  },
  data() {
    return {
      inputVideoDataUrl: null,
      inputFileName: null,
      translatedVideoDataUrl: null,
      translatedVideoName: null,
      sourceLanguageCode: null,
      targetLanguageCode: null,
      isLoading: false
    }
  },
  components: {
    VideoContainer,
    Loading
  }
}
</script>

<template>
  <main>
    <Loading
      v-model:active="isLoading"
      :can-cancel="false"
      color="blue"
      background-color="lightblue"
    />

    <VideoContainer id="input"
      @inputVideoUpdate="receiveInputVideo"
      @languageSelectionUpdate="receiveLanguageCode"
      @translateVideo="translateVideo"
      :videoDataUrl="inputVideoDataUrl"
      forUpload
    />

    <VideoContainer id="output" v-if="translatedVideoDataUrl !== null" :videoDataUrl="translatedVideoDataUrl" :videoFileName="translatedVideoName" />
  </main>
</template>

<style scoped></style>
