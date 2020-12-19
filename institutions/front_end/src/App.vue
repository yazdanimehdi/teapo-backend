<template>
  <v-app>
    <router-view/>
    <v-footer padless absolute color="#1C0153">
    <v-col
      class="text-center"
      cols="12"
      style="color: white"
    >
      {{ new Date().getFullYear() }} — <strong>TEAPO</strong>
    </v-col>
  </v-footer>
  </v-app>
</template>

<script>
import {mapGetters} from 'vuex'
export default {
  name: 'App',

  components: {
  },
  computed:{
    ...mapGetters(['isAuthenticated'])
  },
  watch: {
    isAuthenticated(newVal) {
      if (newVal === false) {
        this.$router.push('/login')
      }
    },
  },
  created() {
    if(this.isAuthenticated === false){
      this.$router.push('/login')
    }
  },
  data: () => ({
    //
  }),
};
</script>
