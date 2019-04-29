<template>
    <div id='import'>
        <h1> Voilà la zone d'import </h1>
            <label for="species"> Species </label>
            <textarea id="species" v-model="species" type="text" name="species"/>
            <button v-on:click="mysubmit"> Import </button>
    </div>
</template>

<script>
import Vue from 'vue'
import VueResource from 'vue-resource'
Vue.use(VueResource)
export default {
  /* data: function () {
    return {
      species: ''
    }
  }, */
  http: {
    root: 'http://localhost:6543'
  },
  methods: {
    mysubmit () {
      var species = document.getElementById('species').value
      var formData = new FormData()
      formData.append('geometry', species)
      this.$http.post('backapp',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }).then((response) => {
        this.citizens = response.data
      }, (response) => {
        console.log('erreur', response)
      }
      )
    }
  }
}
</script>

<style scoped>
h1{
  font-weight: normal;
}
</style>
