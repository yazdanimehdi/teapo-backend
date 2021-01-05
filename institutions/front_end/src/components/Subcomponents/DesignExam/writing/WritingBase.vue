<template>
  <v-app>
    <v-app-bar absolute
               color="#1C0153"
               dark
               :height="height*0.1"

               src="@/assets/icon_group.png"
               style="padding-top:8px;margin: 0;position: fixed; z-index: 10; font-family: Kalam">
      <div style="font-weight: bold; font-size: 20px">Reading</div>
      <v-spacer></v-spacer>
      <v-btn icon to="/">
        <v-icon>{{ icons.mdiChevronRight }}</v-icon>
      </v-btn>
    </v-app-bar>

    <div
        :style="{'margin-left':`${width*0.06}px`, 'margin-right': `${width*0.06}px`, 'margin-top': `${height*0.1 + 30}px`}"
        style="font-family: kalam">
      <v-card height="100" v-for="i in 6" :key="i" style="margin: 20px">
        <v-card-title>salam</v-card-title>
      </v-card>
      <div class="text-center">
        <v-pagination
            v-model="page"
            :length="4"
            circle
            :next-icon="icons.mdiChevronRight"
            :prev-icon="icons.mdiChevronLeft"
        ></v-pagination>
      </div>
    </div>
  </v-app>
</template>

<script>
import {mdiChevronRight, mdiChevronLeft} from '@mdi/js'

export default {
  name: "ReadingBase",
  data() {
    return {
      width: 0,
      height: 0,
      page:1,
      icons: {
        mdiChevronRight,
        mdiChevronLeft
      }
    }
  },
  created() {
    window.addEventListener('resize', this.handleResize);
    this.handleResize();
  },
  methods: {
    handleResize() {
      this.width = window.innerWidth;
      this.height = window.innerHeight;
    },
  }
}
</script>

<style scoped>

</style>