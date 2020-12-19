<template>
  <v-app>
    <v-app-bar absolute
               color="#1C0153"
               dark
               :height="height*0.1"

               src="@/assets/icon_group.png"
               style="padding-top:8px;margin: 0;position: fixed; z-index: 10; font-family: Kalam">
      <div style="font-weight: bold; font-size: 20px">Listening</div>
      <v-spacer></v-spacer>
      <v-btn icon to="/">
        <v-icon>{{ icons.mdiChevronRight }}</v-icon>
      </v-btn>
    </v-app-bar>

    <div v-if="loading" style="text-align: center; margin-top: 100px">
      <v-progress-circular indeterminate size="50"></v-progress-circular>
    </div>
    <div
        v-else
        :style="{'margin-left':`${width*0.06}px`, 'margin-right': `${width*0.06}px`, 'margin-top': `${height*0.1 + 30}px`}"
        style="font-family: kalam; margin-bottom: 100px">

      <v-container fluid style="padding: 0">
        <v-row>
          <v-col cols="12" sm="8" md="6" lg="6" xl="6" style="padding: 0">
            <v-text-field
                v-model="searchText"
                label="Search"
                filled
                rounded
                dense
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="4" md="6" lg="6" xl="6" style="text-align: right; padding: 0">
            <v-btn icon
                   width="60" height="60" to="/add_listening">
              <v-icon color="success" large>{{ icons.mdiPlusBox }}</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-container>


      <v-card v-for="listening in paginatedList" :key="listening.id" style="margin-top: 10px">
        <v-container fluid>
          <v-row>
            <v-hover v-slot:default="{ hover }">
              <v-col cols="12" sm="8" md="6" lg="6" xl="6" @click="openPassage(listening.transcript)"
                     :style="{ 'cursor': hover ? 'pointer' : ''}">
                <h2>{{ listening.id }}. {{listening.type}}. {{ listening.title }}</h2>
                <audio id="music" preload="metadata" controls>
                  <source :src="'http://127.0.0.1:8000' + listening.listening"> <!-- audio file-->
                </audio>
                <h4 style="color: rgba(0, 0, 0, 0.5)">
                  <span v-for="(test, index) in listening['tests']" :key="`t${index}`">{{ test }}, </span>
                </h4>
              </v-col>
            </v-hover>
            <v-col cols="12" sm="4" md="6" lg="6" xl="6" style="text-align: right">
              <v-btn
                  x-large @click="goToQuestions(listening)">
                Questions
              </v-btn>
              <v-btn icon
                     x-large @click="editReading(listening)">
                <v-icon color="blue">{{ icons.mdiBookEdit }}</v-icon>
              </v-btn>
              <v-btn icon
                     x-large @click="deleteDialogFunction(listening.id)">
                <v-icon color="red">{{ icons.mdiTrashCan }}</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
      <div class="text-center" style="margin-top: 20px">
        <v-pagination
            v-model="page"
            :length="readingNumberOfPages"
            circle
            :next-icon="icons.mdiChevronRight"
            :prev-icon="icons.mdiChevronLeft"
        ></v-pagination>
      </div>
    </div>
    <v-dialog width="400" v-model="deleteDialog">
      <v-card width="400" style="font-family: dana">
        <v-container>
          <v-row>
            <v-col>
              <h2 style="text-align: center">
                آیا از پاک کردن این لیسنینگ اطمینان دارید؟
              </h2>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-btn color="success" block style="font-family: dana; font-weight: bold; letter-spacing: 0"
                     @click="deleteListening">
                بله
              </v-btn>
            </v-col>
            <v-col>
              <v-btn color="error" block style="font-family: dana; font-weight: bold; letter-spacing: 0"
                     @click="deleteDialog = false">
                خیر
              </v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-dialog>
    <div class="text-center">
      <v-snackbar
          v-model="deleteSnackbar"
          :timeout="2000"
          :color="snackbarColor"
      >
        <v-btn
            color="#1C0153"
            text
            @click="deleteSnackbar = false"
        >
          بستن
        </v-btn>
        {{ snackbarMassage }}

      </v-snackbar>
    </div>
    <v-dialog width="600" v-model="transcriptDialog">
      <v-card width="600" style="font-size: 20px; padding: 20px">
        {{ transcript }}
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script>
import {mdiChevronRight, mdiChevronLeft, mdiBookEdit, mdiTrashCan, mdiPlusBox, mdiMagnify} from '@mdi/js'
import {mapGetters} from 'vuex'
import {GET_LISTENING_BASE_LIST, GO_TO_EDIT_LISTENING, DELETE_LISTENING} from "@/store/actions/listening";

export default {
  name: "ListeningBase",
  data() {
    return {
      width: 0,
      height: 0,
      page: 1,
      transcriptDialog: false,
      loading: true,
      searchText: '',
      transcript: '',
      deleteId: 0,
      deleteDialog: false,
      deleteSnackbar: false,
      snackbarColor: 'success',
      snackbarMassage: '',
      icons: {
        mdiChevronRight,
        mdiChevronLeft,
        mdiBookEdit,
        mdiTrashCan,
        mdiPlusBox,
        mdiMagnify
      }
    }
  },
  computed: {
    ...mapGetters(['listeningList']),
    rawList() {
      return this.listeningList.filter(listening => {
        return listening.title.toLowerCase().includes(this.searchText.toLowerCase()) || listening.id.toString() === this.searchText || listening.type.toLowerCase().includes(this.searchText.toLowerCase())
      }).sort((listening) => {
        return -listening.id
      })
    },
    paginatedList() {
      return this.rawList.slice(this.page === 1 ? 0 : (this.page - 1) * 5, this.page === 1 ? 5 : (this.page - 1) * 5 + 5)
    },
    readingNumberOfPages() {
      return Math.ceil(this.rawList.length / 5)
    },
  },
  created() {
    window.addEventListener('resize', this.handleResize);
    this.handleResize();
    this.$store.dispatch(GET_LISTENING_BASE_LIST).then(() => {
      this.loading = false
    })
    if (this.$route.params.success === 'true') {
      this.deleteSnackbar = true;
      this.snackbarMassage = 'لیسنینگ با موفقیت ویرایش شد';
      this.snackbarColor = 'success';
    }
  },
  methods: {
    handleResize() {
      this.width = window.innerWidth;
      this.height = window.innerHeight;
    },
    deleteDialogFunction(id) {
      this.deleteDialog = true;
      this.deleteId = id;
    },
    editReading(listening) {
      this.$store.dispatch(GO_TO_EDIT_LISTENING, listening);
      this.$router.push('/edit_listening');
    },
    deleteListening() {
      this.deleteDialog = false
      this.loading = true
      this.$store.dispatch(DELETE_LISTENING, this.deleteId).then(() => {
        this.$store.dispatch(GET_LISTENING_BASE_LIST).then(() => {
          this.loading = false
        })
        this.snackbarColor = "success"
        this.snackbarMassage = "لیسنینگ با موفقیت حذف گردید."
        this.deleteSnackbar = true
      }).catch(() => {
        this.loading = false
        this.snackbarColor = "error"
        this.snackbarMassage = "خطایی رخ داده است دوباره تلاش کنید."
        this.deleteSnackbar = true
      })
    },
    openPassage(transcript) {
      this.transcript = transcript
      this.transcriptDialog = true
    },
    goToQuestions(reading) {
      this.$store.dispatch(GO_TO_EDIT_LISTENING, reading)
      this.$router.push('/questions_listening')
    }
  }
}
</script>

<style scoped>

</style>