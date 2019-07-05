<template>
  <div id="app">
    <visualization></visualization>
    <ImportData @UpdateData='cleanCollection'></ImportData>
    <Export2 @downloadcsv='ManageData'></Export2>
    <div class="viewer" ref="myViewer">
      <div id="interact_data" class="demo-tool">
        <!-- :disabled="event.target.checked ? false : true" -->
        <!-- @change.stop="alert('import data')" -->
        <!-- v-if="seen" -->
        <div  v-if="displayCheckbox">
          <input id = "rd" value="rd" type="checkbox" @change="onChange($event)" v-model="checkedNames" />
          <label for="rd">Raw data</label>
          <input id = "id" value="id" type="checkbox" @change="onChange($event)" v-model="checkedNames" />
          <label for="id">Impossible data</label>
          <input id = "pfd" value="pfd" type="checkbox" @change="onChange($event)" v-model="checkedNames"/>
          <label for="pfd">prefiltereddata</label>
          <input id = "ed" value="ed" type="checkbox" @change="onChange($event)" v-model="checkedNames"/>
          <label for="ed">eliminateddata</label>
          <input id = "fd" value="fd" type="checkbox" @change="onChange($event)" v-model="checkedNames"/>
          <label for="fd">filtereddata</label>
          <button v-on:click="remove_point" >Remove point</button>
          <div id='params'>
            <input id = "3DT" value="3DT" type="checkbox" @change="onChange($event)"/>
            <label for="3DT">Terrain transparency</label>
          </div>
        </div>
      </div>
       <input type="checkbox" id='timelinedisplay' v-model="timeline"/>
      <label for="timelinedisplay">Time line</label>
      <cesium-viewer :animation="animation" @Tick="Tick" :camera="camera" :fullscreenButton="fullscreenButton" :timeline="timeline" @ready="ready">
      <cesium-terrain-provider></cesium-terrain-provider>
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
// import { debuglog } from 'util';

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
      timeline: true,
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
      },
      displayCheckbox: false
    }
  },
  methods: {
    ShowOptions (Option, value, selection) {
      if (value === Option) {
        this._myViewer.scene.globe.depthTestAgainstTerrain = selection // to remove transparency from 3D layer
      }
    },
    ShowPoints (collection, selection) {
      this._myViewer.scene.primitives.add(collection)
      for (var i = 0; i < collection.length; i++) {
        var p = collection.get(i)
        p.show = selection
      }
    },
    onChange (event) {
      var selection = event.target.checked
      var value = event.target.value
      this.ShowOptions('3DT', value, selection)
      if (typeof (this.myRawDataPrimitive) === 'undefined' || typeof (this.myEliminatedDataPrimitive) === 'undefined' || typeof (this.myPrefilteredDataPrimitive) === 'undefined' || typeof (this.myfilteredDataPrimitive) === 'undefined') {
        alert('First import data')
      } else {
        if (value === 'rd') {
          this.ShowPoints(this.myRawDataPrimitive, selection)
          this.ShowPoints(this.Rawlines, selection)
        }
        if (value === 'id') {
          this.ShowPoints(this.myImpossibleDataPrimitive, selection)
        }
        if (value === 'pfd') {
          this.ShowPoints(this.myPrefilteredDataPrimitive, selection)
        }
        if (value === 'ed') {
          this.ShowPoints(this.myEliminatedDataPrimitive, selection)
        }
        if (value === 'fd') {
          this.ShowPoints(this.myfilteredDataPrimitive, selection)
        }
      }
    },
    // function to create the points from imported data
    createPointPrimitive (options, color, outlineColor) {
      return new this._myCesium.PointPrimitive(
        {
          id: options.id,
          name: options.id,
          show: false,
          allowPicking: true,
          description: 'date et heure:' + options.date + '<BR>' + 'distance 1:' + options.distance1 + '<BR>' + 'distance 2:' + options.distance2,
          color: this._myCesium.Color.fromRgba(color),
          outlineColor: this._myCesium.Color.fromRgba(outlineColor),
          outlineWidth: 2,
          position: this._myCesium.Cartesian3.fromDegrees(options.LON, options.LAT, options.elevation, this._myCesium.Ellipsoid.WGS84)
        }
      )
    },
    createPointEntity (options, color, outlineColor) {
      return new this._myCesium.Entity(
        {
          id: options.id,
          name: options.id,
          description: 'date et heure:' + options.date + '<BR>' + 'distance 1:' + options.distance1 + '<BR>' + 'distance 2:' + options.distance2,
          position: this._myCesium.Cartesian3.fromDegrees(options.LON, options.LAT, options.elevation, this._myCesium.Ellipsoid.WGS84),
          date: this._myCesium.JulianDate.fromIso8601(options.date),
          point: {
            pixelSize: 5,
            color: this._myCesium.Color.fromRgba(color),
            outlineColor: this._myCesium.Color.fromRgba(outlineColor),
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
    CreatePolylines (collection, object) {
      // for (var i = 0; i < collection.length - 1; i++) {
      // var p = collection.get(i)
      // var q = collection.get(i+1)
      // var lonp = this._myCesium.Math.toDegrees(p.position.x)
      // var latp = this._myCesium.Math.toDegrees(p.position.y)
      // var lonq = this._myCesium.Math.toDegrees(p.position.x)
      // var latq = this._myCesium.Math.toDegrees(p.position.y)
      // console.log(lonp,latp)
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
      // }
    },
    //   for (var itf = 0; itf < data[3].length - 1; itf++)
    //     this._myViewer.scene.primitives.add(collection)
    //   _this._myViewer.entities.add({
    //   parent: _this.fpolylines,
    //   position: _this._myCesium.Cartesian3.fromDegrees(data[3][itf].LON, data[3][itf].LAT),
    //   polyline: {
    //     positions: [
    //       _this._myCesium.Cartesian3.fromDegrees(data[3][itf].LON, data[3][itf].LAT),
    //       _this._myCesium.Cartesian3.fromDegrees(data[3][itf + 1].LON, data[3][itf + 1].LAT)
    //     ],
    //     width: new _this._myCesium.ConstantProperty(2),
    //     material: _this._myCesium.Color.RED,
    //     followSurface: new _this._myCesium.ConstantProperty(true)
    //   }
    // })
    // },
    // function to display points from a set of data
    parseData (dataCollection) {
      for (var item in dataCollection) {
        var tmpPoint = this.createPointPrimitive(dataCollection[item])
        this._myViewer.entities.add(tmpPoint)
      }
    },
    Tick (event) {
      if (event.shouldAnimate && event.canAnimate) {
        // console.log("clock play")
      }

      // console.log( this._myCesium.JulianDate.toDate(event.currentTime) )
    },
    MakeListSameColor (collection, list, color) {
      for (var i = 0; i < collection.length; i++) {
        var p = collection.get(i)
        if (p._color.toRgba() === color) {
          list.push(p)
        }
      }
      console.log('la liste à remove', list)
    },
    DeletePoints (List, collection) {
      for (var i = 0; i < List.length; i++) {
        if (typeof (List[i]) !== 'undefined') {
          collection.remove(List[i])
        }
      }
    },
    ready (cesiumInstance) {
      const { Cesium, viewer, Ellipsoid } = cesiumInstance
      this._myCesium = Cesium
      this._myViewer = viewer
      this._myEllispoid = Ellipsoid
      var startDate = this._myCesium.JulianDate.fromIso8601('2019-05-01T23:00:00.000')
      var endDate = this._myCesium.JulianDate.fromIso8601('2019-06-01T00:00:00.000')
      this._myViewer.timeline.zoomTo(startDate, endDate)
      // to interact with point primitive on click
      var _this = this
      this._myViewer.screenSpaceEventHandler.setInputAction(function onLeftClick (movement) {
        // debugger
        // boucle sur les collection
        // on retrouve le point
        // _this.myRawDataPrimitive._pointPrimitives.find(function(item) {  return item.id == selectPoint.id } )
        // aprés on fait ce qu'on veut = mettre tous les points de cet id d'une couleur
        
        var selectPoint = viewer.scene.pick(movement.position)
        var selectCollection = selectPoint.collection
        // selectPoint.primitive
        var PointColorRgba = selectPoint.primitive._color.toRgba()
        for (var item in _this.myConfigCollection) {
          if (selectCollection === _this.myConfigCollection[item].references) {
            if (PointColorRgba === _this.myConfigCollection[item].defaultColor) {
              selectPoint.primitive.color = Cesium.Color.fromRgba(_this.myConfigCollection[item].clickedColor)
            } else {
              selectPoint.primitive.color = Cesium.Color.fromRgba(_this.myConfigCollection[item].defaultColor)
            }
          }
        }
        console.log(selectPoint.id)
      }, Cesium.ScreenSpaceEventType.LEFT_CLICK)
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
        console.log('data avant remove', _this.myPrefilteredDataPrimitive)
        _this.myPrefilteredDataPrimitive.entities.remove(entity)
        console.log('data apres remove', _this.myPrefilteredDataPrimitive)
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
      var PointToRemoveColor = 4278190335 // Red points are to remove
      var PointToRestoreColor = 4294967295
      var PointsToRemove = []
      var PointToRestore = []
      this.MakeListSameColor(this.myfilteredDataPrimitive, PointsToRemove, PointToRemoveColor)
      this.MakeListSameColor(this.myEliminatedDataPrimitive, PointToRestore, PointToRestoreColor)
      for (var point in PointsToRemove) {
        this.myEliminatedDataPrimitive.add(
          {
            id: PointsToRemove[point]._id,
            show: false,
            allowPicking: true,
            color: this._myCesium.Color.fromRgba(this.myConfigCollection.myEliminatedData.defaultColor),
            outlineColor: this._myCesium.Color.YELLOW,
            outlineWidth: 2,
            position: new this._myCesium.Cartesian3(PointsToRemove[point].position.x, PointsToRemove[point].position.y, PointsToRemove[point].position.z)
          }
        )
      }
      for (var points in PointToRestore) {
        this.myfilteredDataPrimitive.add(
          {
            id: PointToRestore[points]._id,
            show: false,
            allowPicking: true,
            color: this._myCesium.Color.fromRgba(this.myConfigCollection.myfilteredData.defaultColor),
            outlineColor: this._myCesium.Color.YELLOW,
            outlineWidth: 2,
            position: new this._myCesium.Cartesian3(PointToRestore[points].position.x, PointToRestore[points].position.y, PointToRestore[points].position.z)
          }
        )
      }
      this.DeletePoints(PointsToRemove, this.myfilteredDataPrimitive)
      this.DeletePoints(PointToRestore, this.myEliminatedDataPrimitive)
    },
    // remove_point () {
    //   // var SelectedPoint = this._myViewer.selectedEntity
    //   // // console.log('on est dans remove_point', SelectedPoint)
    //   // SelectedPoint.entityCollection.remove(SelectedPoint)
    // },
    // Function to give data from entitescollections same shape as backapp and then send it to export2
    ManageData () {
      // alert(' ok managedata')
      if (typeof (this.myRawDataPrimitive) === 'undefined' || typeof (this.myEliminatedDataPrimitive) === 'undefined' || typeof (this.myfilteredDataPrimitive) === 'undefined') { // METTRE LES CONDITIONS POUR LES AUTRE
        alert('Import data first')
      } else {
        // console.log('je genere les data a transformer depuis managedata', this.myfilteredDataPrimitive.length)
        var dataPoints = []
        for (var i = 0; i < this.myfilteredDataPrimitive.length - 1; i++) {
          var p = this.myfilteredDataPrimitive.get(i)
          debugger
          // for (var i = 0; i < this.myfilteredDataPrimitive.length; i++) {
          // var item = this.myfilteredDataPrimitive.values[i]
          var curPosition = p.position
          var carto = this._myCesium.Ellipsoid.WGS84.cartesianToCartographic(curPosition)
          var lon = this._myCesium.Math.toDegrees(carto.longitude)
          var lat = this._myCesium.Math.toDegrees(carto.latitude)
          var height = this._myCesium.Math.toDegrees(carto.height)
          // var date = this._myCesium.JulianDate.toIso8601(p._date) // VOIR SOUCI DE DATE
          // var date = this._myCesium.JulianDate.toDate(p._date)
          dataPoints.push({
            id: p._id,
            date: p._date,
            LON: lon,
            LAT: lat,
            elevation: height
          })
        }
        // console.log(dataPoints)
        this.$root.$emit('CSVtodownload', dataPoints)
      }
    },
    cleanCollection () { // to clean everything before importing new data
      // console.log('update du front')
      if (this.myRawDataPrimitive || this.myPrefilteredDataPrimitive || this.myEliminatedDataPrimitive || this.myfilteredDataPrimitive) {
        if (confirm('You are going to loose current data, do you still want to proceed ?')) {
          // to destroy the collection and erase points from viewer
          this.myRawDataPrimitive.destroy()
          this.myPrefilteredDataPrimitive.destroy()
          this.myEliminatedDataPrimitive.destroy()
          this.myfilteredDataPrimitive.destroy()
          // to uncheck checkboxes
          document.getElementById('rd').checked = false
          document.getElementById('pfd').checked = false
          document.getElementById('ed').checked = false
          document.getElementById('fd').checked = false
        }
      }
    }
  },
  mounted () {
    var _this = this
    // MODIFIER AVEC THIS.EMIT DANS ImportData ET EVENT LISTENER DANS APP avec fonction https://www.telerik.com/blogs/how-to-emit-data-in-vue-beyond-the-vuejs-documentation
    _this.$root.$on('eventing', data => {
      // Creating Collections of points
      this.displayCheckbox = true
      var dates = []
      _this.myRawDataPrimitive = new _this._myCesium.PointPrimitiveCollection('my raw data') // new _this._myCesium.CustomDataSource('my raw data')
      _this.myRawDataEntity = new _this._myCesium.EntityCollection()
      // _this.RDate = new _this.myCesium.TimeIntervalCollection()
      _this.myImpossibleDataPrimitive = new _this._myCesium.PointPrimitiveCollection()
      _this.myPrefilteredDataPrimitive = new _this._myCesium.PointPrimitiveCollection('my prefiltered data')
      _this.myPrefilteredDataEntity = new _this._myCesium.EntityCollection()
      _this.myEliminatedDataPrimitive = new _this._myCesium.PointPrimitiveCollection('my eliminated data')
      _this.myEliminatedDataEntity = new _this._myCesium.EntityCollection()
      _this.myfilteredDataPrimitive = new _this._myCesium.PointPrimitiveCollection('my filtered data')
      _this.myfilteredDataEntity = new _this._myCesium.EntityCollection()
      _this.Detected_immoPrimitive = new _this._myCesium.PointPrimitiveCollection()
      _this.myConfigCollection = {
        'myRawData': {
          defaultColor: 4294901760,
          clickedColor: 4278190335,
          outlineColor: 4294967295,
          references: _this.myRawDataPrimitive
        },
        'myImpossibleData': {
          defaultColor: 4278190080,
          outlineColor: 4294967295,
          clickedOutlineColor: 4278255615,
          references: _this.myImpossibleDataPrimitive
        },
        'myPrefilteredData': {
          defaultColor: 4286611584,
          clickedColor: 4278190335,
          outlineColor: 4294967295,
          references: _this.myPrefilteredDataPrimitive
        },
        'myEliminatedData': {
          defaultColor: 4278190335,
          clickedColor: 4294967295,
          outlineColor: 4294967295,
          references: _this.myEliminatedDataPrimitive
        },
        'myfilteredData': {
          defaultColor: 4278222848,
          clickedColor: 4278190335,
          outlineColor: 4294967295,
          references: _this.myfilteredDataPrimitive
        }
      }
      // To add data to points collections
      for (var itr in data[0]) {
        _this.myRawDataPrimitive.add(_this.createPointPrimitive(data[0][itr], _this.myConfigCollection.myRawData.defaultColor, _this.myConfigCollection.myRawData.outlineColor))
        _this.myRawDataEntity.add(_this.createPointEntity(data[0][itr], _this.myConfigCollection.myRawData.defaultColor, _this.myConfigCollection.myRawData.outlineColor))
        dates.push(data[0][itr]['date'])
      }
      console.log('les dates', dates)
      console.log('la collection', _this.myRawDataPrimitive)
      // debugger
      // _this.RDates = this._myCesium.TimeIntervalCollection.fromIso8601DateArray({
      //   iso8601Dates: dates
      // })
      console.log('les dates en collection', _this.RDate)
      for (var itp in data[1]) {
        _this.myPrefilteredDataPrimitive.add(_this.createPointPrimitive(data[1][itp], this.myConfigCollection.myPrefilteredData.defaultColor, _this.myConfigCollection.myPrefilteredData.outlineColor))
        _this.myPrefilteredDataEntity.add(_this.createPointEntity(data[1][itp], this.myConfigCollection.myPrefilteredData.defaultColor, _this.myConfigCollection.myPrefilteredData.outlineColor))
      }
      for (var ite in data[2]) {
        _this.myImpossibleDataPrimitive.add(_this.createPointPrimitive(data[2][ite], this.myConfigCollection.myImpossibleData.defaultColor, _this.myConfigCollection.myImpossibleData.outlineColor))
      }
      for (var itf = 0; itf < data[3].length - 1; itf++) {
      //   _this.fpolylines = _this._myViewer.entities.add(new _this._myCesium.Entity()) // to create segments between consecutive points
        _this.myfilteredDataPrimitive.add(_this.createPointPrimitive(data[3][itf], this.myConfigCollection.myfilteredData.defaultColor, _this.myConfigCollection.myfilteredData.outlineColor)) // to create points
        _this.myfilteredDataEntity.add(_this.createPointEntity(data[3][itf], this.myConfigCollection.myfilteredData.defaultColor, _this.myConfigCollection.myfilteredData.outlineColor))
        // To create lines
        _this.Rawlines = new _this._myCesium.PolylineCollection()
        _this.CreatePolylines(_this.myRawDataPrimitive, _this.Rawlines)
      }
      if (data[4].length > 0) {
        console.log('une immobilité a été détectée')
        for (var iti in data[4]) {
          _this.Detected_immoPrimitive.add(_this.createPointPrimitive(data[4][iti], this._myCesium.Color.WHITE, this._myCesium.Color.RED))
        }
      }
    })
    // _this.$root.$on('UpdateData', () =>  {
    //   console.log(" ok on va clean")
    // })
    // _this.$root.$on('downloadcsv', flag => {

    //   console.log('je genere les data a transformer', _this.myPrefilteredDataPrimitive)
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
