<template>
  <div id="app">
    <visualization></visualization>
    <ImportData></ImportData>
    <Export2 @downloadcsv='ManageData'></Export2>
    <div class="viewer" ref="myViewer">
      <div class="demo-tool">
        <input id = "rd" value="rd" type="checkbox" @change="onChange($event)" v-model="checkedNames" />
        <label for="rd">Raw data</label>
        <input id = "ad" value="ad" type="checkbox" @change="onChange($event)" v-model="checkedNames"/>
        <label for="ad">analyzeddata</label>
        <button v-on:click="remove_point">Remove point</button>
      </div>
      <cesium-viewer :animation="animation" :camera="camera" :fullscreenButton="fullscreenButton" @ready="ready">
      </cesium-viewer>
    </div>
  </div>
</template>

<script>
import visualization from './components/Visualization/visualization.vue'
import ImportData from './components/Import/ImportData.vue'
import Export2 from './components/Export/Export2.vue'
import VueCesium from 'vue-cesium'
import Vue from 'vue'

Vue.use(VueCesium, {
  // local Cesium Build package:
  // cesiumPath: './static/Cesium/Cesium.js'
  // Official Online Cesium Build package：
  cesiumPath: 'https://unpkg.com/cesium/Build/Cesium/Cesium.js'
})

