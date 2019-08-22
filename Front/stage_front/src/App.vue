<template>
  <div id="app">
    <visualization></visualization>
    <Parameters></Parameters>
    <ImportData @UpdateData='cleanCollection' @loading ='spinnerOn'></ImportData>
    <Export @downloadcsv='ManageData'></Export>
    <div class="viewer col-4" ref="myViewer">
      <!-- <div id="immo" v-if="immobility">
        <b-alert>An immobility has been detected</b-alert>
      </div> -->
      <div id="interact_data" class="demo-tool">
        <div v-if="displayCheckbox">
          <div id='primitive'>
            <h2>Choose the collection to display</h2>
            <b-form-group>
              <b-form-checkbox-group
                id="checkbox-group-1"
                v-model="selected"
                :options="optionscheckbox"
                name="flavour-1"
                @change="onCheckboxCollectionChange($event)"
              ></b-form-checkbox-group>
              <div>Selected in filtered data: <strong>{{ pointsToRemoveFd }}</strong></div>
              <div>Selected in eliminated data: <strong>{{ pointsToRemoveEd }}</strong></div>
            </b-form-group>
            <button v-on:click="remove_point" >Remove point</button>
          </div>
          <div id='player'>
            <b-form-group label="PLAYER MODE">
              <b-form-radio-group
                v-model="picked"
                :options="optionsRadios"
                name="radio-inline"
                @change="collectionToAnimate($event)"
              ></b-form-radio-group>
            </b-form-group>
          </div>
        </div>
        <div v-else-if='loading'>
          <div class="d-flex justify-content-center mb-3">
              <b-spinner label="Loading..."></b-spinner>
          </div>
        </div>
        <div id='globeOptions'>
          <b-form-checkbox id = "3DT" v-model="terrainTransparency" @change="displayTransparency($event)" switch/>
          <label for="3DT">Terrain transparency</label>
        </div>
      </div>
    </div>
    <div id='globeOptions'>
      <b-form-checkbox id = "3DT" v-model="terrainTransparency" @change="displayTransparency($event)" switch/>
      <label for="3DT">Terrain transparency</label>
    </div>

    <cesium-viewer :animation="animation" :navigationHelpButton="navigationHelpButton" :baseLayerPicker="baseLayerPicker" :sceneModePicker="sceneModePicker" :homeButton="homeButton" @Tick="Tick" :camera="camera" :fullscreenButton="fullscreenButton" @ready="ready">
      <cesium-terrain-provider></cesium-terrain-provider>
      </cesium-viewer>
  </div>
</template>

<script>
import visualization from './components/Visualization/visualization.vue'
import ImportData from './components/Import/ImportData.vue'
import Export from './components/Export/Export.vue'
import Parameters from './components/Parameters/Parameters.vue'
import VueCesium from 'vue-cesium'
import Vue from 'vue'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(VueCesium)

