import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'
import api from '../../services/api'

export const fetchInteractions = createAsyncThunk('interactions/fetch', async () => {
  const { data } = await api.get('/interactions')
  return data
})

export const createInteraction = createAsyncThunk('interactions/create', async (payload) => {
  const { data } = await api.post('/interactions', payload)
  return data
})

const interactionSlice = createSlice({
  name: 'interactions',
  initialState: {
    items: [],
    loading: false,
    error: null
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchInteractions.pending, (state) => {
        state.loading = true
      })
      .addCase(fetchInteractions.fulfilled, (state, action) => {
        state.loading = false
        state.items = action.payload
      })
      .addCase(fetchInteractions.rejected, (state, action) => {
        state.loading = false
        state.error = action.error.message
      })
      .addCase(createInteraction.fulfilled, (state, action) => {
        state.items.unshift(action.payload)
      })
  }
})

export default interactionSlice.reducer
