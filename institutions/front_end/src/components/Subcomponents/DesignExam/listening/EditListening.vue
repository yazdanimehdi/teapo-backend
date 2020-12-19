<template>
  <v-app>
    <v-app-bar absolute
               color="#1C0153"
               dark
               :height="height*0.1"
               src="@/assets/icon_group.png"
               style="margin: 0;position: fixed; z-index: 10; font-family: Kalam">
      <div style="font-weight: bold; font-size: 20px">Listening</div>
      <v-spacer></v-spacer>
      <v-btn icon to="/listening">
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
      <h1>Edit Listening</h1>
      <br/>
      <v-form v-model="valid">
        <v-select
            v-model="listeningType"
            :items="['Conversation', 'Lecture']"
            outlined
            label="Listening Type"
        ></v-select>

        <v-text-field
            label="Title"
            v-model="title"
            outlined
            :rules="[v => !!v || 'عنوان متن ضروری می‌باشد']"
            :disabled="sending"
        >
        </v-text-field>
        <v-file-input
            label="Listening Audio File"
            outlined
            @change="saveFileListening($event)"
            :prepend-icon="icons.mdiFile"
            :disabled="sending"
        ></v-file-input>
        <v-file-input
            label="Listening Picture"
            outlined
            @change="saveFileListeningPicture($event)"
            :prepend-icon="icons.mdiPictureInPictureTopRight"
            :disabled="sending"
        ></v-file-input>
        <v-textarea
            label="Transcript"
            height="600"
            outlined
            :rules="[v => !!v || 'متن شنیدار ضروری می‌باشد']"
            :disabled="sending"
            v-model="transcript"
        >
        </v-textarea>
        <v-btn
            block
            shaped
            color="success"
            style="font-weight: bold; font-size: 20px; margin-bottom: 90px"
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
import {mdiChevronRight, mdiChevronLeft, mdiFile, mdiPictureInPictureTopRight} from '@mdi/js'
import {ADD_NEW_LISTENING} from "@/store/actions/listening";
import {mapGetters} from 'vuex';

export default {
  name: "EditListening",
  data() {
    return {
      width: 0,
      height: 0,
      page: 1,
      valid: false,
      listeningType: 'Conversation',
      title: '',
      transcript: '',
      listeningFile: null,
      listeningPicture: null,
      snackbar: false,
      snackbarColor: 'error',
      snackbarMassage: 'خطایی رخ داده‌است دوباره تلاش کنید.',

      icons: {
        mdiChevronRight,
        mdiChevronLeft,
        mdiFile,
        mdiPictureInPictureTopRight
      },
      sending: false,
    }
  },
  created() {
    window.addEventListener('resize', this.handleResize);
    this.handleResize();
    this.title = this.listeningSelected.title
    this.transcript = this.listeningSelected.transcript
    this.listeningType = this.listeningSelected.type
  },
  computed: {
    ...mapGetters(['listeningSelected'])
  },
  methods: {
    handleResize() {
      this.width = window.innerWidth;
      this.height = window.innerHeight;
    },
    savePassage() {
      this.sending = true
      let bodyFormData = new FormData();
      bodyFormData.set('id', this.listeningSelected.id)
      bodyFormData.set('title', this.title);
      bodyFormData.set('type', this.listeningType);
      bodyFormData.set('transcript', this.transcript);

      if (this.listeningFile !== null) {
        bodyFormData.append('listening', this.listeningFile);
      }
      if (this.listeningPicture !== null) {
        bodyFormData.append('listening_image', this.listeningPicture);
      }
      this.$store.dispatch(ADD_NEW_LISTENING, bodyFormData).then(() => {
        this.sending = false;
        this.$router.push({name: 'Listening', params: { success: 'true'}});
      }).catch((err) => {
        console.log(err)
        this.snackbar = true
      })
    },

    saveFileListening(event) {
      this.listeningFile = event
    },
    saveFileListeningPicture(event) {
      this.listeningPicture = event
    }
  }
}
</script>

<style scoped>

</style>