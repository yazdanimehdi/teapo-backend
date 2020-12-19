<template>
  <v-app @click.native="appClick($event)">

    <div class="teapo_title" :style="{'height': `${height*0.08}px`,
         'width': `${mini? width*0.08 : width*0.230}px`,
          'max-width': '280px', 'position': 'fixed', 'z-index': '20'}">

      <div style="margin: 0" v-if="!mini">
        <div class="teapo_title_text">TEAPO</div>
        <div class="teapo_title_desc">Toefl Exam And Practice Online</div>
      </div>
      <div v-else>
        <div class="teapo_title_text_mini">TEAPO</div>
      </div>
    </div>
    <v-app-bar
        absolute
        color="#1C0153"
        dark
        :height="height*0.08"

        src="../assets/icon_group.png"
        style="padding: 0; margin: 0;position: fixed; z-index: 10"
    >
      <v-spacer></v-spacer>
      <div style="font-size: 18px; font-family: dana; font-weight: bold">{{ getName }}</div>
      <v-menu

      >
        <template v-slot:activator="{ on }">
          <v-btn icon text v-on="on">
            <v-icon>{{ icons.mdiChevronDown }}</v-icon>
          </v-btn>

        </template>

        <v-list>
          <v-list-item link>
            <v-list-item-icon :style="{'margin-right': '10px'}">
              <v-icon small>
                {{ icons.mdiAccountEdit }}
              </v-icon>
            </v-list-item-icon>
            <v-list-item-title class="menu_class">ویرایش حساب کاربری</v-list-item-title>
          </v-list-item>

          <v-list-item link @click="logout">
            <v-list-item-icon :style="{'margin-right': '10px'}">
              <v-icon small>
                {{ icons.mdiLogout }}
              </v-icon>
            </v-list-item-icon>
            <v-list-item-title class="menu_class">خروج</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

    </v-app-bar>
    <v-navigation-drawer
        right
        id="navdrawer_element"
        color="#E6E6E6"
        :expand-on-hover="false"
        :mini-variant.sync="mini"
        :permanent="true"
        absolute
        :width="width*0.23"
        :style="{'padding-top': `${height*0.1}px`, 'max-width': '280px', 'position': 'fixed'}"
        :mini-variant-width="width*0.08"
    >
      <div></div>
      <v-list
          nav
      >
        <v-list-item link @click="dashboardSelected">
          <v-list-item-icon :style="{'margin-right': '10px'}">
            <v-icon :color="linkSelected.dashboard ? '#A40000' : '#1C0153'" large>
              {{ icons.mdiViewDashboard }}
            </v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title class="drawer_links"
                               :style="{'color': `${linkSelected.dashboard ? '#A40000' : '#1C0153'}`}"
            >داشبورد
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item link @click="examDesignSelected">
          <v-list-item-icon :style="{'margin-right': '10px'}">
            <v-icon :color="linkSelected.examDesign ? '#A40000' : '#1C0153'" large>
              {{ icons.mdiLeadPencil }}
            </v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title class="drawer_links"
                               :style="{'color': `${linkSelected.examDesign ? '#A40000' : '#1C0153'}`}"
            >طراحی آزمون
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item link @click="mockSelected">
          <v-list-item-icon :style="{'margin-right': '10px'}">
            <v-icon :color="linkSelected.mockTest ? '#A40000' : '#1C0153'" large>
              {{ icons.mdiFormatListBulletedSquare }}
            </v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title class="drawer_links"
                               :style="{'color': `${linkSelected.mockTest ? '#A40000' : '#1C0153'}`}"
            >برگزاری ماک
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item link @click="TPOSelected">
          <v-list-item-icon :style="{'margin-right': '10px'}">
            <v-icon :color="linkSelected.TPO ? '#A40000' : '#1C0153'" large>
              {{ icons.mdiBookOpenPageVariant }}
            </v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title class="drawer_links"
                               :style="{'color': `${linkSelected.TPO ? '#A40000' : '#1C0153'}`}"
            >ساخت آزمون تمرینی
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>


        <v-list-item link @click="analyticsSelected">
          <v-list-item-icon :style="{'margin-right': '10px'}">
            <v-icon :color="linkSelected.analytics ? '#A40000' : '#1C0153'" large>
              {{ icons.mdiFinance }}
            </v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title class="drawer_links"
                               :style="{'color': `${linkSelected.analytics ? '#A40000' : '#1C0153'}`}"
            >گزارشات جامع
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>


        <v-list-item link @click="addCorrectorCorrectSelected">
          <v-list-item-icon :style="{'margin-right': '10px'}">
            <v-icon :color="linkSelected.addCorrector ? '#A40000' : '#1C0153'" large>
              {{ icons.mdiAccountPlus }}
            </v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title class="drawer_links"
                               :style="{'color': `${linkSelected.addCorrector ? '#A40000' : '#1C0153'}`}"
            >تعریف مصحح
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>

      </v-list>
    </v-navigation-drawer>
    <transition name="scroll-x-transition">
      <DesignExam :width="mini? width*0.91 - 50 : width*0.76 - 50" v-if="linkSelected.examDesign"
                  :style="{'margin-right': mini? `${width*0.08 + 10}px`:`${width*0.23 + 10}px`, 'margin-left': '50px', 'margin-top': `${height*0.08}px`}"
                  :height="height"/>
    </transition>
  </v-app>
