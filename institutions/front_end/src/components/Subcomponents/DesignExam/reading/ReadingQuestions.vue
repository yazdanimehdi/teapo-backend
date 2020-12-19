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
      <v-btn icon to="/reading">
        <v-icon>{{ icons.mdiChevronRight }}</v-icon>
      </v-btn>
    </v-app-bar>
    <div v-if="loading" style="text-align: center; margin-top: 100px">
      <v-progress-circular indeterminate size="50"></v-progress-circular>
    </div>
    <div
        v-else
        :style="{'margin-left':`${width*0.06}px`, 'margin-right': `${width*0.06}px`, 'margin-top': `${height*0.1 + 30}px`}"
        style="font-family: kalam">

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
                   width="60" height="60" to="/add_reading_question">
              <v-icon color="success" large>{{ icons.mdiPlusBox }}</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-container>


      <v-card v-for="question in paginatedList" :key="question.id" style="margin-top: 10px">
        <v-container fluid>
          <v-row>
            <v-col cols="12" sm="8" md="6" lg="6" xl="6">
              <h2>{{ question.number }}. {{ question.question }}</h2>
              <h4 style="color: rgba(0, 0, 0, 0.5)">
                <div v-for="(answer, index) in question['answers']" :key="`t${index}`">{{ answer['code'] }}.
                  {{ answer['answer'] }}
                </div>
              </h4>
            </v-col>
            <v-col cols="12" sm="4" md="6" lg="6" xl="6" style="text-align: right">
              <v-btn icon
                     x-large @click="deleteDialogFunction(question.id)">
                <v-icon color="red">{{ icons.mdiTrashCan }}</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
      <div class="text-center" style="margin-top: 20px; margin-bottom: 90px">
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
                آیا از پاک کردن این سوال اطمینان دارید؟
              </h2>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-btn color="success" block style="font-family: dana; font-weight: bold; letter-spacing: 0"
                     @click="deleteQuestion">
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
  </v-app>
</template>

<script>
import {mdiChevronRight, mdiChevronLeft, mdiBookEdit, mdiTrashCan, mdiPlusBox, mdiMagnify} from '@mdi/js'
import {
  DELETE_READING_QUESTION,
  GET_READING_QUESTIONS
} from "@/store/actions/reading";
import {mapGetters} from 'vuex'

export default {
  name: "ReadingQuestions",
  data() {
    return {
      width: 0,
      height: 0,
      page: 1,
      passageDialog: false,
      loading: true,
      searchText: '',
      passage: '',
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
    ...mapGetters(['questionsArray']),
    rawList() {
      return this.questionsArray.filter(question => {
        return question.question.toLowerCase().includes(this.searchText.toLowerCase()) || question.number.toString() === this.searchText
      }).sort((question) => {
        return -question.number
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
    this.$store.dispatch(GET_READING_QUESTIONS).then(() => {
      this.loading = false
    })
    if (this.$route.params.success === 'true') {
      this.deleteSnackbar = true;
      this.snackbarMassage = 'متن با موفقیت ویرایش شد';
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
    deleteQuestion() {
      this.deleteDialog = false
      this.loading = true
      this.$store.dispatch(DELETE_READING_QUESTION, this.deleteId).then(() => {
        this.$store.dispatch(GET_READING_QUESTIONS).then(() => {
          this.loading = false
        })
        this.snackbarColor = "success"
        this.snackbarMassage = "سوال با موفقیت حذف گردید."
        this.deleteSnackbar = true
      }).catch(() => {
        this.loading = false
        this.snackbarColor = "error"
        this.snackbarMassage = "خطایی رخ داده است دوباره تلاش کنید."
        this.deleteSnackbar = true
      })
    },

  }
}
</script>

<style scoped>

</style>