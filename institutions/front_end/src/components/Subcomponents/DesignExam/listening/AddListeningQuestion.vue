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
      <v-btn icon to="/questions_listening">
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
      <h1>New Listening</h1>
      <br/>
      <v-form v-model="valid">

        <v-slider
            v-model="questionNumber"
            :rules="[v => v!==0 || 'شماره‌ي سوال ضروری می‌باشد']"
            color="green"
            label="Question Number"
            persistent-hint
            hint="شماره‌ی سوال در ترتیب سوالات را انتخاب کنید"
            min="1"
            max="30"
            thumb-label
            style="margin-bottom: 20px"
        >
          <template v-slot:append>
            <v-text-field
                v-model="questionNumber"
                class="mt-0 pt-0"
                hide-details
                single-line
                type="number"
                style="width: 60px"
            ></v-text-field>
          </template>
        </v-slider>
        <v-text-field
            label="Question"
            v-model="question"
            outlined
            :rules="[v => !!v || 'متن سوال ضروری می‌باشد']"
            required
            :disabled="sending"
        >
        </v-text-field>

        <v-container
            class="px-0"
            fluid
        >
          <v-checkbox
              v-model="isQuoted"
              label="Is the Question Have Quote?"
              :on-icon="icons.mdiCheckboxMarkedCircleOutline"
              :off-icon="icons.mdiCheckboxBlankCircleOutline"
          ></v-checkbox>
        </v-container>

        <v-file-input
            label="Question Audio File"
            outlined
            @change="saveFileQuestion($event)"
            :rules="[v => !!v || 'بارگذاری فایل شنیداری سوال ضروری می‌باشد']"
            :prepend-icon="icons.mdiFile"
            :disabled="sending"
        ></v-file-input>
        <v-file-input
            label="Quote Audio File"
            outlined
            v-if="isQuoted"
            @change="saveFileQuote($event)"
            :rules="[v => !!v || 'بارگذاری فایل شینداری نقل قول ضروری می‌باشد']"
            :prepend-icon="icons.mdiFile"
            :disabled="sending"
        ></v-file-input>

        <v-container fluid>
          <v-row>
            <v-col>
              <h3>Answer Choices</h3>
              <h5>Choice (for adding new choices press + and for removing choices
                press -) if this choice is the correct answer please check the checkbox</h5>
            </v-col>
          </v-row>
          <v-row align="start" justify="start" v-for="choice in choices.length" :key="`c${choice}`">
            <v-text-field
                outlined
                :label="`Choice ${choice}`"
                v-model="choices[choice - 1]"
                :rules="[v => !!v || 'متن گزینه ضروری است']"
            >
              <template slot="prepend" v-if="choice !== 1 && choice !== 2">
                <v-btn icon style="padding-bottom: 10px" @click="removeAnswer(choice)">
                  <v-icon color="error">{{ icons.mdiMinusBox }}</v-icon>
                </v-btn>
              </template>


              <v-btn icon slot="append-outer" style="padding-bottom: 10px" @click="addCorrectAnswer(choice)">
                <v-icon :color="correctAnswers.indexOf(choice) !== -1 ? 'success': ''">{{
                    correctAnswers.indexOf(choice) !== -1 ? icons.mdiCheckboxMarkedCircleOutline : icons.mdiCheckboxBlankCircleOutline
                  }}
                </v-icon>
              </v-btn>

            </v-text-field>
          </v-row>
          <hr/>
          <v-btn icon large @click="addAnswer" :disabled="choices.length >= 6">
            <v-icon color="success">{{ icons.mdiPlusBox }}</v-icon>
          </v-btn>


        </v-container>

        <v-btn
            block
            shaped
            color="success"
            style="font-weight: bold; font-size: 20px; margin-bottom: 90px"
            @click="saveQuestion"
            :disabled="sending || !valid || correctAnswers.length === 0"
        >
          Save
        </v-btn>
      </v-form>
    </div>
    <v-dialog width="600" v-model="dialog" persistent>
      <v-card width="600" height="100" style="font-family: dana;">
        <h2 style="font-weight: bold; color: limegreen;  text-align: center; padding-top: 20px">سوال با موفقیت اضافه
          شد.</h2>
      </v-card>
      <v-btn color="success" style="font-family: dana; font-weight: bold; letter-spacing: 0" @click="resetAll">
        اضافه کردن سوال جدید
      </v-btn>
      <v-btn color="error" style="font-family: dana; font-weight: bold; letter-spacing: 0" to="/questions_listening">
        بازگشت به صفحه‌ی سوالات
      </v-btn>
    </v-dialog>
  </v-app>