</template>

<script>
import {
  mdiViewDashboard,
  mdiBookOpenPageVariant,
  mdiLeadPencil,
  mdiChevronDown,
  mdiLogout,
  mdiAccountEdit,
  mdiFormatListBulletedSquare,
  mdiAccountPlus,
  mdiFinance

} from '@mdi/js'
import {CHANGE_TAB} from "@/store/actions/dashboard";
import DesignExam from "@/components/Main/DesignExam";
import {mapGetters} from 'vuex'
import {AUTH_LOGOUT} from "@/store/actions/auth";

export default {
  name: "Dashboard",
  components: {DesignExam},
  data() {
    return {
      mini: false,
      icons: {
        mdiViewDashboard,
        mdiBookOpenPageVariant,
        mdiLeadPencil,
        mdiChevronDown,
        mdiLogout,
        mdiAccountEdit,
        mdiFormatListBulletedSquare,
        mdiAccountPlus,
        mdiFinance
      },
      titleHeight: 56,
      navWidth: 180,
      width: 0,
      height: 0,
      linkSelected: {
        dashboard: true,
        TPO: false,
        mockTest: false,
        analytics: false,
        addCorrector: false,
        examDesign: false
      }
    }
  },
  computed:{
    ...mapGetters(['tabNumber', 'getName'])
  },
  created() {
    window.addEventListener('resize', this.handleResize);
    this.handleResize();
    switch (this.tabNumber) {
      case 0:
        this.dashboardSelected();
        break;
      case 1:
        this.TPOSelected();
        break;
      case 2:
        this.mockSelected();
        break;
      case 3:
        this.analyticsSelected();
        break;
      case 4:
        this.addCorrectorCorrectSelected();
        break;
      case 5:
        this.examDesignSelected();
        break;
    }
  },
  destroyed() {
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    dashboardSelected() {
      this.$store.dispatch(CHANGE_TAB, 0);
      this.linkSelected.dashboard = true;
      this.linkSelected.TPO = false;
      this.linkSelected.mockTest = false;
      this.linkSelected.analytics = false;
      this.linkSelected.examDesign = false;
      this.linkSelected.addCorrector = false;
    },
    TPOSelected() {
      this.$store.dispatch(CHANGE_TAB, 1);
      this.linkSelected.dashboard = false;
      this.linkSelected.TPO = true;
      this.linkSelected.mockTest = false;
      this.linkSelected.analytics = false;
      this.linkSelected.examDesign = false;
      this.linkSelected.addCorrector = false;
    },

    mockSelected() {
      this.$store.dispatch(CHANGE_TAB, 2);
      this.linkSelected.dashboard = false;
      this.linkSelected.TPO = false;
      this.linkSelected.mockTest = true;
      this.linkSelected.analytics = false;
      this.linkSelected.examDesign = false;
      this.linkSelected.addCorrector = false;
    },
    analyticsSelected() {
      this.$store.dispatch(CHANGE_TAB, 3);
      this.linkSelected.dashboard = false;
      this.linkSelected.TPO = false;
      this.linkSelected.mockTest = false;
      this.linkSelected.analytics = true;
      this.linkSelected.examDesign = false;
      this.linkSelected.addCorrector = false;
    },
    addCorrectorCorrectSelected() {
      this.$store.dispatch(CHANGE_TAB, 4);
      this.linkSelected.dashboard = false;
      this.linkSelected.TPO = false;
      this.linkSelected.mockTest = false;
      this.linkSelected.analytics = false;
      this.linkSelected.examDesign = false;
      this.linkSelected.addCorrector = true
    },
    examDesignSelected() {
      this.$store.dispatch(CHANGE_TAB, 5);
      this.linkSelected.dashboard = false;
      this.linkSelected.TPO = false;
      this.linkSelected.mockTest = false;
      this.linkSelected.analytics = false;
      this.linkSelected.examDesign = true;
      this.linkSelected.addCorrector = false
    },

    handleResize() {
      this.width = window.innerWidth;
      this.height = window.innerHeight;
    },
    appClick(event) {
      let myElementToCheckIfClicksAreInsideOf = document.querySelector('#navdrawer_element');
      if (myElementToCheckIfClicksAreInsideOf !== null) {
        if (!myElementToCheckIfClicksAreInsideOf.contains(event.target)) {
          this.mini = true;
        }
      }
    },
    logout(){
      this.$store.dispatch(AUTH_LOGOUT)
    }
  }
}
</script>

<style scoped>
@import "../assets/fonts.css";

.teapo_title {
  background-color: #a9a1ba;
  margin: 0;
  padding: 0;
  position: relative;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: kalam;
}

.teapo_title_text {
  color: #1C0153;
  font-weight: bold;
  text-align: center;
  font-size: 22px;
  font-family: kalam;
}

.teapo_title_text_mini {
  color: #1C0153;
  font-weight: bold;
  text-align: center;
  font-size: 20px;
  margin-top: 5px;
  font-family: kalam;
}

.teapo_title_desc {
  color: #1C0153;
  font-size: 12px;
  text-align: center;
  font-family: kalam;
}

.drawer_links {
  font-size: 22px;
  font-family: dana;
  font-weight: bold;
}

.menu_class {
  font-size: 14px;
  font-family: dana;
  font-weight: bold;
}

</style>