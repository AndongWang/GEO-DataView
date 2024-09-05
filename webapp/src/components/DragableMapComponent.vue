<template>
    <div ref="mapContainer" class="map-container"></div>

    <!-- 弹出框 -->
    <div
      v-if="popupVisible"
      :style="{ left: popupPosition.x + 'px', top: popupPosition.y + 'px' }"
      class="popup"
      @mousedown="startDrag"
    >
      <div class="popup-header">
        <!-- <el-image
        style="width: 100px; height: 100px"
        :src="sampleImage"
        :zoom-rate="1.2"
        :max-scale="7"
        :min-scale="0.2"
        :preview-src-list="srcList"
        :initial-index="4"
        fit="cover"
      /> -->
        <div>监测点</div>
        <el-icon style="width:20px" :size="20" @click="popupVisible = !popupVisible"><Close /></el-icon>
      </div>
      <div style="display: flex;">
      <div class="popup-content">
        <!-- <div v-for="(value, key) in popupData" :key="key" class="popup-item">
          <span class="popup-key">{{ key }}</span>
          <span class="popup-value">{{ value }}</span>
        </div> -->
        <div v-for="(value, key) in popupData" :key="key" class="popup-item">
          <div class="key-value-pair" v-if="key != 'position'">
            <el-text class="popup-key">{{ translateKey(key) }}</el-text>
            <div>{{value}}</div>
            <!-- <el-input v-if="isNumber(value)" :value="value" readonly class="popup-value"></el-input>
            <el-input v-else :value="value" readonly class="popup-value"></el-input> -->
          </div>
        </div>
        <!-- <el-row :gutter="20">
          <el-col :span="12" v-for="(value, key) in popupData" :key="key" class="popup-item">
            <div class="key-value-pair">
              <el-text class="popup-key">{{ key }}</el-text>
              <div>{{value}}</div>
            </div>
          </el-col>
        </el-row> -->
      </div>
      <div style="width:500px;height:400px;overflow:auto">
        <img :src="sampleImage" alt="Image" class="popup-image" />
      </div>
    </div>
    </div>
</template>

<script>
/* global AMap */
import { ref, onMounted } from 'vue';
// import logo from '../assets/logo.png';
import { Close } from '@element-plus/icons-vue';
import supervsionData from './supervison-data.json';
import sampleImage from '../assets/supervison-img/image.png';

export default {
  components: {
    Close
  },
  setup() {
    const mapContainer = ref(null);
    const map = ref(null);
    const markers = ref([]);
    const popupVisible = ref(false);
    const popupData = ref({});
    const popupPosition = ref({ x: 0, y: 0 });
    const srcList = [sampleImage];
    let offsetX = 0;
    let offsetY = 0;
    // const logo1 = logo;
    const keyTranslations =  {
      monitoring_well_id: "监测井编号",
      well_depth_m: "井深/m",
      well_diameter_mm: "井管直径/mm",
      water_level_m: "水位/m",
      color: "颜色",
      odor: "气味",
      inspection_time: "核查时间",
      longitude: "经度",
      latitude: "纬度",
      obvious_pollution_traces: "明显污染痕迹",
      well_platform_height_m: "井台高度/m",
      well_pipe_material: "井管材质",
      water_level_meter_reading_m: "水位计读数/m",
      foreign_objects: "异物",
      pH_value: "pH 值",
      conductivity_us_cm: "电导率（us/cm）",
      temperature_C: "温度（℃）",
      dissolved_oxygen_mg_L: "溶解氧（mg/L）",
      oxidation_reduction_potential_mV: "氧化还原电位（mV）",
      turbidity_NTU: "浊度（NTU）"
    }

    const translateKey = (key) =>  {
      // 返回对应的中文描述，如果没有找到则返回原始key
      return keyTranslations[key] || key;
    }

    onMounted(() => {
      map.value = new AMap.Map(mapContainer.value, {
        zoom: 10,
        center: [123.22889,41.2063841],
        mapStyle: 'amap://styles/dark',
        viewMode: '3D',
        layers: [
          new AMap.TileLayer.Satellite(),
          new AMap.TileLayer.RoadNet()
        ]
      });

      addMarkers();
    });

    const isNumber = (value) => {
      return typeof value === 'number';
    }

    const addMarkers = () => {
      const dataPoints = supervsionData;
      console.log
      dataPoints.forEach(data => {
        const marker = new AMap.Marker({
          position: data.position,
          map: map.value
        });

        marker.on('click', (e) => {
          showPopup(data, e.pixel);
        });

        markers.value.push(marker);
      });
    };

    const showPopup = (data, position) => {
      popupData.value = data;
      popupPosition.value = position;
      popupVisible.value = true;
    };

    const startDrag = (event) => {
      offsetX = event.clientX - popupPosition.value.x;
      offsetY = event.clientY - popupPosition.value.y;

      document.addEventListener('mousemove', onDrag);
      document.addEventListener('mouseup', stopDrag);
    };

    const onDrag = (event) => {
      popupPosition.value = {
        x: event.clientX - offsetX,
        y: event.clientY - offsetY,
      };
    };

    const stopDrag = () => {
      document.removeEventListener('mousemove', onDrag);
      document.removeEventListener('mouseup', stopDrag);
    };

    return {
      mapContainer,
      popupVisible,
      popupData,
      popupPosition,
      showPopup,
      startDrag,
      isNumber,
      translateKey,
      sampleImage,
      srcList
    };
  }
};
</script>

<style>
.map-container {
  width: 100%;
  height: 100vh;
}

.popup {
  position: absolute;
  width: 250px;
  background-color: white;
  border: 1px solid #ccc;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  padding: 10px;
  cursor: move;
  width: 800px;
}

.popup-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.popup-image {
  width: 700px;
  height: 700px;
  margin-right: 10px;
}

.popup-title {
  font-weight: bold;
}

.popup-content {
  display: flex;
  flex-wrap: wrap;
  width: 248px;
  height: 400px;
  overflow: auto;
}

.popup-item {
  margin-bottom: 20px;
  width: 120px;
}

.key-value-pair {
  display: flex;
  flex-direction: column;
}

.popup-key {
  font-weight: bold;
}

.popup-value {
  margin-top: 5px;
}
</style>
