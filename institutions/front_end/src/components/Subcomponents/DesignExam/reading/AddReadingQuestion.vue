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
      <v-btn icon to="/questions_reading">
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
        style="font-family: kalam; margin-bottom: 50px">
      <link rel="stylesheet"
            href="https://use.fontawesome.com/releases/v5.2.0/css/all.css"
            integrity="sha384-hWVjflwFxL6sNzntih27bfxkr27PmbbK/iSvJ+a4+0owXq79v+lsFkW54bOGbiDQ"
            crossorigin="anonymous">
      <h1>New Question</h1>
      <br/>
      <v-container fluid>
        <v-row justify="start" align="start">
          <v-col cols="12" sm="12" md="6" lg="6" xl="6">
            <v-form v-model="valid">
              <v-select
                  v-model="questionType"
                  :items="['Fact', 'Insertion', 'Summary']"
                  outlined
                  label="Question Type"
              ></v-select>

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

              <v-slider
                  v-model="paragraphNumber"
                  v-if="questionType !== 'Summary'"
                  :rules="[v => v!==0 || 'شماره‌ي پاراگراف مربوطه ضروری می‌باشد']"
                  color="green"
                  label="Paragraph Number"
                  persistent-hint
                  hint="شماره‌ی پاراگراف مربوطه را انتخاب کنید"
                  min="1"
                  :max="maxParagraphNumber"
                  thumb-label
                  style="margin-bottom: 20px"
              >
                <template v-slot:append>
                  <v-text-field
                      v-model="paragraphNumber"
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

              <v-text-field
                  v-if="questionType==='Insertion'"
                  label="Insertion Sentence"
                  v-model="insertionSentence"
                  outlined
                  required
                  :rules="[v => !!v || 'جمله‌ی اضافه کردن این سوال ضروری می‌باشد']"
                  :disabled="sending"
              >
              </v-text-field>
              <v-container fluid style="padding: 0; margin: 0" v-if="questionType==='Normal'">
                <v-row style="padding: 0; margin: 0">
                  <v-col cols="6" sm="6" md="6" lg="6" xl="6" style="padding: 0; margin: 0">
                    <v-text-field
                        label="Highlighted Word"
                        v-model="highlightedWord"
                        outlined
                        disabled
                    >
                    </v-text-field>
                  </v-col>
                  <v-col cols="6" sm="6" md="6" lg="6" xl="6">
                    <v-btn color="yellow" @click="highlightWord">Highlight</v-btn>
                    <v-btn color="success" @click="resetHighlight" style="margin-left: 10px">Reset</v-btn>
                  </v-col>
                </v-row>

              </v-container>
              <v-btn v-if="questionType==='Insertion'" color="blue" block
                     style="color: white; font-weight: bold; margin-bottom: 16px"
                     @click="insertionDialog = true">
                Add Insertion Answers
              </v-btn>

              <v-container fluid v-if="questionType !== 'Insertion'">
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

              <v-btn color="success" block style="font-weight: bold; margin-bottom: 16px"
                     :disabled="(questionType === 'Insertion' && !questionPassage.includes('[]')) || !valid"
                     @click="saveQuestion"
              >Save
              </v-btn>

            </v-form>
          </v-col>
          <v-col cols="12" sm="12" md="6" lg="6" xl="6">
            <div v-html="questionPassage" id="passage"></div>
          </v-col>
        </v-row>
      </v-container>

    </div>
    <v-dialog width="600" v-model="dialog" persistent>
      <v-card width="600" height="100" style="font-family: dana;">
        <h2 style="font-weight: bold; color: limegreen;  text-align: center; padding-top: 20px">سوال با موفقیت اضافه
          شد.</h2>
      </v-card>
      <v-btn color="success" style="font-family: dana; font-weight: bold; letter-spacing: 0" @click="resetAll">
        اضافه کردن سوال جدید
      </v-btn>
      <v-btn color="error" style="font-family: dana; font-weight: bold; letter-spacing: 0" to="/questions_reading">
        بازگشت به سوالات متن‌ها
      </v-btn>
    </v-dialog>
    <v-dialog v-model="insertionDialog" width="600">
      <v-card width="600" style="font-family: Kalam; padding: 40px">
        <span v-for="(item, index) in lettersList" :key="index">
          <v-btn icon x-small @click="addRemoveInsertionSentence(item[1])">
          <v-icon v-if="insertionArray.indexOf(item[1]) !== -1" small color="error">{{ icons.mdiCommentMinus }}</v-icon>
          <v-icon v-else small color="success">{{ icons.mdiCommentPlus }}</v-icon>
        </v-btn> {{ item[0] }} </span>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script>
import {
  mdiChevronRight,
  mdiChevronLeft,
  mdiCommentPlus,
  mdiCommentMinus,
  mdiPlusBox,
  mdiMinusBox,
  mdiCheckboxBlankCircleOutline,
  mdiCheckboxMarkedCircleOutline
} from '@mdi/js'
import {ADD_NEW_READING_QUESTION} from "@/store/actions/reading";
import {mapGetters} from 'vuex'

