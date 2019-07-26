<template>
  <div id="app">
    <visualization></visualization>
    <ImportData @UpdateData='cleanCollection'></ImportData>
    <Export @downloadcsv='ManageData'></Export>
    <div class="viewer" ref="myViewer">
      <div id="interact_data" class="demo-tool">
        <div id='primitive' v-if="displayCheckbox">
          <input id = "rd" value="rd" name="checkboxp" type="checkbox" @change="onCheckboxCollectionChange($event)"/>
          <label for="rd">Raw data</label>
          <input id = "id" value="id" name="checkboxp" type="checkbox" @change="onCheckboxCollectionChange($event)"/>
          <label for="id">Impossible data</label>
          <input id = "pfd" value="pfd" name="checkboxp" type="checkbox" @change="onCheckboxCollectionChange($event)"/>
          <label for="pfd">prefiltereddata</label>
          <input id = "ed" value="ed" name="checkboxp" type="checkbox" @change="onCheckboxCollectionChange($event)"/>
          <label for="ed">eliminateddata</label>
          <input id = "fd" value="fd" name="checkboxp" type="checkbox" @change="onCheckboxCollectionChange($event)"/>
          <label for="fd">filtereddata</label>
          <button v-on:click="remove_point" >Remove point</button>
        </div>
        <div id='player' v-if="displayCheckbox">
          <input id = "rd" value="rd" type="radio" @change="collectionToAnimate($event)" v-model="picked"/>
          <label for="rd">Raw data</label>
          <input id = "pfd" value="pfd" type="radio" @change="collectionToAnimate($event)" v-model="picked"/>
          <label for="pfd">prefiltereddata</label>
          <input id = "ed" value="ed" type="radio" @change="collectionToAnimate($event)" v-model="picked"/>
          <label for="ed">eliminateddata</label>
          <input id = "fd" value="fd" type="radio" @change="collectionToAnimate($event)" v-model="picked"/>
          <label for="fd">filtereddata</label>
        </div>
        <div id='params'>
          <input id = "3DT" value="3DT" type="checkbox" @change="displayTransparency($event)"/>
          <label for="3DT">Terrain transparency</label>
        </div>
      </div>
      <cesium-viewer :animation="animation" @Tick="Tick" :camera="camera" :fullscreenButton="fullscreenButton" @ready="ready">
      <cesium-terrain-provider></cesium-terrain-provider>
      </cesium-viewer>
    </div>
  </div>
</template>

<script>
import visualization from './components/Visualization/visualization.vue'
import ImportData from './components/Import/ImportData.vue'
import Export from './components/Export/Export.vue'
import VueCesium from 'vue-cesium'
import Vue from 'vue'

Vue.use(VueCesium)

