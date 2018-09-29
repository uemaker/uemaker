<template>
  <el-container class="is-vertical">
    <v-header></v-header>
    <el-main>
      <el-row  class="item-list" v-for="item in articleList" >
        <el-col :xs="24" :sm="16" :md="16" :lg="20">
          <a href="javascript:void(0);" @click="redirect(item)" >{{ item.title }}</a>
        </el-col>
        <el-col class="hidden-sm-and-down" :xs="0" :sm="8" :md="8" :lg="4">
          <span style="float: right;">{{ item.create_time|moment("YYYY-MM-DD HH:mm") }}</span>
        </el-col>
      </el-row>
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
        this.$http.get('http://182.254.148.13/api/article/list/').then(function (res) {
          vm.articleList = res.data.data;
          console.log(vm.articleList);
        }).catch(function (err) {
          console.log(err)
        })
      },
      redirect:function(obj){
        var id = obj.id
        this.$router.push('/article/'+id);
      },
    }

  }
</script>

<style scoped>

</style>
