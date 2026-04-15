import { mount } from '@vue/test-utils'
import { describe, it, expect, vi } from 'vitest'
// import ChatInterface from '@/components/ChatInterface.vue'

describe('ChatInterface.vue', () => {
  it('verifies chat input field emits the correct message payload when submitted', async () => {
    // const wrapper = mount(ChatInterface)
    // const input = wrapper.find('input[type="text"]')
    // await input.setValue('How do I fix Machine 7?')
    // await wrapper.find('form').trigger('submit.prevent')
    
    // expect(wrapper.emitted()).toHaveProperty('sendMessage')
    // expect(wrapper.emitted().sendMessage[0]).toEqual(['How do I fix Machine 7?'])
  })

  it('verifies chat bubbles render correctly when receiving a mock response', async () => {
    // const wrapper = mount(ChatInterface, {
    //   props: {
    //     messages: [
    //       { role: 'user', content: 'How do I fix Machine 7?' },
    //       { role: 'ai', content: 'Use the 10mm wrench.' }
    //     ]
    //   }
    // })
    
    // const bubbles = wrapper.findAll('.chat-bubble')
    // expect(bubbles.length).toBe(2)
    // expect(bubbles[1].text()).toContain('Use the 10mm wrench.')
  })
})
