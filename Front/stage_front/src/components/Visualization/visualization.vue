<template>
  <header>
    <h1>Animal Movement Cleaner Application</h1>
    <div>
      <b-button id="show-btn" @click="$bvModal.show('bv-modal-example')">HELP</b-button>

      <b-modal id="bv-modal-example" hide-footer>
        <template v-slot:modal-title>
          Help
        </template>
        <div class="d-block text-center">
          <h3>Here are several information about what can be done with Animal Movement Application</h3>
        </div>
        <b-button class="mt-3" block @click="$bvModal.hide('bv-modal-example')">Close</b-button>
      </b-modal>
      <!-- <b-button v-b-modal.modal-1>HELP</b-button>
      <b-modal id="modal-1" title="BootstrapVue">
        <p class="my-4">Here are several information about what can be done with Animal Movement Application</p>
      </b-modal> -->
    </div>
    <!-- <a href="#">
      HELP
    </a> -->
  </header>
</template>

<script>
import Vue from 'vue'
import VueCesium from 'vue-cesium'
// Vue-Cesium will load Cesium.js from `https://unpkg.com/cesium/Build/Cesium/Cesium.js`
Vue.use(VueCesium, {
  // cesiumPath is path of Cesium.js', for example:
  // local Cesium Build package:
  // cesiumPath: './static/Cesium/Cesium.js'
  // Official Online Cesium Build package：
  cesiumPath: 'https://unpkg.com/cesium/Build/Cesium/Cesium.js'
})
export default{
}
</script>

<style>
header:not(.modal-header){
  background: #111;
  padding: 0px;
  text-align: left;
  color: #6eb0ed;
  display: inline-flex;
  justify-content: space-between;
  width: 100%;
  position: fixed;
  left: 0;
  top: 0;
  right: 0;
  z-index: 9999;
  max-height: 56px !important;
}
header h1{
  font-size: 2em;
  padding: 10px 20px;
  margin: 0px;
}
header div button{
  background-color: #1b568c !important;
  color: #fff;
  font-weight: bold;
  padding: 0px 50px !important;
  display: flex !important;
  align-items: center !important;
  height: 100%;
  border-radius: 0px !important;
  border: none !important;
}
header div button:hover{
  background-color: #2367a5 !important;
  text-decoration: none;
}
.modal-dialog{
  margin-top: 87px;
}

.modal-dialog .modal-header button{
  width: inherit;
  box-shadow: inherit;
}

.modal-dialog .modal-body h3{
  font-size: 1.2em;
}

.modal-dialog #show-btn{
  display: none;
  }
</style>
