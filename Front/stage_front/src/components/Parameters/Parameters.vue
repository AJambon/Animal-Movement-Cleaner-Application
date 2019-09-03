<template>
    <div id='parameters' class='col-4'>
      <div id='technology'>
        <h2 v-b-toggle.collapse variant="primary">Parameters and file</h2>
        <b-collapse id="collapse" visible>
          <b-form id='p'>
            <div>
              <label>Technology</label>
              <b-form-select v-model="parameters.technology" @change="parametersSelection">
                <option :value="null">Please select a technology</option>
                <option value="argos">ARGOS</option>
                <option value="gps">GPS</option>
              </b-form-select>
            </div>
            <div>
              <label>Type of species</label>
              <b-form-select v-model="parameters.speciesType" @change="parametersSelection">
                <option :value="null">Please select a type of species</option>
                <option value="Terrestrian">Terrestrian</option>
                <option value="Avian">Avian</option>
                <option value="Aquatic">Aquatic</option>
              </b-form-select>
            </div>
            <div>
              <label>Species</label>
              <b-form-input id="species" v-model="parameters.species" required placeholder="Enter species" @change="parametersSelection"></b-form-input>
            </div>
            <div>
              <label>Deployment date</label>
              <b-form-input id="deployment_date" type = "datetime-local" v-model="parameters.deploymentDate" @change="parametersSelection"></b-form-input>
            </div>
            <div>
              <label>Species max speed (km/h)</label>
              <!-- <b-form-input id="species" v-model="parameters.species" required placeholder="Enter species" @change="parametersSelection"></b-form-input> -->
              <b-form-input id="max_speed" v-model="parameters.speed" required placeholder="Enter species max speed" @change="parametersSelection"></b-form-input>
              <label>Immobility min. duration (h)</label>
              <b-form-input id="immo_time" v-model="parameters.immoTime" required placeholder="Enter minimum immobility duration to consider it as immobility detection" @change="parametersSelection"></b-form-input>
            </div>
            <b-button @click="csvPattern">Download CSV pattern</b-button>
          </b-form>
        </b-collapse>
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
        speciesType: 'Avian',
        species: 'EV',
        speed: '300',
        immoTime: '24',
        deploymentDate:"2012-04-17T08:00"
      }
    }
  },
  methods: {
    parametersSelection () {
      EventBusParameters.$emit('ParamsSelect', this.parameters)
    },
    csvPattern() {
      console.log('ok')
      var mandatoryColumns = ['event-id','timestamp','location-lat','location-long','elevation(optional)','HDOP(optional)','info(optional)']
      var separator = ';'
      var headers = mandatoryColumns.join(separator)
      headers += '\n'
      var ligne = ''
      this.myCSV = headers
      var hiddenElement = document.createElement('a')
      hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(this.myCSV)
      hiddenElement.target = '_blank'
      hiddenElement.download = 'csv_pattern.csv'
      document.body.appendChild(hiddenElement)
      hiddenElement.click()
      document.body.removeChild(hiddenElement)
    }
  },
  mounted () {
    this.parametersSelection()
    // this.csvPattern()
  }
}
</script>

<style scoped>
h1
{
  font-weight: normal;
}
</style>
