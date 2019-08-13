<template>
    <div id='parameters'>
      <div id='technology'>
        <h1> Parameters </h1>
        <b-form id='p'>
          <b-form-select v-model="parameters.technology" @change="parametersSelection" class="mb-3">
            <option :value="null">Please select a technology</option>
            <option value="argos">ARGOS</option>
            <option value="gps">GPS</option>
          <!--  <option value="b" disabled>Option B (disabled)</option> -->
            <!-- <optgroup label="Grouped Options">
              <option :value="{ C: '3PO' }">Option with object value</option>
              <option :value="{ R: '2D2' }">Another option with object value</option>
            </optgroup> -->
          </b-form-select>
          <b-form-input id="species" v-model="parameters.species" required placeholder="Enter species" @change="parametersSelection"></b-form-input>
          <b-form-input id="max_speed" v-model="parameters.speed" required placeholder="Enter species max speed" @change="parametersSelection"></b-form-input>
          <b-form-input id="immo_time" v-model="parameters.immoTime" required placeholder="Enter minimum immobility duration to consider it as immobility detection" @change="parametersSelection"></b-form-input>
        </b-form>
      </div>
    </div>
</template>

<script>
import Vue from 'vue'
import VueResource from 'vue-resource'
import BootstrapVue from 'bootstrap-vue'
import { EventBusParameters } from '../../main'

Vue.use(BootstrapVue)
Vue.use(VueResource)

export default {
  data () {
    return {
      test: 2,
      parameters: {
        technology: 'gps',
        species: 'EV',
        speed: '52',
        immoTime: '24'
      }
    }
  },
  methods: {
    parametersSelection () {
      EventBusParameters.$emit('ParamsSelect', this.parameters)
    }
  },
  mounted () {
    this.parametersSelection()
  }
}
</script>

<style scoped>
h1
{
  font-weight: normal;
}
</style>
