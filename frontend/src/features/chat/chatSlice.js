import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'
import api from '../../services/api'

export const sendMessage = createAsyncThunk('chat/send', async (message) => {
  const { data } = await api.post('/agent/chat', { message })
  return { user: message, bot: data.response }
})

const chatSlice = createSlice({
  name: 'chat',
  initialState: {
    messages: [],
    loading: false
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(sendMessage.pending, (state, action) => {
        state.loading = true
        state.messages.push({ role: 'user', content: action.meta.arg })
      })
      .addCase(sendMessage.fulfilled, (state, action) => {
        state.loading = false
        state.messages.push({ role: 'assistant', content: action.payload.bot })
      })
      .addCase(sendMessage.rejected, (state) => {
        state.loading = false
        state.messages.push({ role: 'assistant', content: 'Unable to process request right now.' })
      })
  }
})

export default chatSlice.reducer
