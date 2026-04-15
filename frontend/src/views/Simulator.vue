<template>
  <div class="flex flex-col gap-6">
    <div class="bg-darkCard rounded-xl p-5 shadow-lg border border-slate-800">
      <h2 class="text-lg font-semibold mb-2 flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-indigo-400" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
        </svg>
        Live AR Vision
      </h2>
      <p class="text-sm text-slate-400 mb-4">
        Simulates the view from the AR glasses. (Live camera requires HTTPS/Ngrok on mobile).
      </p>

      <div class="relative w-full aspect-video bg-black rounded-lg overflow-hidden flex items-center justify-center mb-4 group border border-slate-700 shadow-inner">
        <!-- Live Video feed will go here -->
        <video ref="videoElement" class="absolute inset-0 w-full h-full object-cover" autoplay playsinline muted></video>
        <canvas ref="canvasElement" class="hidden"></canvas>
        <div v-if="!isCameraOn" class="text-slate-500 flex flex-col items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 mb-2 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
          <span>Camera Offline</span>
        </div>
        
        <!-- UI overlay for snapshot indicator -->
        <div v-if="isCameraOn" class="absolute top-2 right-2 bg-black bg-opacity-60 px-2 py-1 rounded text-xs text-green-400 font-mono flex items-center">
          <span class="w-2 h-2 rounded-full bg-green-500 mr-2 animate-pulse"></span>
          Capturing
        </div>
      </div>

      <button @click="toggleCamera" class="w-full py-3 rounded-lg font-medium transition-all shadow-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-darkBg flex items-center justify-center" :class="isCameraOn ? 'bg-red-500/10 text-red-500 border border-red-500/50 hover:bg-red-500/20' : 'bg-primary text-white hover:bg-blue-600 focus:ring-blue-500'">
        <svg v-if="!isCameraOn" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.121 17.804A13.937 13.937 0 0112 16c2.5 0 4.847.655 6.879 1.804M15 10a3 3 0 11-6 0 3 3 0 016 0zm6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        {{ isCameraOn ? 'Stop AR Feed' : 'Start Camera Feed' }}
      </button>
    </div>

    <!-- Voice Command Section -->
    <div class="bg-darkCard rounded-xl p-5 shadow-lg border border-slate-800">
      <h2 class="text-lg font-semibold mb-2 flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
        </svg>
        Voice Command
      </h2>
      <p class="text-sm text-slate-400 mb-4">
        Hold to ask the assistant a question. (We are using your browser's native Speech Recognition for the hackathon MVP!)
      </p>

      <div class="flex items-center justify-center py-4">
        <button 
          @pointerdown.prevent="startRecording" 
          @pointerup.prevent="stopRecording"
          @pointerleave="stopRecording"
          @pointercancel="stopRecording"
          class="w-24 h-24 rounded-full flex items-center justify-center transition-transform shadow-[0_0_20px_rgba(34,197,94,0.3)] focus:outline-none"
          style="-webkit-user-select: none; user-select: none; -webkit-touch-callout: none;"
          :class="isRecording ? 'bg-red-500 scale-95 shadow-[0_0_30px_rgba(239,68,68,0.6)]' : 'bg-darkBg border-2 border-green-500 text-green-400 hover:scale-105'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10" fill="none" viewBox="0 0 24 24" stroke="currentColor" :class="isRecording ? 'text-white' : ''">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
          </svg>
        </button>
      </div>
      
      <div class="text-center text-sm font-medium mb-4" :class="isRecording ? 'text-red-400 animate-pulse' : 'text-slate-500'">
        {{ isRecording ? 'Listening (Speak now, release to send)...' : 'Hold to speak' }}
      </div>

      <!-- AR Glasses Overlay Output -->
      <div v-if="transcript || aiResponse || isProcessing" class="mt-4 border-t border-slate-700 pt-4">
        <div class="mb-3">
          <span class="text-xs text-slate-500 uppercase font-bold tracking-wider">You Said:</span>
          <p class="text-white italic text-sm mt-1">"{{ transcript }}"</p>
        </div>
        
        <div>
          <span class="text-xs text-blue-400 uppercase font-bold tracking-wider">AI Assistant:</span>
          <div v-if="isProcessing" class="text-slate-400 text-sm mt-1 flex items-center">
            <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Analyzing vector database...
          </div>
          <p v-else class="text-slate-200 text-sm mt-1 bg-darkBg p-3 rounded border border-slate-700 leading-relaxed">{{ aiResponse }}</p>
        </div>
        
        <!-- Save Expert Session Button -->
        <div v-if="!isRecording && !isProcessing && transcript && transcript !== 'Listening...'" class="mt-6 flex justify-center">
          <button @click="saveSession" :disabled="isSaving" class="bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2.5 px-6 rounded-full shadow-lg transition-colors flex items-center focus:outline-none focus:ring-2 focus:ring-blue-400 disabled:opacity-75 disabled:cursor-wait">
            <svg v-if="isSaving" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7H5a2 2 0 00-2 2v9a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-3m-1 4l-3 3m0 0l-3-3m3 3V4" />
            </svg>
            {{ isSaving ? 'Extracting Tools & Parsing XML...' : 'Save as Expert Video' }}
          </button>
        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onBeforeUnmount, onMounted } from 'vue'

