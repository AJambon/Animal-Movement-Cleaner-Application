<template>
  <div id='export'>
    <button v-on:click="download_csv">Download CSV</button>
  </div>
</template>

<script>

export default {
  methods: {
    download_csv () {
      this.$root.$emit('downloadcsv', true)
      if (typeof (this.myCSV) === 'undefined') {
        alert('Import data first')
      }
      // to create csv file
      // var hiddenElement = document.createElement('a')
      // hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(this.myCSV)
      // hiddenElement.target = '_blank'
      // hiddenElement.download = 'locationsanalysed.csv'
      // document.body.appendChild(hiddenElement)
      // hiddenElement.click()
      // document.body.removeChild(hiddenElement)
    }
  },
  mounted () {
    // to get data from back
    this.$root.$on('eventing', data => {
      // console.log('databrut', data[0])
      var mandatoryColumns = ['id', 'date', 'LON', 'LAT']
      var separator = ';'
      var headers = mandatoryColumns.join(separator)
      headers += '\n'
      var ligne = ''
      for (var item in data[0]) {
        var ligneTmp = ''
        for (var col of mandatoryColumns) {
          // console.log(col)
          if (col in data[0][item]) {
            ligneTmp += data[0][item][col]
          } else {
            ligneTmp += ''
          }
          ligneTmp += separator
        }
        ligneTmp += '\n'
        ligne += ligneTmp
      }
      // to fill csv file
      this.myCSV = headers + ligne
    })
  }
}
</script>

<style>
</style>
