<template>
  <div class="h-screen w-full flex justify-center bg-black">
    <!-- Phone simulator container -->
    <div class="h-full w-full max-w-md bg-darkBg text-slate-200 overflow-hidden font-sans relative flex flex-col shadow-2xl border-x border-slate-800">
      
      <!-- Top Header -->
      <header class="flex items-center justify-center p-4 bg-darkBg border-b border-slate-800 shadow-md z-10 sticky top-0 backdrop-blur bg-opacity-80">
        <h1 class="text-xl font-bold bg-gradient-to-r from-blue-400 to-indigo-500 bg-clip-text text-transparent">
          EDGE AR Platform
        </h1>
      </header>

      <!-- Main Content Area -->
      <main class="flex-1 overflow-y-auto w-full relative pb-20 p-4">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>

      <!-- Bottom Mobile Navigation -->
      <nav class="absolute bottom-0 w-full bg-darkCard border-t border-slate-800 flex justify-around p-3 pb-safe shadow-[0_-4px_15px_rgba(0,0,0,0.3)] z-50">
        <router-link to="/simulator" class="flex flex-col items-center justify-center w-full text-slate-400 hover:text-primary transition-colors" active-class="text-primary font-medium">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
          <span class="text-xs">AR Simulator</span>
        </router-link>
        <router-link to="/knowledge" class="flex flex-col items-center justify-center w-full text-slate-400 hover:text-primary transition-colors" active-class="text-primary font-medium">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
          </svg>
          <span class="text-xs">Knowledge Base</span>
        </router-link>
      </nav>
    </div>
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
/* Environment safe area padding for modern phones */
.pb-safe {
  padding-bottom: env(safe-area-inset-bottom, 12px);
}
</style>
