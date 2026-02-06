import { configureStore } from '@reduxjs/toolkit'
import chatReducer from '../features/chat/chatSlice'
import interactionReducer from '../features/interactions/interactionSlice'

export const store = configureStore({
  reducer: {
    interactions: interactionReducer,
    chat: chatReducer
  }
})
