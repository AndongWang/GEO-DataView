<template>
  <div id="map-container" ref="mapContainer" style="width: 100%; height: 100vh;"></div>
  <div v-if="popup.showPopup" :style="popup.popupStyle" class="custom-popup">
    <img :src="popup.popupContent.imageUrl" alt="Popup Image" class="popup-image" v-if="popup.popupContent.imageUrl" />

    <!-- Display JSON data in two columns -->
    <div class="popup-content">
      <div v-for="(value, key) in popup.popupContent" :key="key" class="popup-item">
        <span class="popup-key">{{ key }}</span>
        <span class="popup-value">{{ value }}</span>
      </div>
    </div>

    <button @click="closePopup">关闭</button>
  </div>
</template>

<script>
/* global AMap */
import { ref, onMounted, reactive } from 'vue';

export default {
  name: 'MapComponent',
  setup() {
    const mapContainer = ref(null); // 地图容器引用
    const map = ref(null); // 地图对象引用
    const markers = ref([]); // 存储所有的标记
    const popup = reactive({ // 弹窗相关的数据
      showPopup: false,
      popupContent: '',
      popupStyle: {
        position: 'absolute',
        left: '0px',
        top: '0px',
        backgroundColor: 'white',
        padding: '15px',
        borderRadius: '5px',
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.15)',
        zIndex: 1000,
      },
    });
    
    // 地图初始化
    onMounted(() => {
      map.value = new AMap.Map(mapContainer.value, {
        zoom: 10,
        center: [116.397428, 39.90923],
        mapStyle: 'amap://styles/dark',
        viewMode: '3D',
        layers: [
          new AMap.TileLayer.Satellite(),
          new AMap.TileLayer.RoadNet()
        ]
      });

      addMarkers();
    });

    // 添加标记函数
    const addMarkers = () => {
      const dataPoints = [
        { 
          position: [116.405285, 39.904989], 
          details: {
            imageUrl: 'https://example.com/imageA.jpg', // Main image URL
            title: '地点A',
            description: '这是地点A的描述，位于北京的心脏地带。',
            contact: '电话: 123-456-7890',
            website: '<a href="https://example.com" target="_blank">访问网站</a>',
            rating: '评分: 4.5/5',
            extraInfo: '更多信息A'
          }
        },
        { 
          position: [116.414251, 39.919349], 
          details: {
            imageUrl: 'https://example.com/imageB.jpg', // Main image URL
            title: '地点B',
            description: '地点B有着丰富的历史文化遗产，是游客的热门景点。',
            contact: '电话: 987-654-3210',
            website: '<a href="https://example.com" target="_blank">访问网站</a>',
            rating: '评分: 4.7/5',
            extraInfo: '更多信息B'
          }
        },
      ];

      dataPoints.forEach(data => {
        const marker = new AMap.Marker({
          position: data.position,
          map: map.value
        });

        marker.on('click', (e) => {
          showPopup(data.details, e.pixel);
        });

        markers.value.push(marker);
      });
    };

    // 显示弹窗
    const showPopup = (details, pixel) => {
      popup.popupContent = details;
      popup.popupStyle.left = `${pixel.getX()}px`;
      popup.popupStyle.top = `${pixel.getY()}px`;
      popup.showPopup = true;
    };

    // 关闭弹窗
    const closePopup = () => {
      popup.showPopup = false;
    };

    return {
      mapContainer,
      popup,  // Expose popup to the template
      closePopup,
    };
  },
};
</script>

<style scoped>
.custom-popup {
  position: absolute;
  background-color: white;
  padding: 15px;
  border-radius: 5px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 1000;
}
</style>
