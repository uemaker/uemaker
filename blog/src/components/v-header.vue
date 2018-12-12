<template>
  <el-header>
    <el-menu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" @select="handleSelect">
      <el-menu-item index="1">首页</el-menu-item>
      <el-submenu index="2">
        <template slot="title">编程</template>
        <el-menu-item index="2-1">PHP</el-menu-item>
        <el-menu-item index="2-2">JAVA</el-menu-item>
        <el-menu-item index="2-3">PYTHON</el-menu-item>
      </el-submenu>
      <el-menu-item index="3">架构之路</el-menu-item>
      <el-menu-item index="4">项目管理</el-menu-item>
    </el-menu>
    </el-header>
</template>

<script>
  export default {
    name: "v-header",
    data() {
      return {
        activeIndex: '1',
        activeIndex2: '1'
      };
    },
    methods: {
      handleSelect(key, keyPath) {
        console.log(key, keyPath);
      }
    }
  }
</script>

<style scoped>

</style>
