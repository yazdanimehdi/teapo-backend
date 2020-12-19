<template>
  <div :style="{'font-family':'kalam', 'padding-top': `${height*0.06}px`}">
    <v-container fluid>
      <v-row>
        <v-col cols="12" sm="6" md="6" lg="3" xl="3">
          <v-card
              class="mx-auto"
              height="400"
          >
            <v-img
                src="@/assets/img/reading_toefl.jpg"
                height="200px"
            ></v-img>

            <v-card-title>
              Reading
            </v-card-title>

            <v-card-subtitle style="font-family: dana; height: 40px">
              اضافه کنید Reading در این قسمت شما می‌توانید

            </v-card-subtitle>

            <v-card-actions style="margin-top: 20px">
              <v-btn
                  color="orange lighten-2"
                  to="/reading"
              >
                Reading
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>

        <v-col cols="12" sm="6" md="6" lg="3" xl="3">
          <v-card
              class="mx-auto"
              height="400"
          >
            <v-img
                src="@/assets/img/listening_toefl.jpeg"
                height="200px"
            ></v-img>

            <v-card-title>
              Listening
            </v-card-title>

            <v-card-subtitle style="font-family: dana; height: 40px" >
              اضافه کنید Listening در این قسمت شما می‌توانید

            </v-card-subtitle>

            <v-card-actions style="margin-top: 20px">
              <v-btn
                  color="orange lighten-2"
                  to="/listening"
              >
                Listening
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>

        <v-col cols="12" sm="6" md="6" lg="3" xl="3">
          <v-card
              class="mx-auto"
              height="400"
          >
            <v-img
                src="@/assets/img/speaking_toefl.jpg"
                height="200px"
            ></v-img>

            <v-card-title>
              Speaking
            </v-card-title>

            <v-card-subtitle style="font-family: dana; height: 40px">
              اضافه کنید Speaking در این قسمت شما می‌توانید

            </v-card-subtitle>

            <v-card-actions style="margin-top: 20px">
              <v-btn
                  color="orange lighten-2"

              >
                Speaking
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>

        <v-col cols="12" sm="6" md="6" lg="3" xl="3">
          <v-card
              class="mx-auto"
              height="400"
          >
            <v-img
                src="@/assets/img/writing_toefl.jpg"
                height="200px"
            ></v-img>

            <v-card-title>
              Writing
            </v-card-title>

            <v-card-subtitle style="font-family: dana; height: 40px">
              اضافه کنید Writing در این قسمت شما می‌توانید

            </v-card-subtitle>

            <v-card-actions style="margin-top: 20px">
              <v-btn
                  color="orange lighten-2"

              >
                Writing
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>

      </v-row>
    </v-container>
  </div>
</template>

<script>
import {mdiChevronDown, mdiChevronUp} from '@mdi/js'

export default {
  name: "DesignExam",
  props: {
    width: {
      required: true,
      type: Number
    },
    height: {
      required: true,
      type: Number
    }
  },
  data() {
    return {
      icons: {
        mdiChevronDown,
        mdiChevronUp
      }
    }
  },
  methods:{
  }
}
</script>

<style scoped>


</style>