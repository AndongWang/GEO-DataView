<template>
  <!-- 弹出框 -->
  <div v-if="visible" :style="{ left: currentPosition.x + 'px', top: currentPosition.y + 'px' }" class="popup"
    @mousedown="startDrag">
    <div class="popup-header">
      <div>监测点</div>
      <el-icon style="width:20px;hover:pointer" :size="20" @click="closePopup(popupData.id)">
        <Close />
      </el-icon>
    </div>
    <el-image style="width: 100px; height: 100px" :src="`/supervison-img/${popupData.id}.png`" :zoom-rate="1.2" :max-scale="7" :min-scale="0.2"
      :preview-src-list="[`/supervison-img/${popupData.id}.png`]" :initial-index="0" fit="cover" />
    <div style="display: flex;justify-content:center;align-items:center;overflow:auto">
      <div class="popup-content">
        <template v-for="(value, key) in popupData" :key="key">
          <div v-if="key != 'position'" class="popup-item">
            <div class="key-value-pair">
              <el-text class="popup-key">{{ translateKey(key) }}</el-text>
              <div>{{ value }}</div>
            </div>
          </div>
        </template>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch, onMounted } from 'vue';
import { Close } from '@element-plus/icons-vue';

export default {
  components: {
    Close
  },
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    popupData: {
      type: Object,
      default: () => ({})
    },
    popupPosition: {
      type: Object,
      default: () => ({ x: 0, y: 0 })
    }
  },
  setup(props, context) {
    const currentPosition = ref({ x: 0, y: 0 });
    let offsetX = 0;
    let offsetY = 0;
    const keyTranslations = {
      monitoring_well_id: "监测井编号",
      id: "监测井编号",
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

    const translateKey = (key) => {
      // 返回对应的中文描述，如果没有找到则返回原始key
      return keyTranslations[key] || key;
    }

    const closePopup = (key) => {
      // 向父组件发送关闭弹窗的事件
      context.emit('closePopup', key);
    }

    onMounted(() => {
      // console.log('init');
      // console.log(props.popupPosition.value);
      // currentPosition.value.x = props.popupPosition.value.x;
      // currentPosition.value.y = props.popupPosition.value.y;
    });

    watch(() => props.popupPosition, (newPosition) => {
      currentPosition.value = { ...newPosition };  // 更新为新的位置
    });
    const startDrag = (event) => {
      offsetX = event.clientX - currentPosition.value.x;
      offsetY = event.clientY - currentPosition.value.y;

      document.addEventListener('mousemove', onDrag);
      document.addEventListener('mouseup', stopDrag);
    };

    const onDrag = (event) => {
      currentPosition.value = {
        x: event.clientX - offsetX,
        y: event.clientY - offsetY,
      };
    };

    const stopDrag = () => {
      document.removeEventListener('mousemove', onDrag);
      document.removeEventListener('mouseup', stopDrag);
    };

    return {
      startDrag,
      translateKey,
      closePopup,
      currentPosition
    };
  }
};
</script>

<style>
.popup {
  position: absolute;
  width: 250px;
  background-color: white;
  border: 1px solid #ccc;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  padding: 10px;
  cursor: move;
  height: 500px;
  width: 300px;

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
    width: 300px;
    height: 350px;
    overflow: auto;
    justify-content: center;

    .popup-item {
      margin-bottom: 20px;
      width: 120px;

      .key-value-pair {
        display: flex;
        flex-direction: column;

        .popup-key {
          font-weight: bold;
        }

        .popup-value {
          margin-top: 5px;
        }
      }
    }
  }
}
</style>