const videoElement = ref(null)
const isCameraOn = ref(false)
const isRecording = ref(false)
const transcript = ref('')
const aiResponse = ref('')
const isProcessing = ref(false)
const isSaving = ref(false)

const canvasElement = ref(null)
const capturedFrames = ref([])
const selectedFrames = ref([])
let captureInterval = null

let stream = null
let recognition = null

onMounted(() => {
  if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onresult = (event) => {
      transcript.value = event.results[0][0].transcript;
      sendToAI(transcript.value);
    };

    recognition.onerror = (event) => {
      console.error('Speech recognition error', event.error);
      isRecording.value = false;
      isProcessing.value = false;
      if (event.error === 'not-allowed') {
        transcript.value = "Microphone access denied.";
      } else {
        transcript.value = "Error picking up audio. Sending test query...";
        sendToAI("Tell me about the Infiniti engine maintenance.");
      }
    };
  } else {
    console.warn("Speech API not supported in this browser.")
  }
})

const toggleCamera = async () => {
  if (isCameraOn.value) {
    stopCamera()
  } else {
    await startCamera()
  }
}

const startCamera = async () => {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ 
      video: { facingMode: 'environment' } 
    })
    if (videoElement.value) {
      videoElement.value.srcObject = stream
      isCameraOn.value = true
    }
  } catch (err) {
    console.error('Error accessing camera:', err)
    alert('Could not access camera. Ensure you are on HTTPS or localhost.')
  }
}

const stopCamera = () => {
  if (stream) {
    stream.getTracks().forEach(track => track.stop())
    stream = null
  }
  if (videoElement.value) {
    videoElement.value.srcObject = null
  }
  isCameraOn.value = false
}

const captureFrame = () => {
  if (!videoElement.value || !canvasElement.value) return
  const canvas = canvasElement.value
  const video = videoElement.value
  canvas.width = video.videoWidth
  canvas.height = video.videoHeight
  canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height)
  // Compress heavily to prevent hitting Ollama JSON limits
  const base64Data = canvas.toDataURL('image/jpeg', 0.4)
  capturedFrames.value.push(base64Data.split(',')[1])
}

const startRecording = () => {
  if (!isCameraOn.value) {
    alert('Please turn on the camera first to establish AR context!')
    return
  }
  isRecording.value = true
  aiResponse.value = ''
  transcript.value = 'Listening...'
  isProcessing.value = false
  
  // iOS Audio Unlock Hack - play a silent snippet during the user gesture to unlock speech synthesis
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel()
    window.speechSynthesis.speak(new SpeechSynthesisUtterance('')) 
  }

  capturedFrames.value = []
  captureInterval = setInterval(captureFrame, 333) // ~ 3 FPS (Every 10 frames approx)

  if (recognition) {
    try {
      recognition.start()
    } catch(e) {
      console.log("Recognition already started")
    }
  }
}

const stopRecording = () => {
  if(!isRecording.value) return
  isRecording.value = false
  isProcessing.value = true
  
  if (captureInterval) {
    clearInterval(captureInterval)
  }

  // Filter frames safely
  selectedFrames.value = []
  if (capturedFrames.value.length > 0) {
    if (capturedFrames.value.length <= 3) {
      selectedFrames.value = [...capturedFrames.value]
    } else {
      const step = Math.floor(capturedFrames.value.length / 3)
      selectedFrames.value = [
        capturedFrames.value[0],
        capturedFrames.value[step],
        capturedFrames.value[capturedFrames.value.length - 1]
      ]
    }
  }

  if (recognition) {
    recognition.stop() // this fires onresult automatically if speech was detected
  } else {
    transcript.value = "Speech API not supported. Simulating query..."
    sendToAI("How do I replace the engine oil filler cap?")
  }
}

const sendToAI = async (query) => {
  isProcessing.value = true
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: query, role: "EXPERT", images: selectedFrames.value })
    })
    const data = await res.json()
    aiResponse.value = data.answer
    
    // Speak the response natively
    if ('speechSynthesis' in window) {
      // Clean up markdown formatting like asterisks or hashes before speaking
      const cleanText = data.answer.replace(/[*#`]/g, '')
      const utterance = new SpeechSynthesisUtterance(cleanText)
      utterance.lang = 'en-US'
      utterance.rate = 1.05 // Slightly faster for responsiveness
      window.speechSynthesis.speak(utterance)
    }
    
  } catch (err) {
    aiResponse.value = "Error connecting to AI Backend. Make sure FastAPI is running."
  } finally {
    isProcessing.value = false
  }
}

const saveSession = async () => {
  isSaving.value = true
  try {
    const thumbnailData = selectedFrames.value.length > 0 ? selectedFrames.value[selectedFrames.value.length - 1] : null
    
    const res = await fetch("/api/upload-video", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ transcript: transcript.value, role: "EXPERT", thumbnail: thumbnailData })
    })
    const data = await res.json()
    alert("Success: " + data.message)
  } catch (err) {
    alert("Failed to save expert session.")
  } finally {
    isSaving.value = false
  }
}

onBeforeUnmount(() => {
  stopCamera()
})
</script>
