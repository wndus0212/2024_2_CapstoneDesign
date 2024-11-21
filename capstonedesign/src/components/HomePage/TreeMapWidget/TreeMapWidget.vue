<template>
  <container-box>
    <box-title>
      시장 한눈에 보기
    </box-title>
    <div style="display: flex; gap: 40px">
      <TreeMap/>
      <TreeMap/>
    </div>
  </container-box>
</template>

<script>
import containerBox from '@/components/Box.vue';
import boxTitle from '@/components/BoxTitle.vue';
import TreeMap from './TreeMap.vue';

export default{
  name: 'TreeMapWidget',
  components: {
    containerBox,
    boxTitle,
    TreeMap
  },
};
</script>

<style>
/* 필요에 따라 스타일 추가 */
</style>
