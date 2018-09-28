<template>
  <el-container class="is-vertical">
    <v-header></v-header>
    <el-main>
      <ul id="article_list">
        <li v-for="item in articleList">
          {{ item.title }}
        </li>
      </ul>
    </el-main>
  </el-container>
</template>

<script>
  export default {
    name: "index",
    data() {
      return {
        articleList: []
      }
    }, mounted() {
      this.getArticles()
    }, methods: {
      getArticles() {
        var vm = this;
        this.$http.get('http://127.0.0.1:8000/api/article/list/').then(function (res) {
          vm.articleList = res.data.data;
          console.log(vm.articleList);
        }).catch(function (err) {
          console.log(err)
        })
      }
    }

  }
</script>

<style scoped>

</style>