</template>

<script>
import {
  mdiChevronRight, mdiChevronLeft, mdiFile, mdiPlusBox,
  mdiMinusBox,
  mdiCheckboxBlankCircleOutline,
  mdiCheckboxMarkedCircleOutline
} from '@mdi/js';
import {mapGetters} from 'vuex';
import {ADD_NEW_LISTENING_QUESTION} from "@/store/actions/listening";

export default {
  name: "AddListeningQuestion",
  data() {
    return {
      width: 0,
      height: 0,
      isQuoted: false,
      valid: false,
      question: '',
      questionNumber: '',
      correctAnswers: [],
      choices: ['', ''],
      questionFile: null,
      quoteFile: null,
      dialog: false,
      icons: {
        mdiChevronRight,
        mdiChevronLeft,
        mdiFile,
        mdiPlusBox,
        mdiMinusBox,
        mdiCheckboxBlankCircleOutline,
        mdiCheckboxMarkedCircleOutline
      },
      sending: false,
    }
  },
  created() {
    window.addEventListener('resize', this.handleResize);
    this.handleResize();
  },
  computed: {
    ...mapGetters(['listeningSelected'])
  },
  methods: {
    handleResize() {
      this.width = window.innerWidth;
      this.height = window.innerHeight;
    },
    saveQuestion() {
      this.sending = true
      let bodyFormData = new FormData();
      let rightAnswers = ''
      for (let i = 0; i < this.correctAnswers.length; i++) {
        rightAnswers = this.correctAnswers[i] + ' '
      }
      bodyFormData.set('listening_id', this.listeningSelected.id);
      bodyFormData.set('question', this.question);
      bodyFormData.set('number', this.questionNumber);
      bodyFormData.set('quote', this.isQuoted);
      bodyFormData.set('right_answer', rightAnswers);
      bodyFormData.set('answers', JSON.stringify(this.choices))

      bodyFormData.append('listening_question_audio_file', this.questionFile);
      if (this.isQuoted) {
        bodyFormData.append('quote_audio_file', this.quoteFile);
      }

      this.$store.dispatch(ADD_NEW_LISTENING_QUESTION, bodyFormData).then(() => {
        this.sending = false;
        this.dialog = true
      })
    },
    resetAll() {
      this.isQuoted = false;
      this.valid = false;
      this.question = '';
      this.questionNumber = '';
      this.correctAnswers = [];
      this.choices = ['', ''];
      this.questionFile = null;
      this.quoteFile = null;
      this.dialog = false;
      this.sending = false;
    },
    saveFileQuestion(event) {
      this.questionFile = event
    },
    saveFileQuote(event) {
      this.quoteFile = event
    },
    addCorrectAnswer(answer) {
      if (this.correctAnswers.indexOf(answer) === -1) {
        this.correctAnswers.push(answer)
      } else {
        this.correctAnswers.splice(this.correctAnswers.indexOf(answer), 1);
      }
    },
    removeAnswer(answer) {
      if (this.correctAnswers.indexOf(answer) !== -1) {
        this.correctAnswers.splice(this.correctAnswers.indexOf(answer), 1);
      }
      this.choices.splice(answer - 1, 1)
    },
    addAnswer() {
      this.choices.push('')
    }
  }
}
</script>

<style scoped>

</style>