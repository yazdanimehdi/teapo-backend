import {
    GET_READING_BASE_LIST,
    ADD_NEW_READING,
    DELETE_READING,
    GO_TO_EDIT_READING,
    EDIT_READING,
    GET_READING_QUESTIONS,
    DELETE_READING_QUESTION,
    ADD_NEW_READING_QUESTION
} from '../actions/reading'
import axios from 'axios'

const state = {
    readingsList: [],
    readingSelected: {},
    questionsArray: [],
}
const getters = {
    readingsList: state => state.readingsList,
    readingSelected: state => state.readingSelected,
    questionsArray: state => state.questionsArray,
}
const actions = {
    [GET_READING_BASE_LIST]: ({commit}) => {
        axios.get('api/v1/institute/get_reading_list/').then((resp) => {
            commit('updateReadingList', resp.data)
        })
    },
    // eslint-disable-next-line no-unused-vars
    [ADD_NEW_READING]: ({_}, payload) => {
        return axios.post('api/v1/institute/add_reading/', payload)
    },
    // eslint-disable-next-line no-unused-vars
    [DELETE_READING]: ({_}, payload) => {
        return axios.post('api/v1/institute/delete_reading/', {'id': payload})
    },
    [GO_TO_EDIT_READING]: ({commit}, payload) => {
        commit('updateSelectedReading', payload)
    },
    // eslint-disable-next-line no-unused-vars
    [EDIT_READING]: ({_}, payload) => {
        return axios.post('api/v1/institute/edit_reading/', payload)
    },
    [GET_READING_QUESTIONS]: ({state, commit}) => {
        return axios.get(`api/v1/institute/get_reading_questions?id=${state.readingSelected.id}`).then((resp) => {
            commit('updateQuestionsArray', resp.data)
        })
    },
    // eslint-disable-next-line no-unused-vars
    [DELETE_READING_QUESTION]: ({_}, payload) => {
        return axios.post('api/v1/institute/delete_reading_question/', {'id': payload})
    },

    // eslint-disable-next-line no-unused-vars
    [ADD_NEW_READING_QUESTION]: ({_}, payload) => {
        return axios.post('api/v1/institute/add_reading_question/', payload)
    }
}
const mutations = {
    updateReadingList(state, payload) {
        state.readingsList = payload;
    },
    updateSelectedReading(state, payload) {
        state.readingSelected = payload
    },
    updateQuestionsArray(state, payload) {
        state.questionsArray = payload
    }
}

export default {
    state,
    getters,
    actions,
    mutations
}