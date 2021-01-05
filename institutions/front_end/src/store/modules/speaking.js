import {
    DELETE_SPEAKING,
    GET_SPEAKING_BASE_LIST,
} from '../actions/speaking'


import axios from 'axios'

const state = {
    speakingsList: [],
    speakingSelected: {},
}
const getters = {
    speakingsList: state => state.speakingsList,
    speakingSelected: state => state.speakingSelected,
}
const actions = {
    [GET_SPEAKING_BASE_LIST]: ({commit}) => {
        axios.get('api/v1/institute/get_speaking_list/').then((resp) => {
            commit('updateSpeakingList', resp.data)
        })
    },
    // eslint-disable-next-line no-unused-vars
    [DELETE_SPEAKING]: ({_}, payload) => {
        return axios.post('api/v1/institute/delete_speaking/', {'id': payload})
    },
}

const mutations = {
    updateSpeakingList(state, payload) {
        state.speakingsList = payload;
    },
}

export default {
    state,
    getters,
    actions,
    mutations
}
