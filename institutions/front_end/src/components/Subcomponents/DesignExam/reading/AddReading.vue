<template>
  <v-app>
    <v-app-bar absolute
               color="#1C0153"
               dark
               :height="height*0.1"
               src="@/assets/icon_group.png"
               style="margin: 0;position: fixed; z-index: 10; font-family: Kalam">
      <div style="font-weight: bold; font-size: 20px">Reading</div>
      <v-spacer></v-spacer>
      <v-btn icon to="/reading">
        <v-icon>{{ icons.mdiChevronRight }}</v-icon>
      </v-btn>
       <v-progress-linear
        :active="sending"
        :indeterminate="true"
        height="5"
        absolute
        bottom
        color="success"
      ></v-progress-linear>

    </v-app-bar>

    <div
        :style="{'margin-left':`${width*0.06}px`, 'margin-right': `${width*0.06}px`, 'margin-top': `${height*0.1 + 30}px`}"
        style="font-family: kalam">
      <h1>New Reading</h1>
      <br/>
      <v-form v-model="valid">
        <v-text-field
            label="Title"
            v-model="title"
            outlined
            :rules="[v => !!v || 'عنوان متن ضروری می‌باشد']"
            :disabled="sending"
        >
        </v-text-field>
        <v-textarea
            label="Passage"
            height="600"
            outlined
            :rules="[v => !!v || 'متن ضروری می‌باشد']"
            :disabled="sending"
            v-model="passage"
        >
        </v-textarea>
        <v-btn
            block
            shaped
            color="success"
            style="font-weight: bold; font-size: 20px"
            @click="savePassage"
            :disabled="sending || !valid"
        >
          Save
        </v-btn>
      </v-form>
    </div>
    <v-dialog width="600" v-model="dialog" persistent>
      <v-card width="600" height="100" style="font-family: dana;">
        <h2 style="font-weight: bold; color: limegreen;  text-align: center; padding-top: 20px">متن با موفقیت اضافه شد.</h2>
      </v-card>
        <v-btn color="success" style="font-family: dana; font-weight: bold; letter-spacing: 0" @click="resetAll">
          اضافه کردن متن جدید
        </v-btn>
        <v-btn color="error" style="font-family: dana; font-weight: bold; letter-spacing: 0" to="/reading">
          بازگشت به صفحه‌ی متن‌ها
        </v-btn>
    </v-dialog>
  </v-app>
</template>

<script>
import {mdiChevronRight, mdiChevronLeft} from '@mdi/js'
import {ADD_NEW_READING} from "@/store/actions/reading";

export default {
  name: "AddReading",
  data() {
    return {
      width: 0,
      height: 0,
      page: 1,
      valid: false,
      title: '',
      passage: '',
      dialog: false,
      icons: {
        mdiChevronRight,
        mdiChevronLeft
      },
      sending: false,
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
    savePassage(){
      this.sending = true
      this.$store.dispatch(ADD_NEW_READING, {'title': this.title, 'passage': this.passage}).then(() => {
        this.sending = false;
        this.dialog = true
      })
    },
    resetAll(){
      this.passage = ''
      this.title = ''
      this.dialog = false
    }
  }
}
</script>

<style scoped>

</style>