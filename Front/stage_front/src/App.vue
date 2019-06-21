<template>
  <div id="app">
    <visualization></visualization>
    <ImportData></ImportData>
    <Export2 @downloadcsv='ManageData'></Export2>
    <div class="viewer" ref="myViewer">
      <div class="demo-tool">
        <input id = "rd" value="rd" type="checkbox" @change="onChange($event)" v-model="checkedNames" />
        <label for="rd">Raw data</label>
        <input id = "pfd" value="pfd" type="checkbox" @change="onChange($event)" v-model="checkedNames"/>
        <label for="pfd">prefiltereddata</label>
        <input id = "ed" value="ed" type="checkbox" @change="onChange($event)" v-model="checkedNames"/>
        <label for="ed">eliminateddata</label>
        <input id = "fd" value="fd" type="checkbox" @change="onChange($event)" v-model="checkedNames"/>
        <label for="fd">filtereddata</label>
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
    ShowPoints (collection, selection) {
      debugger
      this._myViewer.scene.primitives.add(collection)
      for (var i = 0; i < collection.length; i++) {
        var p = collection.get(i)
        p.show = selection
      }
    },
    onChange (event) {
      var selection = event.target.checked
      var value = event.target.value
      // VOIR POUR ALERTE PARCE QUE CHIANT
      if (this.myRawData === 'undefined' || this.myPrefilteredData === 'undefined') {
        alert('First import data')
      } else {
        if (value === 'rd') {
          this.ShowPoints(this.myRawData, selection)
          this.ShowPoints(this.Rawlines,selection)
        }
        if (value === 'pfd') {
          this.ShowPoints(this.myPrefilteredData, selection)
        }
        if (value === 'ed') {
          this.ShowPoints(this.myEliminatedData, selection)
        }
        if (value === 'fd') {
          this.ShowPoints(this.myfilteredData, selection)
        }
      }
    },
    // function to create the points from imported data
    createPoint (options, color, outlineColor) {
      return new this._myCesium.PointPrimitive(
        {
          id: options.id,
          name: options.id,
          show: false,
          description: 'date et heure:' + options.date + '<BR>' + 'distance 1:' + options.distance1 + '<BR>' + 'distance 2:' + options.distance2,
          color: color,
          outlineColor: outlineColor,
          outlineWidth: 2,
          position: this._myCesium.Cartesian3.fromDegrees(options.LON, options.LAT, 0.0, this._myCesium.Ellipsoid.WGS84),
          date: this._myCesium.JulianDate.fromIso8601(options.date),
          label: options.id
          // point: {
          //   pixelSize: 5,
          //   // color: options.status === 'pending' ? this._myCesium.Color.BLUE : options.status === 'trust' ? this._myCesium.Color.GREEN : this._myCesium.Color.RED,
          //   color: options.status === 'retained' ? this._myCesium.Color.GREEN : options.status === 'pending' ? this._myCesium.Color.RED : this._myCesium.Color.BLUE,
          //   outlineColor: this._myCesium.Color.WHITE,
          //   outlineWidth: 2
          // },
          // label: {
          //   text: options.id,
          //   font: '14pt monospace',
          //   style: this._myCesium.LabelStyle.FILL_AND_OUTLINE,
          //   outlineWidth: 2,
          //   verticalOrigin: this._myCesium.VerticalOrigin.BOTTOM,
          //   pixelOffset: new this._myCesium.Cartesian2(0, -9)
          // }
        }
      )
      // return new this._myCesium.Entity(
      //   {
      //     id: options.id,
      //     name: options.id,
      //     description: 'date et heure:' + options.date + '<BR>' + 'distance 1:' + options.distance1 + '<BR>' + 'distance 2:' + options.distance2,
      //     position: this._myCesium.Cartesian3.fromDegrees(options.LON, options.LAT, 0.0, this._myCesium.Ellipsoid.WGS84),
      //     date: this._myCesium.JulianDate.fromIso8601(options.date),
      //     point: {
      //       pixelSize: 5,
      //       // color: options.status === 'pending' ? this._myCesium.Color.BLUE : options.status === 'trust' ? this._myCesium.Color.GREEN : this._myCesium.Color.RED,
      //       color: options.status === 'trust' ? this._myCesium.Color.GREEN : options.status === 'pending' ? this._myCesium.Color.RED : this._myCesium.Color.BLUE,
      //       outlineColor: this._myCesium.Color.WHITE,
      //       outlineWidth: 2
      //     },
      //     label: {
      //       text: options.id,
      //       font: '14pt monospace',
      //       style: this._myCesium.LabelStyle.FILL_AND_OUTLINE,
      //       outlineWidth: 2,
      //       verticalOrigin: this._myCesium.VerticalOrigin.BOTTOM,
      //       pixelOffset: new this._myCesium.Cartesian2(0, -9)
      //     }
      //   }
      // )
    },
    CreatePolylines (collection,object) {
      for (var i = 0; i < collection.length-1; i++) {
        var p = collection.get(i)
        var q = collection.get(i+1)
        var lonp = this._myCesium.Math.toDegrees(p.position.x)
        var latp = this._myCesium.Math.toDegrees(p.position.y)
        var lonq = this._myCesium.Math.toDegrees(p.position.x)
        var latq = this._myCesium.Math.toDegrees(p.position.y)
        console.log(lonp,latp)
        // object.add({
        //   parent: object,
        //   position: this._myCesium.Cartesian3.fromDegrees(lonq, latp),
        //   polyline: {
        //     positions: [
        //       this._myCesium.Cartesian3.fromDegrees(lonq , latp),
        //       this._myCesium.Cartesian3.fromDegrees(lonq, latq),
        //     ],
        //     width: new this._myCesium.ConstantProperty(2),
        //     material: this._myCesium.Color.RED,
        //     followSurface: new this._myCesium.ConstantProperty(true)
        //   }
        // })
      }
    },
    //   for (var itf = 0; itf < data[3].length - 1; itf++)
    //         this._myViewer.scene.primitives.add(collection)
      //   _this._myViewer.entities.add({
      //     parent: _this.fpolylines,
      //     position: _this._myCesium.Cartesian3.fromDegrees(data[3][itf].LON, data[3][itf].LAT),
      //     polyline: {
      //       positions: [
      //         _this._myCesium.Cartesian3.fromDegrees(data[3][itf].LON, data[3][itf].LAT),
      //         _this._myCesium.Cartesian3.fromDegrees(data[3][itf + 1].LON, data[3][itf + 1].LAT)
      //       ],
      //       width: new _this._myCesium.ConstantProperty(2),
      //       material: _this._myCesium.Color.RED,
      //       followSurface: new _this._myCesium.ConstantProperty(true)
      //     }
      //   })
    // },
    // function to display points from a set of data
    parseData (dataCollection) {
      for (var item in dataCollection) {
        var tmpPoint = this.createPoint(dataCollection[item])
        this._myViewer.entities.add(tmpPoint)
      }
    },
    ready (cesiumInstance) {
      const { Cesium, viewer, Ellipsoid } = cesiumInstance
      this._myCesium = Cesium
      this._myViewer = viewer
      this._myEllispoid = Ellipsoid
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
        console.log('data avant remove', _this.myPrefilteredData)
        _this.myPrefilteredData.entities.remove(entity)
        console.log('data apres remove', _this.myPrefilteredData)
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
      if (typeof (this.myPrefilteredData) === 'undefined') {
        alert('Import data first')
      } else {
        console.log('je genere les data a transformer depuis managedata', this.myPrefilteredData.entities.values)
        var dataPoints = []
        for (var i = 0; i < this.myPrefilteredData.entities.values.length; i++) {
          var item = this.myPrefilteredData.entities.values[i]
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
      // Creating Collections of points
      _this.myRawData = new _this._myCesium.PointPrimitiveCollection('my raw data') // new _this._myCesium.CustomDataSource('my raw data')
      _this.myPrefilteredData = new _this._myCesium.PointPrimitiveCollection('my prefiltered data')
      _this.myEliminatedData = new _this._myCesium.PointPrimitiveCollection('my eliminated data')
      _this.myfilteredData = new _this._myCesium.PointPrimitiveCollection('my filtered data')
      // To add data to points collections
      for (var itr in data[0]) {
        _this.myRawData.add(_this.createPoint(data[0][itr], this._myCesium.Color.BLUE, this._myCesium.Color.WHITE))
      }
      for (var itp in data[1]) {
        _this.myPrefilteredData.add(_this.createPoint(data[1][itp], this._myCesium.Color.GREY, this._myCesium.Color.WHITE))
      }
      for (var ite in data[2]) {
        _this.myEliminatedData.add(_this.createPoint(data[2][ite], this._myCesium.Color.RED, this._myCesium.Color.WHITE))
      }
      for (var itf = 0; itf < data[3].length - 1; itf++) {
      //   _this.fpolylines = _this._myViewer.entities.add(new _this._myCesium.Entity()) // to create segments between consecutive points
        _this.myfilteredData.add(_this.createPoint(data[3][itf], this._myCesium.Color.GREEN, this._myCesium.Color.WHITE)) // to create points
      
      // To create lines 
      _this.Rawlines = new _this._myCesium.PolylineCollection()
      _this.CreatePolylines (_this.myRawData,_this.Rawlines)
      }
    })
    // _this.$root.$on('downloadcsv', flag => {

    //   console.log('je genere les data a transformer', _this.myPrefilteredData)
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
