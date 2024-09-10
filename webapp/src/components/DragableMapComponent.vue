<template>
  <div ref="mapContainer" class="map-container"></div>
  <PopupComponent
    v-for="point in dataList"
    :key="point.id"
    :popupPosition="(isShowInclude(point.id) && popupPositionList[point.id]) ? popupPositionList[point.id] : { x: 0, y: 0}"
    :visible="isShowInclude(point.id)"
    @closePopup="closePopup(point.id)"
    :popupData="point"
    >
  </PopupComponent>
        <!-- <div style="width:500px;height:400px;overflow:auto">
        <img :src="sampleImage" alt="Image" class="popup-image" />
      </div> -->
</template>

<script>
/* global AMap */
import { ref, onMounted } from 'vue';
import supervsionData from './supervision-data.json';
import PopupComponent from './PopupComponent.vue';

export default {
  components: {
    PopupComponent
  },
  setup() {
    const mapContainer = ref(null);
    const map = ref(null);
    const markers = ref([]);

    const dataList = ref([]);
    const popupShowList = ref([]);
    const popupPositionList = ref({});
    const isShowInclude = (key) => {
      return popupShowList.value.includes(key);
    };
    const closePopup = (key) => {
      popupShowList.value = popupShowList.value.filter(item => item !== key);
    };

    onMounted(() => {
      dataList.value = supervsionData;
      map.value = new AMap.Map(mapContainer.value, {
        zoom: 10,
        center: [123.22889, 41.2063841],
        mapStyle: 'amap://styles/dark',
        viewMode: '3D',
        layers: [
          new AMap.TileLayer.Satellite(),
          new AMap.TileLayer.RoadNet()
        ]
      });

      addMarkers();
    });

    const addMarkers = () => {
      const dataPoints = supervsionData;
      dataPoints.forEach(data => {
        const marker = new AMap.Marker({
          position: data.position,
          map: map.value,
          popupVisible: false,
          label: {
            content: data.id,  // 显示的名称
            offset: new AMap.Pixel(5, 5), // 标签的偏移量
            style: {
              'background-color': 'white',
              'border': '1px solid black',
              'border-radius': '3px',
              'padding': '2px 5px'
            }
          }
        });

        marker.on('click', (e) => {
          showPopup(data, e.pixel);
        });

        markers.value.push(marker);
      });
    };

    const showPopup = (data, position) => {
      if (!popupShowList.value.includes(data.id)) {
        popupShowList.value.push(data.id);
      } 
      popupPositionList.value[data.id] = position;
    };

    return {
      mapContainer,
      showPopup,
      closePopup,
      dataList,
      popupPositionList,
      isShowInclude,
    };
  }
};
</script>

<style>
.map-container {
  width: 100%;
  height: 100vh;
}
</style>
