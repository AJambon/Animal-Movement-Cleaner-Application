<template>
  <div id='export'>
    <button v-on:click="download_csv">Download CSV</button>
  </div>
</template>

<script>

export default {
  methods: {
    download_csv () {
      this.$emit('downloadcsv', true)
      if (typeof (this.myCSV) === 'undefined') {
        alert('Import data first')
      }
      // to create csv file
      var hiddenElement = document.createElement('a')
      hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(this.myCSV)
      hiddenElement.target = '_blank'
      hiddenElement.download = 'locationsanalysed.csv'
      document.body.appendChild(hiddenElement)
      hiddenElement.click()
      document.body.removeChild(hiddenElement)
    }
  },
  mounted () {
    // to get data from back
    this.$root.$on('CSVtodownload', dataPoints => {
      // console.log('databrut', data[0])
      var mandatoryColumns = ['id', 'date', 'LON', 'LAT', 'elevation', 'HDOP', 'info']
      var separator = ';'
      var headers = mandatoryColumns.join(separator)
      headers += '\n'
      var ligne = ''
      for (var item in dataPoints) {
        var ligneTmp = ''
        for (var col of mandatoryColumns) {
          // console.log(col)
          if (col in dataPoints[item]) {
            ligneTmp += dataPoints[item][col]
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
      // console.log(this.myCSV)
    })
  }
}
</script>

<style>
</style>
