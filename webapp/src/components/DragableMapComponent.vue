<template>
  <el-button text @click="sidePanelVisible = true"
  >检测列表</el-button
  >
  <el-button text @click="showArea"
  >显示监测区域</el-button
  >
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
  <!-- 侧边栏弹框，展示树结构和Checkbox控制 -->
  <el-drawer 
    v-model="sidePanelVisible" 
    direction="ltr" 
    title="监测点列表">
    <el-tree
      :data="treeData"
      node-key="id"
      show-checkbox
      default-expand-all="false"
      :default-checked-keys="checkedKeys"
      @check="handleCheck"
      :props="defaultProps"
    >
    </el-tree>
  </el-drawer>
</template>

<script>
/* global AMap */
/* eslint-disable no-debugger */
import { ref, onMounted } from 'vue';
import supervsionData from './supervision-data.json';
import positionData from './positions.json';
import PopupComponent from './PopupComponent.vue';

export default {
  components: {
    PopupComponent
  },
  setup() {
    const mapContainer = ref(null);
    const map = ref(null);
    const markers = ref([]);
    const positions = ref([]);

    // map popup
    const dataList = ref([]);
    const popupShowList = ref([]);
    const popupPositionList = ref({});
    const isShowInclude = (key) => {
      return popupShowList.value.includes(key);
    };
    const closePopup = (key) => {
      popupShowList.value = popupShowList.value.filter(item => item !== key);
    };

    // sidenav
    const sidePanelVisible = ref(false);
    const treeData = ref([]);
    const checkedKeys = ref(['HC1']);

    const handleCheck = (data, { checkedKeys: newCheckedKeys }) => {
      checkedKeys.value = newCheckedKeys;
      const selectedMarkers = dataList.value.filter(i => newCheckedKeys.includes(i.id));
      map.value.clearMap();
      addMarkers(selectedMarkers)
      console.log(markers);
    };

    const defaultProps = ref({
      children: 'children',
      label: 'id'
    });

    const showArea = () => {
      // 创建折线实例，地图画线
      const polyline = new AMap.Polyline({
        path: positions.value,          // 设置线的坐标点
        borderWeight: 2,     // 线条宽度
        strokeColor: "#FF33FF",  // 线条颜色
        strokeOpacity: 1,    // 线条透明度
        strokeWeight: 3,     // 线条宽度
        strokeStyle: "solid", // 线条样式
        strokeDasharray: [10, 5] // 虚线样式
      });
      map.value.add(polyline);
    }

    onMounted(() => {
      dataList.value = supervsionData; // 
      treeData.value = [
        {
          id: "水质检测",
          label: "水质检测",
          children: supervsionData
        }
      ]; // 树点
      positions.value = positionData; // 地图线点
      checkedKeys.value = supervsionData.map(item => item.id);

      // 初始化地图组件
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

      // 创建折线实例，地图画线
      const polyline = new AMap.Polyline({
        path: positions.value,          // 设置线的坐标点
        borderWeight: 2,     // 线条宽度
        strokeColor: "#FF33FF",  // 线条颜色
        strokeOpacity: 1,    // 线条透明度
        strokeWeight: 3,     // 线条宽度
        strokeStyle: "solid", // 线条样式
        strokeDasharray: [10, 5] // 虚线样式
      });
      map.value.add(polyline);

      const dataPoints = supervsionData;
      addMarkers(dataPoints);
    });

    // 添加点位
    const addMarkers = (dataPoints) => {
      dataPoints.forEach(data => {
        const marker = new AMap.Marker({
          position: data.position,
          map: map.value,
          id: data.id,
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
      sidePanelVisible,
      treeData,
      handleCheck,
      defaultProps,
      positions,
      showArea
    };
  }
};
</script>

<style>
.map-container {
  width: 100%;
  height: 94vh;
}
</style>
