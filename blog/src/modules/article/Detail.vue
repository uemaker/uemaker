<template>
  <el-container class="is-vertical">
    <v-header></v-header>
    <el-main>
      <div class="article-content">
        <h3>{{ data.title }}</h3>
        <div v-html="data.content"></div>
      </div>
    </el-main>
  </el-container>
</template>

<script>
  export default {
    name: "ArticleDetail",
    data() {
      return {
        data: {}
      }
    }, mounted() {
      this.getData()
    }, methods: {
      getData() {
        var vm = this;
        var id = vm.$route.params.id
        this.$http.get('http://127.0.0.1:8000/api/article/detail/'+id+'/').then(function (res) {
          vm.data = res.data.data;
          console.log(vm.data);
        }).catch(function (err) {
          console.log(err)
        })
      }
    }

  }
</script>

<style scoped>

</style>