export default {
  name: 'App',
  components: {
    visualization,
    ImportData,
    Export
  },
  data () {
    // Cesium.BingMapsApi.defaultKey = 'AgqG7d1hd0psBdMyO3kPG8COGLUqA7knynwLSBkjiBRAnvRfOaOv1ZEl3GsDutjC'// ma key
    return {
      animation: false,
      fullscreenButton: true,
      timeline: false,
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
      mySelectedPoints: [],
      picked: []
    }
  },
  methods: {
    // Function that enables to update current time when selected by hand
    onTimelineScrubfunction (e) {
      this._myViewer.clock.currentTime = e.timeJulian
      // console.log(" set time ", this.lastestIndexFind)
      this.hideEntity(this.currentCollection,this.lastestIndexFind)
      this.displayedIndex = []
      var indexFinded = this.findNearIndexToDisplay(this.currentCollection, this._myViewer.clock.currentTime)
      // console.log(" ON A TROUVE ",indexFinded)
      if (indexFinded > -1) {
        this.drawEntity(this.currentCollection, indexFinded, indexFinded)
      }
      // this.initPlayer()
      //cacher les points affichéf
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
      if( minAndMaxDate.minDate.dayNumber == null || minAndMaxDate.maxDate.dayNumber == null ) {
        this.customDestroyTimeline()
      }
      else {
        this.animation = selection
        this.timeline = selection
        var startDate = new this._myCesium.JulianDate(minAndMaxDate.minDate.dayNumber , minAndMaxDate.minDate.secondsOfDay )
        var endDate = new this._myCesium.JulianDate(minAndMaxDate.maxDate.dayNumber , minAndMaxDate.maxDate.secondsOfDay )
        if ((!this._myCesium.defined(this._myViewer.timeline) || this._myViewer.timeline.isDestroyed()) && this.timeline == true) {
          this.customCreateTimeline (startDate, endDate) 
          // this._myViewer._forceResize = true
          // this._myViewer.resize()
        }
      }
    },
    // Linked to checkbox Terrain transparency and permit to display and remove transparency of 3D layer
    displayTransparency (event) {
      var selection = event.target.checked
      this._myViewer.scene.globe.depthTestAgainstTerrain = selection
    },
    // Function to hide and show points from primitive collections
    // ShowPoints (collection, selection) {
    //   for (var i = 0; i < collection.length; i++) {
    //     var p = collection.get(i)
    //     p.show = selection
    //   }
    // },
    // Function linked to checkboxes to hide and show primitive collections
    cleanPlayer() {
      var allcheckbox = document.querySelectorAll('div#player input')
      for (var i = 0 ; i < allcheckbox.length ; i++ ) {
        allcheckbox[i].checked = false
      }
      if(this._myViewer.dataSources.length) {
        this._myViewer.dataSources.removeAll()
      }
      this._myViewer.entities.removeAll()
      this.customDestroyTimeline()
    },
    onCheckboxCollectionChange (event) {
      var selection = event.target.checked
      this.lastCheckBoxChecked = event.target.value
      this.cleanPlayer()
      switch (this.lastCheckBoxChecked) {
        case 'rd': {
          console.log(this.myRawDataPrimitive)
          if(selection === false) {
            this._myViewer.scene.primitives.remove(this.myRawDataPrimitive)
          } else {
            console.log('on add')
            this._myViewer.scene.primitives.add(this.myRawDataPrimitive)
          }
          break
        }
        case 'id': {
          if(selection === false) {
            this._myViewer.scene.primitives.remove(this.myRawDataPrimitive)
          } else {
            this._myViewer.scene.primitives.add(this.myRawDataPrimitive)
          }
          break
        }
        case 'pfd': {
          this._myViewer.scene.primitives.add(this.myPrefilteredDataPrimitive)
          if(selection === false) {
            this._myViewer.scene.primitives.show = false
          } else {
            
          }
          break
        }
        case 'ed': {
          if(selection === false) {
            this._myViewer.scene.primitives.remove(this.myEliminatedDataPrimitive)
          } else {
            this._myViewer.scene.primitives.add(this.myEliminatedDataPrimitive)
          }
          break
        }
        case 'fd': {
          if(selection === false) {
            this._myViewer.scene.primitives.remove(this.myfilteredDataPrimitive)
          } else {
            this._myViewer.scene.primitives.add(this.myfilteredDataPrimitive)
          }
          break
        }
        default: {
          console.log('should never be here')
          break
        }
      }

    },
    // functions to create the points primitives from imported data
    createPointPrimitive (options, color, outlineColor) {
      return new this._myCesium.PointPrimitive(
        {
          id: options.id,
          show: true,
          allowPicking: true,
          color: this._myCesium.Color.fromRgba(color),
          outlineColor: this._myCesium.Color.fromRgba(outlineColor),
          outlineWidth: 2,
          position: this._myCesium.Cartesian3.fromDegrees(options.LON, options.LAT, options.elevation, this._myCesium.Ellipsoid.WGS84)
        }
      )
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
      var collectionEntity = collectionEntity.entities
      var minDate = {
        dayNumber: null,
        secondsOfDay: null
      }
      var maxDate = {
        dayNumber: null,
        secondsOfDay: null
      }
      if (collectionEntity.values.length > 0) {
        var firstItem = collectionEntity.values[0]
        minDate.dayNumber = firstItem._date.dayNumber
        minDate.secondsOfDay = firstItem._date.secondsOfDay
        maxDate.dayNumber = firstItem._date.dayNumber
        maxDate.secondsOfDay = firstItem._date.secondsOfDay
        for (var item in collectionEntity.values) {
          var curDay = collectionEntity.values[item]._date.dayNumber
          var curSeconds = collectionEntity.values[item]._date.secondsOfDay
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
      return {
        minDate,
        maxDate
      }
    },
    // SERT A RIEN POUR LE MOMENT
    DisplayPoint (collectionEntity, startDate, endDate) {
      var animationpoint = model.activeAnimations.add({
        name: 'DisplayPoints',
        startTime: startDate,
        delay: 0.0, // Play at startTime (default)
        stopTime: endDate,
        removeOnStop: false, // Do not remove when animation stops (default)
        multiplier: 2.0, // Play at double speed
        reverse: true, // Play in reverse
        loop: this._myCesium.ModelAnimationLoop.REPEAT // Loop the animation
      })

      // for(var point in collectionEntity) {
      //   if point.date ==
      // }
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
      var selection = event.target.checked
      var value = event.target.value
      // Hide primitive collections
      this._myViewer.scene.primitives.removeAll()
      // Uncheck all the checkboxes
      var allcheckbox = document.querySelectorAll('div#primitive input')
      for (var i = 0 ; i < allcheckbox.length ; i++ ) {
        allcheckbox[i].checked = false
      }
      this.collectiontoplay = value
      this.initPlayer()
      this.currentCollection = null
      // config of timeline
      var minAndMaxDate = {}
      if(this._myViewer.dataSources.length) {
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
          debugger
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
        default: {
          console.log('should never be here')
          break
        }
      }
    },
    initPlayer() {
      this.lastestIndexFind = -1
      this.normal = 0
      this.reverse = 0
      this.displayedIndex = []
      this.maxHistory = 10
      this.maxPolylines = 2
      this.polylineCollection = new this._myCesium.PolylineCollection()
      if ( this.currentCollection ) {
        this.hideEntity(this.currentCollection,this.currentCollection.entities.values.length-1)
      }
    },
    findNearIndexToDisplay(collection, date) {
      var startingIndex = 0
      var arrCollection = collection.entities.values
      var startingIndexSeconds = -1
      var matchedIndex = -1
      for (var i = startingIndex ; i < arrCollection.length ; i ++) {
        var entityDate = arrCollection[i].date

        if ( entityDate.dayNumber <= date.dayNumber ) {
          if ( entityDate.dayNumber < date.dayNumber) {
            startingIndexSeconds = i
          }
          if ( entityDate.dayNumber == date.dayNumber )  {
            if ( entityDate.secondsOfDay <= date.secondsOfDay) {
            startingIndexSeconds = i
            }
            else {
              break
            }
          }
        }
        else {
          break
        }
      }
      if ( startingIndexSeconds > -1 ) {
        if ( arrCollection[startingIndexSeconds].date.dayNumber < date.dayNumber ) {//special case
            matchedIndex = startingIndexSeconds
        }  
        else {
          for ( var j = startingIndexSeconds; j < arrCollection.length ; j ++) {
            var entityDate = arrCollection[j].date
            if ( entityDate.secondsOfDay <= date.secondsOfDay && entityDate.dayNumber <= date.dayNumber) {
              matchedIndex = j
            }
            else {
              break
            }
          }
        }
      }
      else {
        console.log("something goes wrong we should not be there")
      }
      if (matchedIndex == -1 ) {
        return startingIndexSeconds
      }
      else {
        return matchedIndex
      }
    },
    findNearIndexToDisplayBackwards(collection, date) {
      console.log("on est dans le passé")
      var startingIndex = 0
      var arrCollection = collection.entities.values
      var startingIndexSeconds = -1
      var matchedIndex = -1
      for (var i = startingIndex ; i < arrCollection.length ; i ++) {
        var entityDate = arrCollection[i].date
        if ( entityDate.dayNumber <= date.dayNumber ) {
          if ( entityDate.dayNumber < date.dayNumber) {
            startingIndexSeconds = i
          }
          if ( entityDate.dayNumber == date.dayNumber )  {
            if ( entityDate.secondsOfDay <= date.secondsOfDay) {
            startingIndexSeconds = i
            }
            else {
              break
            }
          }
        }
        else {
          break
        }
      }
      if ( startingIndexSeconds > -1 ) {
        if ( arrCollection[startingIndexSeconds].date.dayNumber < date.dayNumber ) {//special case
            matchedIndex = startingIndexSeconds
        }  
        else {
          for ( var j = startingIndexSeconds; j < arrCollection.length ; j ++) {
            var entityDate = arrCollection[j].date
            if ( entityDate.secondsOfDay <= date.secondsOfDay && entityDate.dayNumber <= date.dayNumber) {
              matchedIndex = j
            }
            else {
              break
            }
          }
        }
      }
      else {
        console.log("something goes wrong we should not be there")
      }

      if (matchedIndex == -1 ) {
        return startingIndexSeconds
      }
      else {
        return matchedIndex
      }
    },
    findIndexToDisplay(collection, date) {
      var startingIndex = 0
      if ( this.lastestIndexFind > -1) {
         startingIndex = this.lastestIndexFind
      }
      var arrCollection = collection.entities.values
      var startingIndexSeconds = -1
      var matchedIndex = -1


      for (var i = startingIndex ; i < arrCollection.length ; i ++) {
        var entityDate = arrCollection[i].date
        if ( entityDate.dayNumber === date.dayNumber ) {
          startingIndexSeconds = i
          break
        }
      }

      if ( startingIndexSeconds > -1 ) {
        for ( var j = startingIndexSeconds; j < arrCollection.length ; j ++) {
          var entityDate = arrCollection[j].date

          if ( entityDate.secondsOfDay <= date.secondsOfDay && entityDate.dayNumber <= date.dayNumber) {
            matchedIndex = j
          }
          else {
            break
          }
        }
      }
      else {
        console.log("something goes wrong we should not be there")
      }
      if (matchedIndex == this.lastestIndexFind ) {
        return -1
      }
      return matchedIndex
    },
    storeHistory(index){
      if( this.displayedIndex.length >= this.maxHistory ) { // tableau plein
          this.displayedIndex.pop() // enlève l'élément d'index le plus haut
          //hide entity
      }
      if ( this.displayedIndex.length > 0 ) {
        if( this.displayedIndex[0] != index ) { // to only have different indexes
          this.displayedIndex.unshift(index) // to add a new element with index 0
        }
      } else {
        this.displayedIndex.unshift(index)
      }
    },
    // storeHistoryReverse(index){
    //   if( this.displayedIndex.length >= this.maxHistory ) { // tableau plein
    //       this.displayedIndex.shift() // enlève l'élément d'index le plus bas
    //       //hide entity
    //   }
    //   if ( this.displayedIndex.length > 0 ) {
    //     if( this.displayedIndex[0] != index ) { // to only have different indexes
    //       this.displayedIndex.push(index) // to add a new element with index max
    //     }
    //   } else {
    //     this.displayedIndex.push(index)
    //   }
    // },
    drawPolylines(nbToDraw) {
      var nbPolyLinesDraw = 0
      var nbToDel = this._myViewer.entities.values.length - this.maxPolylines
      if ( nbToDel >  0 ) {
        for( var j = 0 ; j < nbToDel ; j++) {
          var curEntity = this._myViewer.entities.values[j]
          this._myViewer.entities.remove(curEntity)
        }
      }
      for (var i = 0 ; i <= nbToDraw ; i++ ) {
        if ( i + 1 < this.displayedIndex.length ) {
          var lastEntityindex = this.displayedIndex[i]
          var beforeLastEntityIndex = this.displayedIndex[i+1]
          // get points positions       
          var firstPoint =  this.currentCollection.entities.values[beforeLastEntityIndex]
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
                  this._myCesium.Cartographic.fromDegrees(lonf,latf,f.height),
                  this._myCesium.Cartographic.fromDegrees(lonl,latl,l.height)
                ]
              ),
              width : 2,
              material: this._myCesium.Color.RED
              // clampToGround: true
              // followSurface: new this._myCesium.ConstantProperty(true)
            }
          })
          }
        }       
      },
    drawEntity(collection, startingIndex, endingIndex ) {
      for (var i = startingIndex; i <= endingIndex; i++) {
        this.storeHistory(i)
        collection.entities.values[i].show = true
        if (this.displayedIndex.length > 1) {
          var nbLinesToDraw = -1 // equals nb lines to draw - 1 because Starting index = lastIndexFind+1
          nbLinesToDraw = endingIndex - startingIndex
          this.drawPolylines(nbLinesToDraw)
        }
      }
      this.lastestIndexFind = endingIndex
    },
    drawEntityReverse(collection, minIndex, maxIndex ) {
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
    hideEntity(collection, index) {
      var arrCollection = collection.entities.values
      for( var i = 0; i <= index; i++ ) {
        arrCollection[i].show = false
      }
    },
    hideEntityReverse(collection, index) {
      var arrCollection = collection.entities.values
      for( var i = index; i >= 0; i-- ) {
        arrCollection[i].show = false
      }
    },
    player(collection,date) { 
      if (this._myViewer.clock._multiplier > 0) {
        var indexFinded = this.findIndexToDisplay(collection, date)
        if (indexFinded > -1 ) {
          if ( this.lastestIndexFind == -1 ) {
            this.drawEntity(collection, 0, indexFinded) 
          } else {
            this.hideEntity(collection, this.lastestIndexFind)
            this.drawEntity(collection, this.lastestIndexFind+1, indexFinded)
          }
        }
      } else {
        var indexFinded = this.findNearIndexToDisplay(collection, date)
        if (indexFinded > -1 ) {
          if ( this.lastestIndexFind == -1 ) {
            console.log('on peut pas reverse depuis le début') 
          } else {
            this.hideEntityReverse(collection, this.lastestIndexFind)
            this.drawEntityReverse(collection, indexFinded, this.lastestIndexFind-1)
          }
        }
      }
    },
    displayEntity(collection, matchedIndex, latestIndex) {
      for( var j = 0 ; j < matchedIndex ; j++ ) {
        collection.entities.values[j].show = false
      }

      if (typeof(latestIndex) == 'undefined') {
        collection.entities.values[matchedIndex].show = true
        return
      }
      for( var i = latestIndex ; i < matchedIndex ; i++ ) {
        collection.entities.values[i].show = true
      }

    },
    // function thats exec at each tick of the clock when it plays
    Tick (event) {
      if (event.shouldAnimate && event.canAnimate) {
        var date = event._currentTime
        if (this._myViewer.clock._multiplier > 0) {
          if (this.normal = 0) {
            this.displayedIndex = []
          }
          this.normal = 1
          this.reverse = 0
        } else {
          if (this.reverse = 0) {
            this.displayedIndex = []
          }
          this.reverse = 1
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
        // _this.myRawDataPrimitive._pointPrimitives.find(function(item) {  return item.id == selectPoint.id } )
        var selectPoint = viewer.scene.pick(movement.position)
        var selectCollection = selectPoint.collection // To know in which collection we are
        var PointColorRgba = selectPoint.primitive._color.toRgba() // to know the point's color
        for (var item in _this.myConfigCollection) {
          if (selectCollection === _this.myConfigCollection[item].references) { // to find matching collection
            if (PointColorRgba === _this.myConfigCollection[item].defaultColor) { // to know in what color is the point and give him the other one
              selectPoint.primitive.color = Cesium.Color.fromRgba(_this.myConfigCollection[item].clickedColor)
              _this.mySelectedPoints.push(selectPoint)
            } else {
              selectPoint.primitive.color = Cesium.Color.fromRgba(_this.myConfigCollection[item].defaultColor)
              _this.findAndRemovePointSelected(selectPoint) // when point is clicked on a second time , give back default color and delete from selected point list
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
    // Function to delete a point from a collection and add it to another
    remove_point () {
      for (var point in this.mySelectedPoints) {
        var pointEntity = this.myfilteredDataEntity.getById(this.mySelectedPoints[point].primitive._id)
        if (pointEntity === undefined) {
          pointEntity = this.myEliminatedDataEntity.getById(this.mySelectedPoints[point].primitive._id)
          this.myfilteredDataEntity.add(
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
              show: false,
              allowPicking: true,
              color: this._myCesium.Color.fromRgba(this.myConfigCollection.myfilteredData.defaultColor),
              outlineColor: this._myCesium.Color.YELLOW,
              outlineWidth: 2,
              position: new this._myCesium.Cartesian3(this.mySelectedPoints[point].primitive._position.x, this.mySelectedPoints[point].primitive._position.y, this.mySelectedPoints[point].primitive._position.z)
            }
          )
          this.myEliminatedDataPrimitive.remove(this.mySelectedPoints[point].primitive)
          this.myEliminatedDataEntity.remove(pointEntity)
        } else {
          this.myEliminatedDataEntity.add(
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
              show: false,
              allowPicking: true,
              color: this._myCesium.Color.fromRgba(this.myConfigCollection.myEliminatedData.defaultColor),
              outlineColor: this._myCesium.Color.YELLOW,
              outlineWidth: 2,
              position: new this._myCesium.Cartesian3(this.mySelectedPoints[point].primitive._position.x, this.mySelectedPoints[point].primitive._position.y, this.mySelectedPoints[point].primitive._position.z)
            }
          )
          this.myfilteredDataPrimitive.remove(this.mySelectedPoints[point].primitive)
          this.myfilteredDataEntity.remove(pointEntity)
        }
      }
      // _this.myRawDataPrimitive._pointPrimitives.find(function(item) {  return item.id == selectPoint.id } )
      this.mySelectedPoints = []
    },
    // remove_point () {
    //   // var SelectedPoint = this._myViewer.selectedEntity
    //   // // console.log('on est dans remove_point', SelectedPoint)
    //   // SelectedPoint.entityCollection.remove(SelectedPoint)
    // },
    // Function to give data from entitescollections same shape as backapp and then send it to export2 to make csv
    ManageData () {
      // alert(' ok managedata')
      if (typeof (this.myRawDataEntity) === 'undefined' || typeof (this.myEliminatedDataEntity) === 'undefined' || typeof (this.myfilteredDataEntity) === 'undefined') { // METTRE LES CONDITIONS POUR LES AUTRE
        alert('Import data first')
      } else {
        var dataPoints = []
        for (var i = 0; i < this.myfilteredDataEntity.values.length; i++) {
          // var p = this.myfilteredDataPrimitive.get(i)
          var item = this.myfilteredDataEntity.values[i]
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
      }
    },
    // to clean everything before importing new data
    cleanCollection () { 
      // console.log('update du front')
      if (this.myRawDataPrimitive || this.myPrefilteredDataPrimitive || this.myEliminatedDataPrimitive || this.myfilteredDataPrimitive) {
        if (confirm('You are going to loose current data, do you still want to proceed ?')) {
          // to destroy the collection and erase points from viewer
          this.myRawDataPrimitive.destroy()
          this.myPrefilteredDataPrimitive.destroy()
          this.myEliminatedDataPrimitive.destroy()
          this.myfilteredDataPrimitive.destroy()
          this.myRawDataEntity.entities.removeAll()
          this.myPrefilteredDataEntity.entities.removeAll()
          this.myEliminatedDataEntity.entities.removeAll()
          this.myfilteredDataEntity.entities.removeAll()
          this._myViewer.entities.removeAll()
          // to uncheck checkboxes
          var allcheckbox = document.querySelectorAll('div#primitive input')
          for (var i = 0 ; i < allcheckbox.length ; i++ ) {
            allcheckbox[i].checked = false
          }
          var allcheckbox = document.querySelectorAll('div#player input')
          for (var i = 0 ; i < allcheckbox.length ; i++ ) {
            allcheckbox[i].checked = false
          }
          this.customDestroyTimeline()
          // document.getElementById('rd').checked = false
          // document.getElementById('pfd').checked = false
          // document.getElementById('ed').checked = false
          // document.getElementById('fd').checked = false
        }
      }
    }
  },
  // Create collections and config object
  mounted () {
    var _this = this
    // MODIFIER AVEC THIS.EMIT DANS ImportData ET EVENT LISTENER DANS APP avec fonction https://www.telerik.com/blogs/how-to-emit-data-in-vue-beyond-the-vuejs-documentation
    _this.$root.$on('eventing', data => {
      // Creating Collections of points
      this.displayCheckbox = true
      _this.myRawDataPrimitive = new _this._myCesium.PointPrimitiveCollection('my raw data') // new _this._myCesium.CustomDataSource('my raw data')
      _this.myRawDataEntity = new _this._myCesium.CustomDataSource()
      // _this.RDate = new _this.myCesium.TimeIntervalCollection()
      _this.myImpossibleDataPrimitive = new _this._myCesium.PointPrimitiveCollection()
      _this.myPrefilteredDataPrimitive = new _this._myCesium.PointPrimitiveCollection('my prefiltered data')
      _this.myPrefilteredDataEntity = new _this._myCesium.CustomDataSource()
      _this.myEliminatedDataPrimitive = new _this._myCesium.PointPrimitiveCollection('my eliminated data')
      _this.myEliminatedDataEntity = new _this._myCesium.CustomDataSource()
      _this.myfilteredDataPrimitive = new _this._myCesium.PointPrimitiveCollection('my filtered data')
      _this.myfilteredDataEntity = new _this._myCesium.CustomDataSource()
      _this.Detected_immoPrimitive = new _this._myCesium.PointPrimitiveCollection()
      _this.myConfigCollection = {
        'myRawData': {
          defaultColor: 4294901760,
          clickedColor: 4294901760,
          // clickedColor: 4278190335,//red
          outlineColor: 4294967295,
          references: _this.myRawDataPrimitive
        },
        'myImpossibleData': {
          defaultColor: 4278190080,
          clickedColor: 4278190080,
          outlineColor: 4294967295,
          // clickedOutlineColor: 4278255615,
          references: _this.myImpossibleDataPrimitive
        },
        'myPrefilteredData': {
          defaultColor: 4286611584,
          clickedColor: 4286611584,
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
        _this.myRawDataEntity.entities.add(_this.createPointEntity(data[0][itr], _this.myConfigCollection.myRawData.defaultColor, _this.myConfigCollection.myRawData.outlineColor))
        // dates.push(data[0][itr]['date'])
      }
      // console.log('les dates', dates)
      // console.log('la collection', _this.myRawDataPrimitive)
      // debugger
      // _this.RDates = this._myCesium.TimeIntervalCollection.fromIso8601DateArray({
      //   iso8601Dates: dates
      // })
      // console.log('les dates en collection', _this.RDate)
      for (var itp in data[1]) {
        _this.myPrefilteredDataPrimitive.add(_this.createPointPrimitive(data[1][itp], this.myConfigCollection.myPrefilteredData.defaultColor, _this.myConfigCollection.myPrefilteredData.outlineColor))
        _this.myPrefilteredDataEntity.entities.add(_this.createPointEntity(data[1][itp], this.myConfigCollection.myPrefilteredData.defaultColor, _this.myConfigCollection.myPrefilteredData.outlineColor))
      }
      for (var ite in data[2]) {
        _this.myImpossibleDataPrimitive.add(_this.createPointPrimitive(data[2][ite], this.myConfigCollection.myImpossibleData.defaultColor, _this.myConfigCollection.myImpossibleData.outlineColor))
      }
      // for (var itf = 0; itf < data[3].length - 1; itf++) {
      for (var itf in data[3]) {
      //   _this.fpolylines = _this._myViewer.entities.add(new _this._myCesium.Entity()) // to create segments between consecutive points
        _this.myfilteredDataPrimitive.add(_this.createPointPrimitive(data[3][itf], this.myConfigCollection.myfilteredData.defaultColor, _this.myConfigCollection.myfilteredData.outlineColor)) // to create points
        _this.myfilteredDataEntity.entities.add(_this.createPointEntity(data[3][itf], this.myConfigCollection.myfilteredData.defaultColor, _this.myConfigCollection.myfilteredData.outlineColor))
        // To create lines
        _this.Rawlines = new _this._myCesium.PolylineCollection()
        // _this.CreatePolylines(_this.myRawDataPrimitive, _this.Rawlines)
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
