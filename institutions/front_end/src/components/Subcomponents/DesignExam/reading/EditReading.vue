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
      <h1>Edit Reading</h1>
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
     <div class="text-center">
      <v-snackbar
          v-model="snackbar"
          :timeout="2000"
          :color="snackbarColor"
      >
        <v-btn
            color="#1C0153"
            text
            @click="snackbar = false"
        >
          بستن
        </v-btn>
        {{ snackbarMassage }}

      </v-snackbar>
    </div>
  </v-app>
</template>

<script>
import {mdiChevronRight, mdiChevronLeft} from '@mdi/js'
import {EDIT_READING} from "@/store/actions/reading";
import {mapGetters} from 'vuex';

export default {
  name: "EditReading",
  data() {
    return {
      width: 0,
      height: 0,
      page: 1,
      valid: false,
      snackbar: false,
      snackbarColor: 'error',
      snackbarMassage: 'خطایی رخ داده‌است دوباره تلاش کنید.',
      title: '',
      passage: '',
      icons: {
        mdiChevronRight,
        mdiChevronLeft
      },
      sending: false,
    }
  },
  computed: {
    ...mapGetters(['readingSelected']),
  },
  created() {
    window.addEventListener('resize', this.handleResize);
    this.handleResize();
    this.title = this.readingSelected.title
    let passage = this.readingSelected.passage
    passage = passage.replaceAll(/<pr id="\d">/g, '');
    passage = passage.replaceAll(/<p id="\d">/g, '');
    passage = passage.replaceAll('</p>', '\n');
    this.passage = passage;

  },
  methods: {
    handleResize() {
      this.width = window.innerWidth;
      this.height = window.innerHeight;
    },
    savePassage(){
      this.sending = true
      this.$store.dispatch(EDIT_READING, {'id': this.readingSelected.id, 'title': this.title, 'passage': this.passage}).then(() => {
        this.sending = false;
        this.$router.push({name: 'Reading', params: { success: 'true'}});
      }).catch((err) => {
        console.log(err)
        this.snackbar = true
      })
    },
  }
}
</script>

<style scoped>

</style>