export default {
  name: 'App',
  components: {
    visualization,
    ImportData,
    Export,
    Parameters
  },
  data () {
    // Cesium.BingMapsApi.defaultKey = 'AgqG7d1hd0psBdMyO3kPG8COGLUqA7knynwLSBkjiBRAnvRfOaOv1ZEl3GsDutjC'// ma key
    return {
      animation: false,
      fullscreenButton: true,
      timeline: false,
      homeButton: true,
      baseLayerPicker: false,
      sceneModePicker: true,
      navigationHelpButton: true,
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
      displayCheckbox: false,
      loading: false,
      // immobility: false,
      pointsToRemoveFd: [],
      pointsToRemoveEd: [],
      mySelectedPoints: [],
      terrainTransparency: false,
      selected: [],
      picked: '',
      optionsRadios: [
        { text: 'Raw data', value: 'rd' },
        { text: 'Prefiltered data', value: 'pfd' },
        { text: 'Eliminated data', value: 'ed' },
        { text: 'Filtered data', value: 'fd' }
      ],
      optionscheckbox: [
        { text: 'Raw data', value: 'rd' },
        { text: 'Impossible data', value: 'ipd' },
        { text: 'Prefiltered data', value: 'pfd' },
        { text: 'Eliminated data', value: 'ed' },
        { text: 'Filtered data', value: 'fd' },
        { text: 'Immobility data', value: 'id', disabled: true }
      ]
    }
  },
  methods: {
    homeButtonLocation() {
      if ("geolocation" in navigator) {
        // check if geolocation is supported/enabled on current browser
        navigator.geolocation.getCurrentPosition(
        function success(position) {
        // for when getting location is a success
        console.log('latitude', position.coords.latitude, 'longitude', position.coords.longitude)
        })
      }
    },
    spinnerOn () {
      this.loading = true
    },
    // Function that enables to update current time when selected by hand
    onTimelineScrubfunction (e) {
      this._myViewer.clock.currentTime = e.timeJulian
      this.hideEntity(this.currentCollection, this.lastestIndexFind)
      this.displayedIndex = []
      var indexFinded = this.findNearIndexToDisplay(this.currentCollection, this._myViewer.clock.currentTime)
      if (indexFinded > -1) {
        this.drawEntity(this.currentCollection, indexFinded, indexFinded)
      }
      // this.initPlayer()
      // cacher les points affichés
      // this._myViewer.clock.shouldAnimate = false    A VOIR AVEC LE PLAYER CE QUI SERA LE PLUS PRATIQUE
    },
    // Function to create timeline div, timeline and timeline zoom
    customCreateTimeline (startDate, endDate) {
      let timelineContainer = document.createElement('div')
      timelineContainer.className = 'cesium-viewer-timelineContainer'
      var viewerContainer = document.getElementsByClassName('cesium-viewer')[0]
      viewerContainer.appendChild(timelineContainer)
      let timeline = new this._myCesium.Timeline(timelineContainer, this._myViewer.clock)
      timeline.addEventListener('settime', this.onTimelineScrubfunction, false)
      this._myViewer._timeline = timeline
      this._myViewer.timeline.zoomTo(startDate, endDate)
    },
    // Function to destroy timeline and timeline div if exist
    customDestroyTimeline () {
      if (this._myCesium.defined(this._myViewer.timeline)) {
        this.animation = false
        this.timeline = false
        this._myViewer.timeline.destroy()
        this._myViewer._timeline = undefined
        var viewerContainer = document.getElementsByClassName('cesium-viewer')[0]
        let timelineContainer = viewerContainer.getElementsByClassName('cesium-viewer-timelineContainer')[0]
        viewerContainer.removeChild(timelineContainer)
      }
    },
    // Function to zoom on timeline according to collection's min and max dates
    timelineZoom (minAndMaxDate, selection) {
      if (minAndMaxDate.minDate.dayNumber === null || minAndMaxDate.maxDate.dayNumber === null) {
        this.customDestroyTimeline()
      } else {
        this.animation = selection
        this.timeline = selection
        var startDate = new this._myCesium.JulianDate(minAndMaxDate.minDate.dayNumber, minAndMaxDate.minDate.secondsOfDay)
        var endDate = new this._myCesium.JulianDate(minAndMaxDate.maxDate.dayNumber, minAndMaxDate.maxDate.secondsOfDay)
        if ((!this._myCesium.defined(this._myViewer.timeline) || this._myViewer.timeline.isDestroyed()) && this.timeline === true) {
          this.customCreateTimeline(startDate, endDate)
          // this._myViewer._forceResize = true
          // this._myViewer.resize()
        }
      }
    },
    zoomToPrimitive (collection) {
      var maxLat = -200
      var minLat = 200
      var maxLon = -200
      var minLon = 200
      if (collection.length > 0) {
        // loop to find most extreme points most eastern (min longitude), most Northern (max latitude)...
        for (var i = 0; i < collection.length; i++) {
          var pos = this._myCesium.Ellipsoid.WGS84.cartesianToCartographic(collection._pointPrimitives[i]._position)
          var x = this._myCesium.Math.toDegrees(pos.latitude)
          if (x < minLat) {
            minLat = x
          }
          if (x > maxLat) {
            maxLat = x
          }
          var y = this._myCesium.Math.toDegrees(pos.longitude)
          if (y < minLon) {
            minLon = y
          }
          if (y > maxLon) {
            maxLon = y
          }
        }
        this._myViewer.camera.flyTo({
          destination: this._myCesium.Rectangle.fromDegrees(minLon - 0.5, minLat - 0.5, maxLon + 0.5, maxLat + 0.5)
        })
      } else {
        alert('collection is empty')
      }
    },
    // Linked to checkbox Terrain transparency and permit to display and remove transparency of 3D layer
    displayTransparency (event) {
      this._myViewer.scene.globe.depthTestAgainstTerrain = event
      // var camera = this._myViewer.camera
      // camera.constrainedAxis = this._myCesium.Cartesian3.UNIT_Z
    },
    // Function to hide and show points from primitive collections
    // ShowPoints (collection, selection) {
    //   for (var i = 0; i < collection.length; i++) {
    //     var p = collection.get(i)
    //     p.show = selection
    //   }
    // },
    // Function linked to checkboxes to hide and show primitive collections
    cleanPlayer () {
      var allcheckbox = document.querySelectorAll('div#player input')
      for (var i = 0; i < allcheckbox.length; i++) {
        allcheckbox[i].checked = false
      }
      if (this._myViewer.dataSources.length) {
        this._myViewer.dataSources.removeAll()
      }
      this._myViewer.entities.removeAll()
      this.customDestroyTimeline()
    },
    CleanMap (collection) {
      for (var i = this._myViewer.scene.primitives._primitives.length - 1; i >= 0; i--) {
        if (this._myViewer.scene.primitives._primitives[i] === collection) {
          this._myViewer.scene.primitives._primitives.splice(i, 1)
        }
      }
      // for (var i = 0; i < this._myViewer.scene.primitives._primitives.length; i++) {
      //   console.log()
      //   if (this._myViewer.scene.primitives._primitives[i] === collection) {
      //     this._myViewer.scene.primitives._primitives.splice(i, 1)
      //   }
      // }
    },
    addToMap (collection) {
      var present = false
      for (var i = 0; i < this._myViewer.scene.primitives._primitives.length; i++) {
        if (this._myViewer.scene.primitives._primitives[i] === collection) {
          present = true
          break
        }
      }
      if (!present) {
        this._myViewer.scene.primitives.add(collection)
      }
    },
    onCheckboxCollectionChange (event) {
      var arraySelected = event
      var arrayCheckboxes = this.optionscheckbox.map(function (item) { return item.value })
      var arrayUnSelected = arrayCheckboxes.filter(x => !arraySelected.includes(x))
      this.cleanPlayer()
      for (var val of arrayUnSelected) {
        switch (val) {
          case 'rd': {
            this.CleanMap(this.myRawDataPrimitive)
            break
          }
          case 'ipd': {
            this.CleanMap(this.myImpossibleDataPrimitive)
            break
          }
          case 'pfd': {
            this.CleanMap(this.myPrefilteredDataPrimitive)
            break
          }
          case 'ed': {
            this.CleanMap(this.myEliminatedDataPrimitive)
            break
          }
          case 'fd': {
            this.CleanMap(this.myfilteredDataPrimitive)
            break
          }
          case 'id': {
            this.CleanMap(this.myDetected_immoPrimitive)
            break
          }
          default: {
            console.log('should never be here')
            break
          }
        }
      }
      console.log('test', event.length)
      if (event.length === 0) {
        console.log('rien n est coché')
        // var center = this._myCesium.Cartesian3.fromDegrees(5.369222, 43.292770)
        // this._myViewer.camera.lookAt(center)
        // this._myViewer.zoomTo(this._myViewer.entities)
        // this.camera.position.longitude = 5.369222
        // this.camera.position.latitude = 43.292770
        // this.camera.position.height = 20000000
      } else {
        for (var val2 of arraySelected) {
          switch (val2) {
            case 'rd': {
              this.addToMap(this.myRawDataPrimitive)
              this.zoomToPrimitive(this.myRawDataPrimitive)
              break
            }
            case 'ipd': {
              this.addToMap(this.myImpossibleDataPrimitive)
              this.zoomToPrimitive(this.myImpossibleDataPrimitive)
              break
            }
            case 'pfd': {
              this.addToMap(this.myPrefilteredDataPrimitive)
              this.zoomToPrimitive(this.myPrefilteredDataPrimitive)
              break
            }
            case 'ed': {
              this.addToMap(this.myEliminatedDataPrimitive)
              this.zoomToPrimitive(this.myEliminatedDataPrimitive)
              break
            }
            case 'fd': {
              this.addToMap(this.myfilteredDataPrimitive)
              this.zoomToPrimitive(this.myfilteredDataPrimitive)
              break
            }
            case 'id': {
              console.log(this.myDetected_immoPrimitive)
              this.addToMap(this.myDetected_immoPrimitive)
              this.zoomToPrimitive(this.myDetected_immoPrimitive)
              break
            }
            default: {
              console.log('should never be here')
              break
            }
          }
        }
      }
      // switch (this.lastCheckBoxChecked) {
      //   case 'rd': {
      //     console.log('rd selection', selection)
      //     if (selection === false) {
      //       this.CleanMap(this.myRawDataPrimitive)
      //     } else {
      //       this._myViewer.scene.primitives.add(this.myRawDataPrimitive)
      //       this.zoomToPrimitive(this.myRawDataPrimitive)
      //     }
      //     break
      //   }
      //   case 'ipd': {
      //     if (selection === false) {
      //       this.CleanMap(this.myImpossibleDataPrimitive)
      //     } else {
      //       this._myViewer.scene.primitives.add(this.myImpossibleDataPrimitive)
      //       this.zoomToPrimitive(this.myImpossibleDataPrimitive)
      //     }
      //     break
      //   }
      //   case 'pfd': {
      //     if (selection === false) {
      //       this.CleanMap(this.myPrefilteredDataPrimitive)
      //     } else {
      //       this._myViewer.scene.primitives.add(this.myPrefilteredDataPrimitive)
      //       this.zoomToPrimitive(this.myPrefilteredDataPrimitive)
      //     }
      //     break
      //   }
      //   case 'ed': {
      //     if (selection === false) {
      //       this.CleanMap(this.myEliminatedDataPrimitive)
      //     } else {
      //       this._myViewer.scene.primitives.add(this.myEliminatedDataPrimitive)
      //       this.zoomToPrimitive(this.myEliminatedDataPrimitive)
      //     }
      //     break
      //   }
      //   case 'fd': {
      //     if (selection === false) {
      //       this.CleanMap(this.myfilteredDataPrimitive)
      //     } else {
      //       this._myViewer.scene.primitives.add(this.myfilteredDataPrimitive)
      //       this.zoomToPrimitive(this.myfilteredDataPrimitive)
      //     }
      //     break
      //   }
      //   case 'id': {
      //     if (selection === false) {
      //       this.CleanMap(this.myDetected_immoPrimitive)
      //     } else {
      //       this._myViewer.scene.primitives.add(this.myDetected_immoPrimitive)
      //       this.zoomToPrimitive(this.myDetected_immoPrimitive)
      //     }
      //     break
      //   }
      //   case 'cd': {
      //     if (selection === false) {
      //       this.CleanMap(this.myCleanDataPrimitive)
      //     } else {
      //       this._myViewer.scene.primitives.add(this.myCleanDataPrimitive)
      //       this.zoomToPrimitive(this.myCleanDataPrimitive)
      //     }
      //     break
      //   }
      //   default: {
      //     console.log('should never be here')
      //     // this._myViewer.zoomTo(this._myViewer.entities)
      //     // this.camera.position.longitude = 5.369222
      //     // this.camera.position.latitude = 43.292770
      //     // this.camera.position.height = 10000000
      //     break
      //   }
      // }
    },
    getElevation (Lat, Lon, Height) {
      // var carto = this._myCesium.Cartographic.fromDegrees(Lon, Lat)
      // var position = new this._myCesium.Cartographic(carto.longitude, carto.latitude)
      // var height = this._myViewer.scene.sampleHeight(position)
      // console.log(height)
      // debugger
      // var elevation = null
      // var originalHeight = Height
      // Construct the default list of terrain sources.
      // var terrainModels = Cesium.createDefaultTerrainProviderViewModels();
      // // Construct the viewer, with a high-res terrain source pre-selected.
      // var viewer = new Cesium.Viewer('cesiumContainer', {
      //   terrainProviderViewModels: terrainModels,
      //   selectedTerrainProviderViewModel: terrainModels[1]  // Select STK High-res terrain
      // });
      // // Get a reference to the ellipsoid, with terrain on it.  (This API may change soon)
      // var ellipsoid = viewer.scene.globe.ellipsoid;
      // // Specify our point of interest.
      // var pointOfInterest = Cesium.Cartographic.fromDegrees(-99.64592791446208, 61.08658108795938, 5000, new Cesium.Cartographic())
      // // Sample the terrain (async) and write the answer to the console.
      // Cesium.sampleTerrain(viewer.terrainProvider, 9, [ pointOfInterest ])
      // .then(function(samples) {
      //   //console.log('Height in meters is: ' + samples[0].height);
      // })
      // var terrainProvider = this._myViewer.terrainProvider
      // var position = [
      //   this._myCesium.Cartographic.fromDegrees(Lon, Lat)
      // ]
      // // var promise = this._myCesium.sampleTerrainMostDetailed(terrainProvider, position)
      // var promise = this._myCesium.sampleTerrain(terrainProvider, 2, position)
      // this._myCesium.when(promise, function (updatedPositions) {
      //   elevation = position[0].height
      //   return 3000
      //   // console.log('elevation', position[0].height)
      // })
      // console.log('elevation', elevation)
    },
    // functions to create the points primitives from imported data
    createPointPrimitive (options, color, outlineColor) {
      // console.log('id', options.id)
      // var newHeight = this.getElevation(options.LAT, options.LON,3000)
      // console.log("point",options)
      // console.log("height",newHeight)
      var newPoint = new this._myCesium.PointPrimitive(
        {
          id: options.id,
          show: true,
          allowPicking: true,
          color: this._myCesium.Color.fromRgba(color),
          // color: color,
          outlineColor: this._myCesium.Color.fromRgba(outlineColor),
          outlineWidth: 2,
          position: this._myCesium.Cartesian3.fromDegrees(options.LON, options.LAT, options.elevation, this._myCesium.Ellipsoid.WGS84),
          heightReference: this._myCesium.HeightReference.CLAMP_TO_GROUND
          // position: this._myCesium.Cartesian3.fromDegrees(options.LON, options.LAT, this.getElevation(options.LAT, options.LON, options.elevation), this._myCesium.Ellipsoid.WGS84)
        }
      )
      // debugger
      // var height = this._myViewer.scene.sampleHeight(newPoint.position);
      // console.log("height calculated",height);
      // console.log(" new position", this._myViewer.scene.clampToHeight(newPoint.position))
      // console.log("converted ", this._myCesium.Ellipsoid.WGS84.cartesianToCartographic(newPoint.position))
      // newPoint.position = this._myViewer.scene.clampToHeight(newPoint.position)
      return newPoint
    },
    // functions to create the points entities from imported data
    createPointEntity (options, color, outlineColor) {
      return new this._myCesium.Entity(
        {
          id: options.id,
          name: options.id,
          show: false,
          description: 'date et heure:' + options.date + '<BR>' + 'distance 1:' + options.distance1 + '<BR>' + 'distance 2:' + options.distance2,
          position: this._myCesium.Cartesian3.fromDegrees(options.LON, options.LAT, options.elevation, this._myCesium.Ellipsoid.WGS84),
          date: this._myCesium.JulianDate.fromIso8601(options.date),
          point: {
            pixelSize: 5,
            color: this._myCesium.Color.fromRgba(color),
            outlineColor: this._myCesium.Color.fromRgba(outlineColor),
            outlineWidth: 2,
            heightReference : this._myCesium.HeightReference.CLAMP_TO_GROUND
          },
          label: {
            text: options.id,
            font: '14pt monospace',
            style: this._myCesium.LabelStyle.FILL_AND_OUTLINE,
            outlineWidth: 2,
            verticalOrigin: this._myCesium.VerticalOrigin.BOTTOM,
            pixelOffset: new this._myCesium.Cartesian2(0, -9),
            heightReference : this._myCesium.HeightReference.CLAMP_TO_GROUND
          }
        }
      )
    },
    // functions to create polylines
    CreatePolylines (collection, object) {
      for (var i = 0; i < collection.length - 1; i++) {
        var p = collection.get(i)
        var q = collection.get(i + 1)
        var lonp = this._myCesium.Math.toDegrees(p.position.x)
        var latp = this._myCesium.Math.toDegrees(p.position.y)
        var lonq = this._myCesium.Math.toDegrees(q.position.x)
        var latq = this._myCesium.Math.toDegrees(q.position.y)
        object.add({
          parent: object,
          position: this._myCesium.Cartesian3.fromDegrees(lonq, latp),
          polyline: {
            positions: [
              this._myCesium.Cartesian3.fromDegrees(lonp, latp),
              this._myCesium.Cartesian3.fromDegrees(lonq, latq)
            ],
            width: new this._myCesium.ConstantProperty(2),
            material: this._myCesium.Color.RED,
            followSurface: new this._myCesium.ConstantProperty(true)
          }
        })
      }
    },
    // Function to get time period of a collection
    getMinMaxDate (collectionEntity) {
      var ncollectionEntity = collectionEntity.entities
      var minDate = {
        dayNumber: null,
        secondsOfDay: null
      }
      var maxDate = {
        dayNumber: null,
        secondsOfDay: null
      }
      if (ncollectionEntity.values.length > 0) {
        var firstItem = ncollectionEntity.values[0]
        minDate.dayNumber = firstItem._date.dayNumber
        minDate.secondsOfDay = firstItem._date.secondsOfDay
        maxDate.dayNumber = firstItem._date.dayNumber
        maxDate.secondsOfDay = firstItem._date.secondsOfDay
        for (var item in ncollectionEntity.values) {
          var curDay = ncollectionEntity.values[item]._date.dayNumber
          var curSeconds = ncollectionEntity.values[item]._date.secondsOfDay
          // get min date
          if (curDay <= minDate.dayNumber) {
            minDate.dayNumber = curDay
            if (curSeconds <= minDate.secondsOfDay) {
              minDate.secondsOfDay = curSeconds
            }
          }
          // get max date
          if (curDay > maxDate.dayNumber) { // if max day changes, we have to rebegin seconds comparison to take the matching max seconds
            maxDate.dayNumber = curDay
            maxDate.secondsOfDay = curSeconds
          }
          if (curDay >= maxDate.dayNumber) {
            maxDate.dayNumber = curDay
            if (curSeconds >= maxDate.secondsOfDay) { // to search max combinaison of day and seconds
              maxDate.secondsOfDay = curSeconds
            }
          }
        }
      }
      // Add some seconds so the last point can be displayed
      minDate.secondsOfDay -= 3600
      maxDate.secondsOfDay += 3600
      return {
        minDate,
        maxDate
      }
    },
    // Function to set the clock
    setClockTime (minAndMaxDate) {
      this._myViewer.clock.startTime = minAndMaxDate.minDate
      this._myViewer.clock.stopTime = minAndMaxDate.maxDate
      this._myViewer.clock.currentTime = minAndMaxDate.minDate
      this._myViewer.clock.clockRange = this._myCesium.ClockRange.CLAMPED
    },
    // Function to animate entity collection
    collectionToAnimate (event) {
      var selection = true
      var value = event
      // Hide primitive collections
      this.CleanMap(this.myRawDataPrimitive)
      this.CleanMap(this.myImpossibleDataPrimitive)
      this.CleanMap(this.myPrefilteredDataPrimitive)
      this.CleanMap(this.myEliminatedDataPrimitive)
      this.CleanMap(this.myfilteredDataPrimitive)
      this.CleanMap(this.myDetected_immoPrimitive)
      // this.CleanMap(this.myCleanDataPrimitive)
      // Uncheck all the checkboxes
      var allcheckbox = document.querySelectorAll('div#primitive input')
      for (var i = 0; i < allcheckbox.length; i++) {
        allcheckbox[i].checked = false
      }
      this.collectiontoplay = value
      this.initPlayer()
      this.currentCollection = null
      // config of timeline
      var minAndMaxDate = {}
      if (this._myViewer.dataSources.length) {
        this._myViewer.dataSources.removeAll()
      }
      switch (this.collectiontoplay) {
        case 'rd': {
          minAndMaxDate = this.getMinMaxDate(this.myRawDataEntity)
          this.timelineZoom(minAndMaxDate, selection)
          this.setClockTime(minAndMaxDate)
          this.currentCollection = this.myRawDataEntity
          this._myViewer.dataSources.add(this.myRawDataEntity)
          break
        }
        case 'pfd': {
          minAndMaxDate = this.getMinMaxDate(this.myPrefilteredDataEntity)
          this.timelineZoom(minAndMaxDate, selection)
          this.setClockTime(minAndMaxDate)
          this.currentCollection = this.myPrefilteredDataEntity
          this._myViewer.dataSources.add(this.myPrefilteredDataEntity)
          break
        }
        case 'fd': {
          minAndMaxDate = this.getMinMaxDate(this.myfilteredDataEntity)
          this.timelineZoom(minAndMaxDate, selection)
          this.setClockTime(minAndMaxDate)
          this.currentCollection = this.myfilteredDataEntity
          this._myViewer.dataSources.add(this.myfilteredDataEntity)
          break
        }
        case 'cd': {
          minAndMaxDate = this.getMinMaxDate(this.myCleanDataEntity)
          this.timelineZoom(minAndMaxDate, selection)
          this.setClockTime(minAndMaxDate)
          this.currentCollection = this.myCleanDataEntity
          this._myViewer.dataSources.add(this.myCleanDataEntity)
          break
        }
        default: {
          console.log('should never be here')
          break
        }
      }
    },
    initPlayer () {
      this.lastestIndexFind = -1
      this.normal = 0
      this.reverse = 0
      this.displayedIndex = []
      this.maxHistory = 10
      this.maxPolylines = 2
      this.polylineCollection = new this._myCesium.PolylineCollection()
      if (this.currentCollection) {
        this.hideEntity(this.currentCollection, this.currentCollection.entities.values.length - 1)
      }
    },
    // Function to find point to display when time is set with mouse and event settime
    findNearIndexToDisplay (collection, date) {
      var startingIndex = 0
      var arrCollection = collection.entities.values
      var startingIndexSeconds = -1
      var matchedIndex = -1
      for (var i = startingIndex; i < arrCollection.length; i++) {
        var entityDateDay = arrCollection[i].date
        if (entityDateDay.dayNumber <= date.dayNumber) {
          if (entityDateDay.dayNumber < date.dayNumber) {
            startingIndexSeconds = i
          }
          if (entityDateDay.dayNumber === date.dayNumber) {
            if (entityDateDay.secondsOfDay <= date.secondsOfDay) {
              startingIndexSeconds = i
            } else {
              break
            }
          }
        } else {
          break
        }
      }
      if (startingIndexSeconds > -1) {
        if (arrCollection[startingIndexSeconds].date.dayNumber < date.dayNumber) { // special case
          matchedIndex = startingIndexSeconds
        } else {
          for (var j = startingIndexSeconds; j < arrCollection.length; j++) {
            var entityDateSec = arrCollection[j].date
            if (entityDateSec.secondsOfDay <= date.secondsOfDay && entityDateSec.dayNumber <= date.dayNumber) {
              matchedIndex = j
            } else {
              break
            }
          }
        }
      } else {
        console.log('something goes wrong we should not be there')
      }
      if (matchedIndex === -1) {
        return startingIndexSeconds
      } else {
        return matchedIndex
      }
    },
    // Function to find point to display when animation is set to reverse
    findIndexToDisplayReverse (collection, date) {
      if (this.lastestIndexFind > -1) {
        var startingIndex = this.lastestIndexFind
      }
      var arrCollection = collection.entities.values
      var startingIndexSeconds = -1
      var matchedIndex = -1
      for (var i = startingIndex; i >= 0; i--) {
        var entityDateDay = arrCollection[i].date
        if (entityDateDay.dayNumber === date.dayNumber) {
          startingIndexSeconds = i
          break
        }
      }
      if (startingIndexSeconds > -1) {
        for (var j = startingIndexSeconds; j >= 0; j--) {
          var entityDateSec = arrCollection[j].date
          if (entityDateSec.secondsOfDay >= date.secondsOfDay && entityDateSec.dayNumber >= date.dayNumber) {
            matchedIndex = j
          } else {
            break
          }
        }
      } else {
        console.log('something goes wrong we should not be there')
      }
      if (matchedIndex === this.lastestIndexFind) {
        return -1
      }
      return matchedIndex
    },
    // Function to find point to display when starts from beginning
    findIndexToDisplay (collection, date) {
      var startingIndex = 0
      if (this.lastestIndexFind > -1) {
        startingIndex = this.lastestIndexFind
      }
      var arrCollection = collection.entities.values
      var startingIndexSeconds = -1
      var matchedIndex = -1
      for (var i = startingIndex; i < arrCollection.length; i++) {
        var entityDateDay = arrCollection[i].date
        if (entityDateDay.dayNumber === date.dayNumber) {
          startingIndexSeconds = i
          break
        }
      }
      if (startingIndexSeconds > -1) {
        for (var j = startingIndexSeconds; j < arrCollection.length; j++) {
          var entityDateSec = arrCollection[j].date
          if (entityDateSec.secondsOfDay <= date.secondsOfDay && entityDateSec.dayNumber <= date.dayNumber) {
            matchedIndex = j
          } else {
            break
          }
        }
      } else {
        console.log('something goes wrong we should not be there')
      }
      if (matchedIndex === this.lastestIndexFind) {
        return -1
      }
      return matchedIndex
    },
    // Function that makes a list of last points displayed to have a moving window and to draw lines
    storeHistory (index) {
      if (this.displayedIndex.length >= this.maxHistory) { // tableau plein
        this.displayedIndex.pop() // enlève l'élément d'index le plus haut
        // hide entity
      }
      if (this.displayedIndex.length > 0) {
        if (this.displayedIndex[0] !== index) { // to only have different indexes
          this.displayedIndex.unshift(index) // to add a new element with index 0
        }
      } else {
        this.displayedIndex.unshift(index)
      }
    },
    // Function to draw lines between last points
    drawPolylines (nbToDraw) {
      // var nbPolyLinesDraw = 0
      var nbToDel = this._myViewer.entities.values.length - this.maxPolylines
      if (nbToDel > 0) {
        for (var j = 0; j < nbToDel; j++) {
          var curEntity = this._myViewer.entities.values[j]
          this._myViewer.entities.remove(curEntity)
        }
      }
      for (var i = 0; i <= nbToDraw; i++) {
        if (i + 1 < this.displayedIndex.length) {
          var lastEntityindex = this.displayedIndex[i]
          var beforeLastEntityIndex = this.displayedIndex[i + 1]
          // get points positions
          var firstPoint = this.currentCollection.entities.values[beforeLastEntityIndex]
          var lastPoint = this.currentCollection.entities.values[lastEntityindex]
          var f = this._myCesium.Ellipsoid.WGS84.cartesianToCartographic(firstPoint.position._value)
          var l = this._myCesium.Ellipsoid.WGS84.cartesianToCartographic(lastPoint.position._value)
          var lonf = this._myCesium.Math.toDegrees(f.longitude)
          var latf = this._myCesium.Math.toDegrees(f.latitude)
          var lonl = this._myCesium.Math.toDegrees(l.longitude)
          var latl = this._myCesium.Math.toDegrees(l.latitude)
          // draw line
          this._myViewer.entities.add({
            polyline: {
              positions: this._myCesium.Ellipsoid.WGS84.cartographicArrayToCartesianArray(
                [
                  this._myCesium.Cartographic.fromDegrees(lonf, latf, f.height),
                  this._myCesium.Cartographic.fromDegrees(lonl, latl, l.height)
                ]
              ),
              width: 2,
              material: this._myCesium.Color.RED,
              clampToGround: true
              // followSurface: new this._myCesium.ConstantProperty(true)
            }
          })
        }
      }
    },
    drawEntity (collection, startingIndex, endingIndex) {
      for (var i = startingIndex; i <= endingIndex; i++) {
        this.storeHistory(i)
        collection.entities.values[i].show = true
        var pt = this._myViewer.entities.getById(collection.entities.values[i]._id)
        this._myViewer.trackedEntity = pt
        // this._myViewer.camera.flyTo({
        //   destination : new this._myCesium.Cartesian3(collection.entities.values[i]._position._value.x, collection.entities.values[i]._position._value.y, collection.entities.values[i]._position._value.z)
        // })
        if (this.displayedIndex.length > 1) {
          var nbLinesToDraw = -1 // equals nb lines to draw - 1 because Starting index = lastIndexFind+1
          nbLinesToDraw = endingIndex - startingIndex
          this.drawPolylines(nbLinesToDraw)
        }
      }
      this.lastestIndexFind = endingIndex
    },
    drawEntityReverse (collection, minIndex, maxIndex) {
      for (var i = maxIndex; i >= minIndex; i--) {
        this.storeHistory(i)
        collection.entities.values[i].show = true
        if (this.displayedIndex.length > 1) {
          var nbLinesToDraw = -1 // equals nb lines to draw - 1 because Starting index = lastIndexFind+1
          nbLinesToDraw = maxIndex - minIndex
          this.drawPolylines(nbLinesToDraw)
        }
      }
      this.lastestIndexFind = minIndex
    },
    hideEntity (collection, index) {
      var arrCollection = collection.entities.values
      for (var i = 0; i <= index; i++) {
        arrCollection[i].show = false
      }
    },
    hideEntityReverse (collection, index) {
      var arrCollection = collection.entities.values
      for (var i = arrCollection.length; i >= index; i--) {
        if (arrCollection[i] !== undefined) {
          arrCollection[i].show = false
        }
      }
    },
    player (collection, date) {
      if (this._myViewer.clock._multiplier > 0) {
        var indexFinded = this.findIndexToDisplay(collection, date)
        if (indexFinded > -1) {
          if (this.lastestIndexFind === -1) {
            this.drawEntity(collection, 0, indexFinded)
          } else {
            this.hideEntity(collection, this.lastestIndexFind)
            this.drawEntity(collection, this.lastestIndexFind + 1, indexFinded)
          }
        }
      } else {
        var indexFindedR = null
        if (this.reverse > 1) {
          indexFindedR = this.findIndexToDisplayReverse(collection, date)
        } else {
          indexFindedR = this.findNearIndexToDisplay(collection, date)
        }
        if (indexFindedR > -1) {
          if (this.lastestIndexFind === -1) {
            console.log('on peut pas reverse depuis le début')
          } else {
            this.hideEntityReverse(collection, this.lastestIndexFind)
            this.drawEntityReverse(collection, indexFindedR, this.lastestIndexFind - 1)
          }
        }
      }
    },
    displayEntity (collection, matchedIndex, latestIndex) {
      for (var j = 0; j < matchedIndex; j++) {
        collection.entities.values[j].show = false
      }

      if (typeof (latestIndex) === 'undefined') {
        collection.entities.values[matchedIndex].show = true
        return
      }
      for (var i = latestIndex; i < matchedIndex; i++) {
        collection.entities.values[i].show = true
      }
    },
    // function thats exec at each tick of the clock when it plays
    Tick (event) {
      if (event.shouldAnimate && event.canAnimate) {
        var date = event._currentTime
        if (this._myViewer.clock._multiplier > 0) {
          if (this.normal === 0) {
            this.displayedIndex = []
          }
          this.normal = this.normal + 1
          this.reverse = 0
        } else {
          if (this.reverse === 0) {
            this.displayedIndex = []
          }
          this.reverse = this.reverse + 1
          this.normal = 0
        }
        switch (this.collectiontoplay) {
          case 'rd': {
            this.player(this.myRawDataEntity, date)
            break
          }
          case 'pfd': {
            this.player(this.myPrefilteredDataEntity, date)
            break
          }
          case 'fd': {
            this.player(this.myfilteredDataEntity, date)
            break
          }
          case 'cd': {
            this.player(this.myCleanDataEntity, date)
            break
          }
          default: {
            console.log('should never be here')
            break
          }
        }
      } else {
        // console.log("plus de player")
      }
    },
    // Function to unselect point
    findAndRemovePointSelected (selectedPoint) {
      for (var i = 0; i < this.mySelectedPoints.length; i++) {
        if (selectedPoint === this.mySelectedPoints[i]) {
          this.mySelectedPoints.splice(i, 1)
        }
      }
    },
    ready (cesiumInstance) {
      const { Cesium, viewer } = cesiumInstance
      this._myCesium = Cesium
      this._myViewer = viewer
      // to interact with point primitive on click
      var _this = this
      this._myViewer.screenSpaceEventHandler.setInputAction(function onLeftClick (movement) {
        // debugger
        // _this.myRawDataPrimitive._pointPrimitives.find(function(item) {  return item.id == selectPoint.id } )
        var selectPoint = viewer.scene.pick(movement.position)
        if (selectPoint !== undefined) {
          var selectCollection = selectPoint.collection // To know in which collection we are
          var PointColorRgba = selectPoint.primitive._color.toRgba() // to know the point's color
          for (var item in _this.myConfigCollection) {
            if (selectCollection === _this.myConfigCollection[item].references) { // to find matching collection
              if (PointColorRgba === _this.myConfigCollection[item].defaultColor) { // to know in what color is the point and give him the other one
                // to write selected points id in span
                if (_this.myConfigCollection[item].defaultColor === 4278222848) {
                  _this.pointsToRemoveFd.push(Number(selectPoint.id))
                } else {
                  _this.pointsToRemoveEd.push(Number(selectPoint.id))
                }
                selectPoint.primitive.color = Cesium.Color.fromRgba(_this.myConfigCollection[item].clickedColor)
                _this.mySelectedPoints.push(selectPoint)
              } else {
                // To remove id from liste span selected
                if (_this.myConfigCollection[item].defaultColor === 4278222848) {
                  for (var i=0; i < _this.pointsToRemoveFd.length; i++) {
                    if (Number(selectPoint.id) === _this.pointsToRemoveFd[i] ) {
                      _this.pointsToRemoveFd.splice(i,1)
                    }
                  }
                } else {
                  for (var i=0; i <= _this.pointsToRemoveEd.length; i++) {
                    if (Number(selectPoint.id) === _this.pointsToRemoveEd[i] ) {
                      _this.pointsToRemoveFd.splice(i,1)
                    }
                  }
                }
                // to undo changes so the point won't be removed
                selectPoint.primitive.color = Cesium.Color.fromRgba(_this.myConfigCollection[item].defaultColor)
                _this.findAndRemovePointSelected(selectPoint) // when point is clicked on a second time , give back default color and delete from selected point list
              }
            }
          }
          console.log(selectPoint.id)
        }
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
    // Function to delete a point from a collection and add it to another
    remove_point () {
      for (var point in this.mySelectedPoints) {
        var pointEntity = this.myfilteredDataEntity.entities.getById(this.mySelectedPoints[point].primitive._id)
        if (pointEntity === undefined) {
          pointEntity = this.myEliminatedDataEntity.entities.getById(this.mySelectedPoints[point].primitive._id)
          this.myfilteredDataEntity.entities.add(
            {
              id: pointEntity.id,
              name: pointEntity.id,
              description: 'date et heure:' + pointEntity.date + '<BR>' + 'distance 1:' + pointEntity.distance1 + '<BR>' + 'distance 2:' + pointEntity.distance2,
              position: new this._myCesium.Cartesian3(pointEntity._position._value.x, pointEntity._position._value.y, pointEntity._position._value.z),
              date: pointEntity.date,
              point: {
                pixelSize: 5,
                color: this._myCesium.Color.fromRgba(this.myConfigCollection.myfilteredData.defaultColor),
                outlineColor: this._myCesium.Color.YELLOW,
                outlineWidth: 2
              },
              label: {
                text: pointEntity.id,
                font: '14pt monospace',
                style: this._myCesium.LabelStyle.FILL_AND_OUTLINE,
                outlineWidth: 2,
                verticalOrigin: this._myCesium.VerticalOrigin.BOTTOM,
                pixelOffset: new this._myCesium.Cartesian2(0, -9)
              }
            }
          )
          this.myfilteredDataPrimitive.add(
            {
              id: this.mySelectedPoints[point].primitive._id,
              show: true,
              allowPicking: true,
              color: this._myCesium.Color.fromRgba(this.myConfigCollection.myfilteredData.defaultColor),
              outlineColor: this._myCesium.Color.YELLOW,
              outlineWidth: 2,
              position: new this._myCesium.Cartesian3(this.mySelectedPoints[point].primitive._position.x, this.mySelectedPoints[point].primitive._position.y, this.mySelectedPoints[point].primitive._position.z)
            }
          )
          this.myEliminatedDataPrimitive.remove(this.mySelectedPoints[point].primitive)
          this.myEliminatedDataEntity.entities.remove(pointEntity)
          for(var i=0; i<this.dataReceived[0].length; i++) {
            if (this.dataReceived[0][i].id === this.mySelectedPoints[point].primitive._id) {
              this.dataReceived[0][i].status='validated by hand'
            }
          }
          //this.dataReceived[0][id].status='validated by hand' // pas bon, deuxième indice renvoie à index et non à id.. du coup décalage
        } else {
          this.myEliminatedDataEntity.entities.add(
            {
              id: pointEntity.id,
              name: pointEntity.id,
              description: 'date et heure:' + pointEntity.date + '<BR>' + 'distance 1:' + pointEntity.distance1 + '<BR>' + 'distance 2:' + pointEntity.distance2,
              position: new this._myCesium.Cartesian3(pointEntity._position._value.x, pointEntity._position._value.y, pointEntity._position._value.z),
              date: pointEntity.date,
              point: {
                pixelSize: 5,
                color: this._myCesium.Color.fromRgba(this.myConfigCollection.myEliminatedData.defaultColor),
                outlineColor: this._myCesium.Color.YELLOW,
                outlineWidth: 2
              },
              label: {
                text: pointEntity.id,
                font: '14pt monospace',
                style: this._myCesium.LabelStyle.FILL_AND_OUTLINE,
                outlineWidth: 2,
                verticalOrigin: this._myCesium.VerticalOrigin.BOTTOM,
                pixelOffset: new this._myCesium.Cartesian2(0, -9)
              }
            }
          )
          this.myEliminatedDataPrimitive.add(
            {
              id: this.mySelectedPoints[point].primitive._id,
              show: true,
              allowPicking: true,
              color: this._myCesium.Color.fromRgba(this.myConfigCollection.myEliminatedData.defaultColor),
              outlineColor: this._myCesium.Color.YELLOW,
              outlineWidth: 2,
              position: new this._myCesium.Cartesian3(this.mySelectedPoints[point].primitive._position.x, this.mySelectedPoints[point].primitive._position.y, this.mySelectedPoints[point].primitive._position.z)
            }
          )
          this.myfilteredDataPrimitive.remove(this.mySelectedPoints[point].primitive)
          this.myfilteredDataEntity.entities.remove(pointEntity)
          for(var i=0; i<this.dataReceived[0].length; i++) {
            if (this.dataReceived[0][i].id === this.mySelectedPoints[point].primitive._id) {
              this.dataReceived[0][i].status='removed by hand'
            }
          }
          // this.dataReceived[0][id].status='removed by hand' // pas bon, deuxième indice renvoie à index et non à id.. du coup décalage
        }
      }
      // _this.myRawDataPrimitive._pointPrimitives.find(function(item) {  return item.id == selectPoint.id } )
      this.mySelectedPoints = []
      this.pointsToRemoveFd = []
      this.pointsToRemoveEd = []
    },
    // remove_point () {
    //   // var SelectedPoint = this._myViewer.selectedEntity
    //   // // console.log('on est dans remove_point', SelectedPoint)
    //   // SelectedPoint.entityCollection.remove(SelectedPoint)
    // },
    // Function to give data from entitescollections same shape as backapp and then send it to export2 to make csv
    ManageData () {
      var dataPoints = []
      for (var i = 0; i < this.myfilteredDataEntity.entities.values.length; i++) {
        // var p = this.myfilteredDataPrimitive.get(i)
        var item = this.myfilteredDataEntity.entities.values[i]
        var curPosition = item._position._value
        var carto = this._myCesium.Ellipsoid.WGS84.cartesianToCartographic(curPosition)
        var lon = this._myCesium.Math.toDegrees(carto.longitude)
        var lat = this._myCesium.Math.toDegrees(carto.latitude)
        var height = carto.height
        // var date = this._myCesium.JulianDate.toIso8601(p._date) // VOIR SOUCI DE DATE
        var date = this._myCesium.JulianDate.toDate(item.date)
        dataPoints.push({
          id: item.id,
          date: date,
          LON: lon,
          LAT: lat,
          elevation: height
        })
      }
      this.$root.$emit('CSVtodownload', dataPoints)
    },
    // to clean everything before importing new data
    cleanCollection () {
      if (this.myRawDataPrimitive || this.myPrefilteredDataPrimitive || this.myEliminatedDataPrimitive || this.myfilteredDataPrimitive) {
        if (confirm('You are going to loose current data, do you still want to proceed ?')) {
          // to destroy the collection and erase points from viewer
          this.myRawDataPrimitive.destroy()
          this.myImpossibleDataPrimitive.destroy()
          this.myPrefilteredDataPrimitive.destroy()
          this.myEliminatedDataPrimitive.destroy()
          this.myfilteredDataPrimitive.destroy()
          this.myDetected_immoPrimitive.destroy()
          this.myRawDataEntity.entities.removeAll()
          this.myPrefilteredDataEntity.entities.removeAll()
          this.myEliminatedDataEntity.entities.removeAll()
          this.myfilteredDataEntity.entities.removeAll()
          this._myViewer.entities.removeAll()
          // to uncheck checkboxes and empty checkboxes and radio selected
          this.selected = []
          this.picked = ''
          this.customDestroyTimeline()
          this.displayCheckbox = false
        }
      }
    },
    updateElevationPrimitive (collection) {
      // Construct the default list of terrain sources.
      // var terrainModels = this._myCesium.createDefaultTerrainProviderViewModels()

      // Construct the viewer, with a high-res terrain source pre-selected.
      // var viewer = new this._myCesium.Viewer('cesiumContainer', {
      //   terrainProviderViewModels: terrainModels,
      //   selectedTerrainProviderViewModel: terrainModels[1] // Select STK High-res terrain
      // })

      // Get a reference to the ellipsoid, with terrain on it.  (This API may change soon)
      // var ellipsoid = viewer.scene.globe.ellipsoid
      // var terrainProvider = this._myCesium.createWorldTerrain()
      // // Specify our point of interest.
      // for (var i = 0; i < 1; i++) {
      //   // var pointOfInterest = this._myCesium.Cartographic.fromDegrees( 6.779090, 45.227860, 1240)
      //   var pointOfInterest= [
      //     this._myCesium.Ellipsoid.WGS84.cartesianToCartographic(collection._pointPrimitives[i]._position.x, collection._pointPrimitives[i]._position.y)
      //   ]
      //   console.log('point avant', pointOfInterest)
      //   var promise = this._myCesium.sampleTerrainMostDetailed(terrainProvider, pointOfInterest)
      //   this._myCesium.when(promise, function(updatedPositions) {
      //     //ok
      //   })
      //   console.log('point updated', pointOfInterest)
      // [OPTIONAL] Fly the camera there, to see if we got the right point.
      // viewer.camera.flyTo({
      //   destination: ellipsoid.cartographicToCartesian(pointOfInterest)
      // })
      // Sample the terrain (async) and write the answer to the console.
      // this._myCesium.sampleTerrain(viewer.terrainProvider, 9, [ pointOfInterest ])
      // this.height = null
      // .then(function(samples) {
      //   // this.height=samples[0].height
      //   console.log('Height in meters is: ' + samples[0].height)
      //   // console.log('Height in is: ' + this.height)
      //   // console.log('Height point 1 avant: ' + collection._pointPrimitives[i]._position.z)
      //   // var newHeight = this._myCesium.Cartographic.toCartesian(samples[0].height, ellipsoid)
      //   // console.log('newpos', newHeight)
      //   // collection._pointPrimitives[i]._position.z = newHeight
      //   // console.log('Height point 1 apres: ' + collection._pointPrimitives[i]._position.z)
      // })
      // console.log('Height out is: ' + this.height)
      // }
      // collection._pointPrimitives[i]._position.z = samples[0].height
      // debugger
      // var terrainProvider = this._myViewer.terrainProvider
      // for (var i = 0; i < collection.length; i++) {
      //   var position = this._myCesium.Ellipsoid.WGS84.cartesianToCartographic(collection._pointPrimitives[i]._position)
      //   console.log('position carto', position)
      //   var height = this._myViewer.scene.sampleHeight(terrainProvider, position)
      //   console.log('height', height)
      // var position = [
      //
      // ]
      // // var promise = this._myCesium.sampleTerrainMostDetailed(terrainProvider, position)
      // var promise = this._myCesium.sampleTerrain(terrainProvider, 2, position)
      // this._myCesium.when(promise, function (updatedPositions) {
      //   console.log('elevation', position[0].height)
      //   // collection._pointPrimitives[i]._position.z = position[0].height
      // })
    },
    instanciateCollection(data) {
          // To add data to points collections
      for (var itr in data[0]) {
        this.myRawDataPrimitive.add(this.createPointPrimitive(data[0][itr], this.myConfigCollection.myRawData.defaultColor, this.myConfigCollection.myRawData.outlineColor))
        this.myRawDataEntity.entities.add(this.createPointEntity(data[0][itr], this.myConfigCollection.myRawData.defaultColor, this.myConfigCollection.myRawData.outlineColor))
      }
      for (var itp in data[1]) {
        this.myPrefilteredDataPrimitive.add(this.createPointPrimitive(data[1][itp], this.myConfigCollection.myPrefilteredData.defaultColor, this.myConfigCollection.myPrefilteredData.outlineColor))
        this.myPrefilteredDataEntity.entities.add(this.createPointEntity(data[1][itp], this.myConfigCollection.myPrefilteredData.defaultColor, this.myConfigCollection.myPrefilteredData.outlineColor))
      }
      for (var ite in data[2]) {
        this.myImpossibleDataPrimitive.add(this.createPointPrimitive(data[2][ite], this.myConfigCollection.myImpossibleData.defaultColor, this.myConfigCollection.myImpossibleData.outlineColor))
      }
      for (var itf in data[3]) {
        this.myEliminatedDataPrimitive.add(this.createPointPrimitive(data[3][itf], this.myConfigCollection.myEliminatedData.defaultColor, this.myConfigCollection.myEliminatedData.outlineColor)) // to create points
        this.myEliminatedDataEntity.entities.add(this.createPointEntity(data[3][itf], this.myConfigCollection.myEliminatedData.defaultColor, this.myConfigCollection.myEliminatedData.outlineColor))
      }
      for (var itf in data[4]) {
        this.myfilteredDataPrimitive.add(this.createPointPrimitive(data[4][itf], this.myConfigCollection.myfilteredData.defaultColor, this.myConfigCollection.myfilteredData.outlineColor)) // to create points
        this.myfilteredDataEntity.entities.add(this.createPointEntity(data[4][itf], this.myConfigCollection.myfilteredData.defaultColor, this.myConfigCollection.myfilteredData.outlineColor))
      }
      if (data[5].length > 0) {
        console.log('immobility detected')
        // this.immobility = true
        for (var iti in data[5]) {
          this.myDetected_immoPrimitive.add(this.createPointPrimitive(data[5][iti], this.myConfigCollection.myImmobilityData.defaultColor, this.myConfigCollection.myImmobilityData.outlineColor))
        }
      }
    },
  },
  // Create collections and config object
  mounted () {
    var _this = this
    // MODIFIER AVEC THIS.EMIT DANS ImportData ET EVENT LISTENER DANS APP avec fonction https://www.telerik.com/blogs/how-to-emit-data-in-vue-beyond-the-vuejs-documentation
    _this.$root.$on('eventing', data => {
      // Creating Collections of points
      _this.dataReceived = data
      _this.myRawDataPrimitive = new _this._myCesium.PointPrimitiveCollection('my raw data') // new _this._myCesium.CustomDataSource('my raw data')
      _this.myRawDataEntity = new _this._myCesium.CustomDataSource()
      _this.myImpossibleDataPrimitive = new _this._myCesium.PointPrimitiveCollection()
      _this.myPrefilteredDataPrimitive = new _this._myCesium.PointPrimitiveCollection('my prefiltered data')
      _this.myPrefilteredDataEntity = new _this._myCesium.CustomDataSource()
      _this.myEliminatedDataPrimitive = new _this._myCesium.PointPrimitiveCollection('my eliminated data')
      _this.myEliminatedDataEntity = new _this._myCesium.CustomDataSource()
      _this.myfilteredDataPrimitive = new _this._myCesium.PointPrimitiveCollection('my filtered data')
      _this.myfilteredDataEntity = new _this._myCesium.CustomDataSource()
      _this.myDetected_immoPrimitive = new _this._myCesium.PointPrimitiveCollection()
      _this.myConfigCollection = {
        'myRawData': {
          defaultColor: 4294901760, // blue
          clickedColor: 4294901760,
          // clickedColor: 4278190335,//red
          outlineColor: 4294967295,
          references: _this.myRawDataPrimitive
        },
        'myImpossibleData': {
          defaultColor: 4278190080, // black
          clickedColor: 4278190080,
          outlineColor: 4294967295,
          // clickedOutlineColor: 4278255615,
          references: _this.myImpossibleDataPrimitive
        },
        'myPrefilteredData': {
          defaultColor: 4278232575, // orange
          clickedColor: 4278232575,
          outlineColor: 4294967295,
          references: _this.myPrefilteredDataPrimitive
        },
        'myEliminatedData': {
          defaultColor: 4278190335, // red
          clickedColor: 4294967295, // white
          outlineColor: 4278190080,
          references: _this.myEliminatedDataPrimitive
        },
        'myfilteredData': {
          defaultColor: 4278222848, // green
          clickedColor: 4278190335, // red
          outlineColor: 4294967295,
          references: _this.myfilteredDataPrimitive
        },
        'myImmobilityData': { //  à modifier
          defaultColor: 4286611584,// grey
          clickedColor: 4286611584,
          outlineColor: 4294967295,
          references: null,
          references: _this.myDetected_immoPrimitive
        }
      }
      var terrainProvider = _this._myViewer.terrainProvider
      if (data[4].length !== 0) {
        var position = data[4].map(function(item) { 
          return _this._myCesium.Cartographic.fromDegrees( Number(item.LON), Number(item.LAT),  Number(item.elevation) ) 
        })
        // var promise = this._myCesium.sampleTerrainMostDetailed(terrainProvider, position)
        var promise = this._myCesium.sampleTerrainMostDetailed(terrainProvider, position)
        this._myCesium.when(promise, function (updatedPositions) {
          for ( var i =0; i < updatedPositions.length; i++) {
            if (updatedPositions[i].height > _this.dataReceived[4][i].elevation) {
              _this.dataReceived[4][i].elevation = updatedPositions[i].height
            } 
            if (data[6] === 'Terrestrian' || data[6] === 'Aquatic') {
              _this.dataReceived[4][i].elevation = updatedPositions[i].height
            }
          }
          _this.instanciateCollection(_this.dataReceived)
          console.log('elevation', position[0].height)
          _this.displayCheckbox = true
        })
      } else {
        this.displayCheckbox = true
      }
    })
  },


  // NOT USED
  MakeListSameColor (collection, list, color) {
    for (var i = 0; i < collection.length; i++) {
      var p = collection.get(i)
      if (p._color.toRgba() === color) {
        list.push(p)
      }
    }
  }
}
</script>

<style>
@font-face {
 font-family: 'Exo';
 src: url("~@/assets/font/Exo2-Medium.ttf") format("ttf");
}
.viewer {
  width: 100%;
}
#app {
  font-family: 'Exo', 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  position: relative;
  height: calc(100vh - 88px);
  margin-top: 88px;
  font-size: 15px;
}
.col-4{
  padding-left: 30px;
  padding-right: 20px;
}
#parameters{
  margin-top: 30px;
}
div h2{
  background: #6eb0ed;
  color: #fff;
  text-transform: uppercase;
  text-align: left;
  padding: 10px;
  font-size: 1.1rem;
  position: relative;
}
div#technology h2:hover{
  cursor: pointer;
}
div#technology h2.collapsed:after{
  content: ' ';
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 7px 5.5px 0 5.5px;
  border-color: #fff transparent transparent transparent;
  position: absolute;
  right: 10px;
  top: 18px;
  transition: all 0.2s ease-in-out;
}
div#technology h2:not(.collapsed):after{
  content: ' ';
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 7px 5.5px 0 5.5px;
  border-color: #fff transparent transparent transparent;
  position: absolute;
  right: 10px;
  top: 18px;
  transition: all 0.2s ease-in-out;
  transform: rotate(180deg);
}
form div{
  display: inline-flex;
  width: 100%;
  margin-bottom: 15px;
}
form div label {
  width: 29%;
  text-align: left;
  line-height: 19px;
  margin-bottom: 0px;
}
form div select, form div input{
  width: 65%;
  border-radius: 0px !important;
}
form div:last-of-type label{
  margin-right: 0;
}
form div:last-of-type{
  justify-content: space-between;
}
form div:last-of-type label{
  width: 20%;
}
form div:last-of-type input{
  width: 27%;
}
/* FICHIER */
.fields{
  position: relative;
  margin: 20px 0px;
}
.fields input{
  width: 100%;
}
.fields input:focus{
  outline: none !important;
  border: none !important;
}
.fields button{
  width: 128px !important;
  font-size: 12px;
  position: absolute;
  padding: 5px 4px;
}
.fields button label{
  margin-bottom: 0px;
}
.fields button label:hover{
  cursor: pointer;
}
button:disabled{
  opacity: 0.6;
}
/* IMPORT */
#import{
  margin-bottom: 20px;
}
#import textarea{
  display: none;
}
/* #import button{
  margin-bottom: 10px;
} */
button{
  background: #1b568c;
  color: #fff;
  text-transform: uppercase;
  border: none;
  font-size: 1em;
  padding: 5px;
  width: 100%;
  -webkit-box-shadow: 0px 10px 9px -10px rgba(0,0,0,0.50);
  -moz-box-shadow: 0px 10px 9px -10px rgba(0,0,0,0.50);
  box-shadow: 0px 10px 9px -10px rgba(0,0,0,0.50);
}
/* CHECKBOXES */
#checkbox-group-1{
  display: inline-flex;
  flex-wrap: wrap;
}
.custom-control.custom-control-inline.custom-checkbox {
  width: 29%;
  margin-bottom: 10px;
  font-size: 15px;
}
/* PLAYER */
#player{
  border-top: solid 1px #6eb0ed;
  border-bottom: solid 1px #6eb0ed;
  padding-top: 10px;
  margin-bottom: 15px;
}
#player fieldset{
  margin-bottom: 0px;
}
#player fieldset div:first-of-type{
  display: inline-flex;
  flex-wrap: wrap;
  width: 100%;
}
#player fieldset legend{
  text-align: left;
  font-weight: bold;
  font-size: 1em;
}
#player fieldset div:first-of-type .custom-control.custom-control-inline.custom-radio{
  width: 29%;
  font-size: 15px;
  margin-bottom: 10px;
}
/* EXPORT */
#export{
  text-align: left;
}
#export button{
  font-size: 14px;
  width: fit-content;
  padding: 5px 15px;
}
/* TRANSPARENCE */
#globeOptions{
  width: fit-content;
  position: absolute;
  bottom: 0;
  left: 30%;
  transform: translateX(45%);
  display: inline-flex;
}
#globeOptions label{
  margin-bottom: 5px;
}
/* MAP */
#cesiumContainer{
  width: 66% !important;
  height: calc(100% - 120px) !important;
  position: fixed;
  top: 88px;
  bottom: 0;
  right: 0;
}
</style>
