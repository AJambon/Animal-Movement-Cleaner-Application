<template>
    <div id='import' class='col-4'>
        <!-- <h1> Voilà la zone d'import </h1> -->
            <div class="fields">
              <!-- <label>Upload File</label><br/> -->
              <button>
                <label for="csv-file">Choose your file</label>
              </button>
              <input id="csv-file" name="newcsv" type="file" ref="file" accept=".csv" v-on:change="onSelect()"/>
              <!-- <b-form-file v-model="file" :state="Boolean(file)" placeholder="Choose a file or drop it here..." drop-placeholder="Drop file here..."
              ></b-form-file> -->
            </div>
            <div class="message">
              <h5>{{message}}</h5>
            </div>
          <textarea id="byhand" type="text" name="species"></textarea>
          <button v-on:click="submit ? UpdateData() : mysubmit()"> Import </button>
    </div>
</template>

<script>
import Vue from 'vue'
import VueResource from 'vue-resource'
import BootstrapVue from 'bootstrap-vue'
import { EventBusParameters } from '../../main'
import {myConfig} from '../../config'

Vue.use(BootstrapVue)
Vue.use(VueResource)
export default {
  http: {
    root: myConfig.apiUrl
  },
  data () {
    return {
      file: '',
      message: '',
      parameters: null,
      loading: false,
      submit: false,
      submit1: []
    }
  },
  created () {
    EventBusParameters.$on('ParamsSelect', (data) => { // to get parameters entrered in Parameters component
      this.parameters = data
    })
  },
  methods: {
    UpdateData () {
      if (this.submit === true) {
        if (confirm('You are going to loose current data, do you still want to proceed ?')) {
          this.$emit('UpdateData', true)
          this.mysubmit()
        } else {
          console.log('cancel')
        }
      }
    },
    onSelect () {
      const file = this.$refs.file.files[0]
      this.file = file
      console.log(file)
    },
    mysubmit () {
      if (this.parameters === null) {
        alert('First enter parameters corresponding to your dataset')
      } else {
        this.$emit('loading', true)
        var speciesfromtextarea = document.getElementById('byhand').value
        var parametersToSend = JSON.stringify(this.parameters)
        if (typeof (this.file) === 'object') {
          const formData = new FormData()
          formData.append('file', this.file)
          formData.append('parameters', parametersToSend)
          this.$http.post('upload',
            formData,
            {
              headers: {
                'Content-Type': 'multipart/form-data'
              }
            }
          ).then((response) => {
            console.log('SUCCESS!!')
            this.submit = true
            this.$root.$emit('eventing', response.data)
          })
            .catch(function () {
              console.log('FAILURE!!')
            })
        } else {
          if (speciesfromtextarea !== '') {
            var formData = new FormData()
            formData.append('geometry', speciesfromtextarea)
            formData.append('parameters', parametersToSend)
            this.$http.post('backapp',
              formData,
              {
                headers: {
                  'Content-Type': 'multipart/form-data'
                }
              }).then((response) => {
              this.submit = true
              this.$root.$emit('eventing', response.data)
            },
            (response) => {
              console.log('erreur', response)
            }
            )
          } else {
            alert('First choose a file or enter data')
          }
        }
      }
    }
  },
  mounted () {
    var _this = this
    this.$root.$on('NoUpdate', data => {
      _this.submit = data
    })
  }
}
</script>

<style scoped>
h1{
  font-weight: normal;
}
</style>
