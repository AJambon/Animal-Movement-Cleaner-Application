<template>
    <div id='import'>
        <h1> Voilà la zone d'import </h1>
          <!--<label for="species"> Species </label>-->
          <textarea id="species" type="text" name="species">3387495879,2015-06-22 12:49:20.000,1.611222,44.801796
3387495880,2015-06-22 12:49:20.250,1.611224,45.801796
3387495881,2015-06-22 12:49:20.500,1.611225,46.801796
3387495882,2015-06-22 12:49:21.000,1.611224,47.801796
3387495883,2015-06-22 12:49:21.250,1.611223,48.801797
3387495884,2015-06-22 12:49:21.500,1.611232,49.801786</textarea>
          <button v-on:click="mysubmit"> Import </button>
    </div>
</template>

<script>
import Vue from 'vue'
import VueResource from 'vue-resource'
Vue.use(VueResource)
export default {
  http: {
    root: 'http://localhost:6543'
  },
  methods: {
    mysubmit () {
      var speciesfromtextarea = document.getElementById('species').value
      var formData = new FormData()
      formData.append('geometry', speciesfromtextarea)
      this.$http.post('backapp',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }).then((response) => {
        this.$root.$emit('eventing', response.data)
      },
      (response) => {
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