export default {
  name: "AddReadingQuestion",
  data() {
    return {
      width: 0,
      height: 0,
      page: 1,
      questionNumber: 1,
      paragraphNumber: 1,
      highlightedWord: '',
      insertionDialog: false,
      correctAnswers: [],
      choices: ['', ''],
      originalLetterArray: [],
      insertionArray: [],
      valid: false,
      questionType: 'Fact',
      question: '',
      insertionSentence: '',
      dialog: false,
      questionPassage: '',
      icons: {
        mdiCheckboxBlankCircleOutline,
        mdiCheckboxMarkedCircleOutline,
        mdiCommentMinus,
        mdiCommentPlus,
        mdiChevronRight,
        mdiChevronLeft,
        mdiPlusBox,
        mdiMinusBox
      },
      sending: false,
    }
  },
  computed: {
    ...mapGetters(['readingSelected']),
    maxParagraphNumber() {
      let passage = this.readingSelected.passage
      return passage.match(/<\/p>/g).length
    },
    lettersList() {
      let letters = [];
      for (let i = 0; i < this.originalLetterArray.length; i++) {
        if (!(this.originalLetterArray[i].includes('<') || this.originalLetterArray[i].includes('>') || this.originalLetterArray[i].includes('class="fas') || this.originalLetterArray[i].includes('id="insert') || this.originalLetterArray[i].match(/\s+/g) !== null || this.originalLetterArray[i] === '')) {
          letters.push([this.originalLetterArray[i], i])
        }
      }
      return letters
    },
  },
  created() {
    window.addEventListener('resize', this.handleResize);
    this.handleResize();
    this.questionPassage = this.readingSelected.passage.replaceAll('<pr', '<p').substr(0, 10) + '<i class="fas fa-arrow-right"></i> ' + this.readingSelected.passage.replaceAll('<pr', '<p').substr(10, this.readingSelected.passage.length - 10)
    this.originalLetterArray = this.questionPassage.split(' ')
  },
  watch: {
    paragraphNumber(newVal) {
      let passage = this.questionPassage
      passage = passage.replaceAll(/<i class="fas fa-arrow-right"><\/i>/g, '')
      let paragraphs = passage.split('</p>')
      paragraphs.pop()
      let newPassage = ''
      for (let i = 0; i < paragraphs.length; i++) {
        if (i + 1 === newVal) {
          newPassage = newPassage + paragraphs[i].substr(0, 10) + '<i class="fas fa-arrow-right"></i> ' + paragraphs[i].substr(10, paragraphs[i].length - 10) + '</p>'
        } else {
          newPassage = newPassage + paragraphs[i] + '</p>'
        }

      }
      this.questionPassage = newPassage
    },
    insertionArray(newVal) {
      let newPassage = ''
      let j = 1;
      for (let i = 0; i < this.originalLetterArray.length; i++) {
        if (newVal.includes(i)) {
          j++;
          newPassage = newPassage + ' ' + `<a id="insert${j}" class="insert">[]</a>` + ' ' + this.originalLetterArray[i]
        } else {
          if (i === 0) {
            newPassage = this.originalLetterArray[i] + ' '
          } else {
            newPassage = newPassage + ' ' + this.originalLetterArray[i] + ' '
          }
        }
      }
      this.questionPassage = newPassage
    }

  },
  methods: {
    handleResize() {
      this.width = window.innerWidth;
      this.height = window.innerHeight;
    },
    saveQuestion() {
      this.sending = true
      let rightAnswers = ''
      for (let i = 0; i < this.correctAnswers.length; i++) {
        rightAnswers = this.correctAnswers[i] + ' '
      }
      let payload = {
        'reading_id': this.readingSelected.id,
        'question': this.question,
        'question_type': this.questionType,
        'number': this.questionNumber,
        'related_paragraph': this.paragraphNumber,
        'related_passage': this.questionPassage,
        'right_answer': rightAnswers,
        'insertion_sentence': this.insertionSentence,
        'answers': this.choices,
      }
      this.$store.dispatch(ADD_NEW_READING_QUESTION, payload).then(() => {
        this.sending = false;
        this.dialog = true
      })
    },
    resetAll() {
      this.page = 1;
      this.sending = false;
      this.questionNumber = 1;
      this.paragraphNumber = 1;
      this.highlightedWord = '';
      this.insertionDialog = false;
      this.correctAnswers = [];
      this.choices = ['', ''];
      this.originalLetterArray = [];
      this.insertionArray = [];
      this.valid = false;
      this.questionType = 'Fact';
      this.question = '';
      this.insertionSentence = '';
      this.dialog = false;
      this.questionPassage = this.readingSelected.passage.replaceAll('<pr', '<p').substr(0, 10) + '<i class="fas fa-arrow-right"></i> ' + this.readingSelected.passage.replaceAll('<pr', '<p').substr(10, this.readingSelected.passage.length - 10)
      this.originalLetterArray = this.questionPassage.split(' ')
    },
    highlightWord() {
      let selectedText = '';
      // window.getSelection
      if (window.getSelection) {
        selectedText = window.getSelection();
      }
      // document.getSelection
      else if (document.getSelection) {
        selectedText = document.getSelection();
      }
      // document.selection
      else if (document.selection) {
        selectedText = document.selection.createRange().text;
      }
      let range = window.getSelection().getRangeAt(0),
          mark = document.createElement('mark');

      mark.appendChild(range.extractContents());
      range.insertNode(mark);
      this.questionPassage = document.getElementById('passage').innerHTML
      this.highlightedWord = selectedText.toString();
    },
    resetHighlight() {
      this.questionPassage = this.questionPassage.replaceAll(/<mark>/g, '')
      this.questionPassage = this.questionPassage.replaceAll(/<\/mark>/g, '')
      this.highlightedWord = ''
      document.getElementById('passage').innerHTML = this.questionPassage
    },
    addRemoveInsertionSentence(number) {
      if (this.insertionArray.indexOf(number) === -1) {
        this.insertionArray.push(number)
      } else {
        this.insertionArray.splice(this.insertionArray.indexOf(number), 1);
      }
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