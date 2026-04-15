<template>
  <div class="flex flex-col h-full bg-darkBg text-slate-100">
    <div class="flex items-center justify-between p-4 border-b border-darkCard">
      <div>
        <h2 class="text-xl font-bold font-sans">Platform Inbox</h2>
        <p class="text-xs text-slate-400">Review Expert Insights & Manuals</p>
      </div>
      <!-- Mock Role Switcher for Demo -->
      <span class="bg-indigo-900 text-indigo-300 text-xs px-2 py-1 rounded border border-indigo-700 font-mono">Role: EXPERT</span>
    </div>

    <!-- Tab Navigation -->
    <div class="flex px-4 pt-4 gap-2 text-sm border-b border-darkCard">
      <button 
        class="pb-2 px-1 font-medium transition-colors"
        :class="activeTab === 'chat' ? 'text-blue-400 border-b-2 border-blue-400' : 'text-slate-500 hover:text-slate-300'"
        @click="activeTab = 'chat'">Knowledge Chat</button>
      <button 
        class="pb-2 px-1 font-medium transition-colors"
        :class="activeTab === 'videos' ? 'text-blue-400 border-b-2 border-blue-400' : 'text-slate-500 hover:text-slate-300'"
        @click="activeTab = 'videos'">Expert Summaries</button>
    </div>

    <!-- Active Content Area -->
    <div class="flex-1 overflow-hidden relative">
      
      <!-- Expert Summaries Tab -->
      <div v-if="activeTab === 'videos'" class="p-4 space-y-4">
        
        <div v-if="expertVideos.length === 0" class="text-center text-slate-500 py-10">
          No expert sessions recorded yet. Go to the Simulator to record one!
        </div>

        <div v-for="video in expertVideos" :key="video.id" class="bg-darkCard rounded-xl overflow-hidden border border-slate-700 hover:border-slate-600 transition-colors cursor-pointer group">
          <div class="h-32 bg-black relative flex items-center justify-center overflow-hidden">
            <img v-if="video.thumbnail" :src="'data:image/jpeg;base64,' + video.thumbnail" class="absolute inset-0 w-full h-full object-cover opacity-70 group-hover:opacity-100 transition-opacity" />
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 text-slate-300 group-hover:text-white transition-colors opacity-80" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd" />
            </svg>
            <div class="absolute bottom-2 left-2 text-xs font-bold text-white bg-black bg-opacity-50 px-2 py-0.5 rounded">
              Infiniti FX45 (Engine)
            </div>
          </div>
          <div class="p-4">
            <h3 class="font-semibold text-blue-400 mb-1 leading-tight">{{ video.title }}</h3>
            <p class="text-xs text-slate-400 mb-3 line-clamp-2">
              "{{ video.summary }}"
            </p>
            <div class="flex gap-2 flex-wrap">
              <span v-for="tool in video.tools" :key="tool" class="text-[10px] uppercase font-bold tracking-wider px-2 py-1 bg-slate-800 text-slate-300 rounded">
                {{ tool }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Chat View -->
      <div v-if="activeTab === 'chat'" class="flex flex-col h-full">
        <!-- Chat History -->
        <div class="flex-1 overflow-y-auto p-4 space-y-4">
          <div v-for="msg in messages" :key="msg.id" class="flex gap-3" :class="msg.type === 'user' ? 'flex-row-reverse' : ''">
            
            <div v-if="msg.type === 'system'" class="w-8 h-8 rounded bg-gradient-to-tr from-blue-500 to-indigo-500 flex items-center justify-center flex-shrink-0 shadow-md">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm-2-9a2 2 0 114 0 2 2 0 01-4 0z" clip-rule="evenodd" />
              </svg>
            </div>
            
            <div class="px-3 py-2 rounded-lg text-sm max-w-[85%] border overflow-hidden" 
                 :class="msg.type === 'user' ? 'bg-primary text-white border-blue-600 rounded-tr-none' : 'bg-darkCard text-slate-200 border-slate-700 rounded-tl-none markdown-body'"
                 v-html="msg.type === 'user' ? escapeHtml(msg.text) : renderMarkdown(msg.text)">
            </div>
          </div>
          
          <!-- Dynamic Loading Indicator -->
          <div v-if="isProcessing" class="flex gap-3">
            <div class="w-8 h-8 rounded bg-gradient-to-tr from-blue-500 to-indigo-500 flex items-center justify-center flex-shrink-0 shadow-md">
              <svg class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            </div>
            <div class="px-3 py-2 rounded-lg text-sm bg-darkCard text-slate-400 border border-slate-700 rounded-tl-none flex items-center italic">
              {{ currentStatusMessage }}
            </div>
          </div>
        </div>

        <!-- Chat Input Form -->
        <div class="p-3 border-t border-darkCard bg-darkBg">
          <form @submit.prevent="sendMessage" class="relative flex items-center">
            <input 
              v-model="newUserMessage"
              type="text" 
              placeholder="Ask a technical question..." 
              class="w-full bg-darkCard border border-slate-700 rounded-full py-2.5 pl-4 pr-12 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent placeholder-slate-500 text-slate-200 transition-shadow"
            />
            <button type="submit" :disabled="!newUserMessage" class="absolute right-2 p-1.5 bg-blue-600 hover:bg-blue-500 rounded-full text-white transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-white disabled:opacity-50">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transform rotate-90" viewBox="0 0 20 20" fill="currentColor">
                <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
              </svg>
            </button>
          </form>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { marked } from 'marked'

const activeTab = ref('chat')
const newUserMessage = ref('')
const isProcessing = ref(false)
const currentStatusMessage = ref('')
const expertVideos = ref([])

const statusStages = [
  "Searching Vector Database...",
  "Retrieving manual context...",
  "Running Qwen-VL Inference...",
  "Structuring format..."
]

const messages = ref([
  { id: 1, type: 'system', text: 'Welcome. I am connected to the Vector Database. I can answer questions from the uploaded Infiniti FX45 manuals and expert video transcripts. How can I help?' }
])

const escapeHtml = (text) => text.replace(/</g, "&lt;").replace(/>/g, "&gt;")
const renderMarkdown = (text) => {
  return marked.parse(text)
}

const loadVideos = async () => {
  try {
    const res = await fetch("/api/videos")
    const data = await res.json()
    expertVideos.value = data.videos || []
  } catch(e) {
    console.error("Failed to fetch videos.")
  }
}

// Reload videos whenever the tab is swapped
const switchTab = (tab) => {
  activeTab.value = tab
  if (tab === 'videos') {
    loadVideos()
  }
}

onMounted(() => {
  loadVideos()
})


const sendMessage = async () => {
  if (!newUserMessage.value.trim()) return
  
  messages.value.push({ id: Date.now(), type: 'user', text: newUserMessage.value })
  const query = newUserMessage.value
  newUserMessage.value = ''
  
  isProcessing.value = true
  let stageIdx = 0
  currentStatusMessage.value = statusStages[0]
  
  const statusInterval = setInterval(() => {
    stageIdx = (stageIdx + 1) % statusStages.length
    currentStatusMessage.value = statusStages[stageIdx]
  }, 1500)
  
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: query, role: "EXPERT" })
    })
    const data = await res.json()
    clearInterval(statusInterval)
    messages.value.push({ id: Date.now(), type: 'system', text: data.answer })
  } catch (err) {
    clearInterval(statusInterval)
    messages.value.push({ id: Date.now(), type: 'system', text: "**Error connecting to AI Backend.** Ensure the FastAPI server is running." })
  } finally {
    isProcessing.value = false
  }
}
</script>
