import {
    ADD_NEW_LISTENING,
    ADD_NEW_LISTENING_QUESTION,
    DELETE_LISTENING,
    DELETE_LISTENING_QUESTION,
    EDIT_LISTENING,
    GET_LISTENING_BASE_LIST,
    GET_LISTENING_QUESTIONS,
    GO_TO_EDIT_LISTENING
} from '../actions/listening'
import axios from 'axios'

const state = {
    listeningList: [],
    listeningSelected: {},
    questionsArray: [],
}
const getters = {
    listeningList: state => state.listeningList,
    listeningSelected: state => state.listeningSelected,
    listeningQuestionsArray: state => state.questionsArray,
}
const actions = {
    [GET_LISTENING_BASE_LIST]: ({commit}) => {
        axios.get('api/v1/institute/get_listening_list/').then((resp) => {
            commit('updateListeningList', resp.data)
        })
    },
    // eslint-disable-next-line no-unused-vars
    [ADD_NEW_LISTENING]: ({_}, payload) => {
        return axios({
            method: 'post',
            url: 'api/v1/institute/add_listening/',
            data: payload,
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
    },
    // eslint-disable-next-line no-unused-vars
    [DELETE_LISTENING]: ({_}, payload) => {
        return axios.post('api/v1/institute/delete_listening/', {'id': payload})
    },
    [GO_TO_EDIT_LISTENING]: ({commit}, payload) => {
        commit('updateSelectedListening', payload)
    },
    // eslint-disable-next-line no-unused-vars
    [EDIT_LISTENING]: ({_}, payload) => {
        return axios({
            method: 'post',
            url: 'api/v1/institute/edit_listening/',
            data: payload,
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
    },
    [GET_LISTENING_QUESTIONS]: ({state, commit}) => {
        return axios.get(`api/v1/institute/get_listening_questions?id=${state.listeningSelected.id}`).then((resp) => {
            commit('updateQuestionsArray', resp.data)
        })
    },
    // eslint-disable-next-line no-unused-vars
    [DELETE_LISTENING_QUESTION]: ({_}, payload) => {
        return axios.post('api/v1/institute/delete_listening_question/', {'id': payload})
    },

    // eslint-disable-next-line no-unused-vars
    [ADD_NEW_LISTENING_QUESTION]: ({_}, payload) => {
        return axios({
            method: 'post',
            url: 'api/v1/institute/add_listening_question/',
            data: payload,
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
    }
}
const mutations = {
    updateListeningList(state, payload) {
        state.listeningList = payload;
    },
    updateSelectedListening(state, payload) {
        state.listeningSelected = payload
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