export default {
  name: 'App',
  components: {
    visualization,
    ImportData,
    Export2
  },
  data () {
    // Cesium.BingMapsApi.defaultKey = 'AgqG7d1hd0psBdMyO3kPG8COGLUqA7knynwLSBkjiBRAnvRfOaOv1ZEl3GsDutjC'// ma key
    return {
      animation: true,
      fullscreenButton: true,
      checkedNames: [],
      camera: {
        position: {
          longitude: 5.369222,
          latitude: 43.292770,
          height: 20000000
        },
        heading: 360,
        pitch: -90,
        roll: 0
      }
    }
  },
  methods: {
    onChange (event) {
      var selection = event.target.checked
      var value = event.target.value
      // VOIR POUR ALERTE PARCE QUE CHIANT
      if (this.myRawData === 'undefined' || this.myAnalyzedData === 'undefined') {
        alert('First import data')
      } else {
        if (value === 'rd') {
          if (selection === true) {
            this._myViewer.dataSources.add(this.myRawData)
          } else {
            this._myViewer.dataSources.remove(this.myRawData)
          }
        }
        if (value === 'ad') {
          if (selection === true) {
            this._myViewer.dataSources.add(this.myAnalyzedData)
          } else {
            this._myViewer.dataSources.remove(this.myAnalyzedData)
          }
        }
      }
    },
    // function to create the points from imported data
    createPoint (options) {
      return new this._myCesium.Entity(
        {
          id: options.id,
          name: options.id,
          description: options.date,
          position: this._myCesium.Cartesian3.fromDegrees(options.LON, options.LAT, 0.0, this._myCesium.Ellipsoid.WGS84),
          date: this._myCesium.JulianDate.fromIso8601(options.date),
          point: {
            pixelSize: 5,
            color: typeof (options.status) === 'undefined' ? this._myCesium.Color.BLUE : (options.status === 'kept') ? this._myCesium.Color.GREEN : this._myCesium.Color.RED,
            outlineColor: this._myCesium.Color.WHITE,
            outlineWidth: 2
          },
          label: {
            text: options.id,
            font: '14pt monospace',
            style: this._myCesium.LabelStyle.FILL_AND_OUTLINE,
            outlineWidth: 2,
            verticalOrigin: this._myCesium.VerticalOrigin.BOTTOM,
            pixelOffset: new this._myCesium.Cartesian2(0, -9)
          }
        }
      )
    },
    // function to display points from a set of data
    parseData (dataCollection) {
      for (var item in dataCollection) {
        var tmpPoint = this.createPoint(dataCollection[item])
        this._myViewer.entities.add(tmpPoint)
      }
    },
    ready (cesiumInstance) {
      const { Cesium, viewer } = cesiumInstance
      this._myCesium = Cesium
      this._myViewer = viewer
      // key linked to cesium ion account
      Cesium.Ion.defaultAccessToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJmZTcyOGI0MC1lYzIzLTQwMmQtYTIyNC0zYzUzODc1MDY3YjkiLCJpZCI6MTA0NTUsInNjb3BlcyI6WyJhc2wiLCJhc3IiLCJhc3ciLCJnYyJdLCJpYXQiOjE1NTg1MTU4MDd9.3gdYw0YfxkUkxTAre3lLXCvQsv6rKvW4yBiy27MFGlg'
      // Change imagery layer
      this._myViewer.imageryLayers.remove(this._myViewer.imageryLayers.get(0))
      this._myViewer.imageryLayers.addImageryProvider(new Cesium.IonImageryProvider({ assetId: 2 }))
      // function to modify a selected point
      // var _this = this
      // var SelectedPoint = ''
      // this._myViewer.selectedEntityChanged.addEventListener(function (entity) {
      //   var SelectedPoint = viewer.selectedEntity
      //   console.log('point selectionné', SelectedPoint.id)
      /* if (entity) {
        console.log(entity)
        console.log('data avant remove', _this.myAnalyzedData)
        _this.myAnalyzedData.entities.remove(entity)
        console.log('data apres remove', _this.myAnalyzedData)
      } */
      // })
      // this.parseData(dataTest, viewer, Cesium)
      // Add points

      // viewer.entities.add({
      //   id: '01',
      //   position: Cesium.Cartesian3.fromDegrees(5.369222, 43.292770),
      //   // image for point
      //   billboard: new Cesium.BillboardGraphics({
      //     image: '/static/Assets/Bird.png',
      //     scale: 0.2
      //   }),
      //   /* point : {
      //     pixelSize : 5,
      //     color : Cesium.Color.RED,
      //     outlineColor : Cesium.Color.WHITE,
      //     outlineWidth : 2
      //   },  */
      //   label: {
      //     text: 'Vautour1',
      //     font: '14pt monospace',
      //     style: Cesium.LabelStyle.FILL_AND_OUTLINE,
      //     outlineWidth: 2,
      //     verticalOrigin: Cesium.VerticalOrigin.BOTTOM,
      //     pixelOffset: new Cesium.Cartesian2(0, -9)
      //   }
      // })

      // viewer.zoomTo(viewer.entities);
      /* this.camera.position.longitude = 5.369222
      this.camera.position.latitude = 43.292770
      this.camera.position.height = 10000000
      this.animation = true */
    },
    remove_point () {
      var SelectedPoint = this._myViewer.selectedEntity
      // console.log('on est dans remove_point', SelectedPoint)
      SelectedPoint.entityCollection.remove(SelectedPoint)
    },
    // Function to give data from entitescollections same shape as backapp and then send it to export2
    ManageData () {
      if (typeof (this.myAnalyzedData) === 'undefined') {
        alert('Import data first')
      } else {
        console.log('je genere les data a transformer depuis managedata', this.myAnalyzedData.entities.values)
        var dataPoints = []
        for (var i = 0; i < this.myAnalyzedData.entities.values.length; i++) {
          var item = this.myAnalyzedData.entities.values[i]
          var curPosition = item.position.getValue()
          var carto = this._myCesium.Ellipsoid.WGS84.cartesianToCartographic(curPosition)
          var lon = this._myCesium.Math.toDegrees(carto.longitude)
          var lat = this._myCesium.Math.toDegrees(carto.latitude)
          var height = this._myCesium.Math.toDegrees(carto.height)
          var date = this._myCesium.JulianDate.toIso8601(item._date) // VOIR SOUCI DE DATE
          // var date = this._myCesium.JulianDate.toDate(item._date)
          dataPoints.push({
            id: item._id,
            date: date,
            LON: lon,
            LAT: lat,
            elevation: height
          })
        }
        console.log(dataPoints)
        this.$root.$emit('CSVtodownload', dataPoints)
      }
    }
  },
  mounted () {
    var _this = this
    // MODIFIER AVEC THIS.EMIT DANS ImportData ET EVENT LISTENER DANS APP avec fonction https://www.telerik.com/blogs/how-to-emit-data-in-vue-beyond-the-vuejs-documentation
    _this.$root.$on('eventing', data => {
      // Creates an EntityCollection
      _this.myRawData = new _this._myCesium.CustomDataSource('my raw data')
      // To add to the EntityCollection
      for (var it in data[0]) {
        _this.myRawData.entities.add(_this.createPoint(data[0][it]))
      }
      _this.myAnalyzedData = new _this._myCesium.CustomDataSource('my analyzed data')
      for (var ite in data[1]) {
        _this.myAnalyzedData.entities.add(_this.createPoint(data[1][ite]))
      }
    })
    // _this.$root.$on('downloadcsv', flag => {

    //   console.log('je genere les data a transformer', _this.myAnalyzedData)
    //   // TODO recuperer et transormer la collection

    //   this.$root.$emit('CSVtodownload', true)
    // })
  }}
</script>

<style>
.viewer {
  width: 100%;
  height: 800px;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
