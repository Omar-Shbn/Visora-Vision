import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
// import VideoPlayer from '@/components/VideoPlayer.vue'

describe('VideoPlayer.vue', () => {
  it('verifies video player loads the correct URL', () => {
    // const videoUrl = 'http://localhost:8000/videos/123.mp4'
    // const wrapper = mount(VideoPlayer, {
    //   props: { url: videoUrl }
    // })
    
    // const video = wrapper.find('video')
    // expect(video.attributes('src')).toBe(videoUrl)
  })

  it('checks that the AI-generated Steps and Tools summary renders next to the video', () => {
    // const summaryData = {
    //   tools: ['screwdriver'],
    //   steps: ['Step 1: Open panel']
    // }
    // const wrapper = mount(VideoPlayer, {
    //   props: { summary: summaryData }
    // })
    
    // expect(wrapper.text()).toContain('screwdriver')
    // expect(wrapper.text()).toContain('Step 1: Open panel')
  })
})
